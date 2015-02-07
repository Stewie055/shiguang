from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from app import db
from flask import url_for



'''==============================================================

        The User Model

=============================================================='''

class User(db.Model):
    __tablename__ ="users"
    __searchable__ =['username','email']

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    _password = db.Column('password',db.String(120),nullable=False)
    date_joined = db.Column(db.DateTime,default=datetime.utcnow())
    nick = db.Column(db.String(80))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    department = db.Column(db.String(120))
    phone = db.Column(db.String(16))
    qq = db.Column(db.String(12))
    #TODO : avatar

    posts = db.relationship("Post",backref="author",lazy="dynamic")

    post_count = db.Column(db.Integer,default=0)

    @property
    def last_post(self):
        pass

    @property
    def url(self):
        """Returns the url for the user"""
        return url_for("profile", username=self.username)

    @property
    def permissions(self):
        """Returns the permission for the user"""
        return self.get_permissions()

    @property
    def days_registered(self):
        """Returns the amount of days the user is registered."""
        days_registered = (datetime.utcnow() - self.date_joined).days
        if not days_registered:
            return 1
        return days_registered


    #method
    def _get_password(self):
        """Returns the hashed password"""
        return self._password

    def _set_password(self,password):
        """Generates a password hash for the provieded password"""
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only
    password = db.synonym('_password',descriptor=property(_get_password,_set_password))

    def check_password(self,password):
        """Check passwords.Returns ture if matchs"""
        if self.password is None:
            return False
        return check_password_hash(self.password,password)

    @classmethod
    def authenticate(cls,login,password):
        """A classmethod for authenticating users
        It returns true if the user exists and has entered a correct password
        :param login: This can be either a username or a email address.
        :param password: The password that is connected to username and email.
        """

        user = cls.query.filter(db.or_(User.username == login,
                                       User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    @classmethod
    def get(cls,uid):
        return cls.query.filter(User.username == uid).first()

    def _make_token(self, data, timeout):
        s = Serializer(current_app.config['SECRET_KEY'], timeout)
        return s.dumps(data)

    def _verify_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        data = None
        expired, invalid = False, False
        try:
            data = s.loads(token)
        except SignatureExpired:
            expired = True
        except Exception:
            invalid = True
        return expired, invalid, data

    def make_reset_token(self, expiration=3600):
        """Creates a reset token. The duration can be configured through the
        expiration parameter.
        :param expiration: The time in seconds how long the token is valid.
        """
        return self._make_token({'id': self.id, 'op': 'reset'}, expiration)

    def verify_reset_token(self, token):
        """Verifies a reset token. It returns three boolean values based on
        the state of the token (expired, invalid, data)
        :param token: The reset token that should be checked.
        """

        expired, invalid, data = self._verify_token(token)
        if data and data.get('id') == self.id and data.get('op') == 'reset':
            data = True
        else:
            data = False
        return expired, invalid, data

    def all_posts(self,page):
        """Returns a paginated result with all posts the user has created."""

        return Post.query.filter(Post.user_id == self.id).\
                paginate(page,app_config['TOPICS_PER_PAGE'],False)

    def get_permissions(self,exclude=None):
        """Returns a dictionary with all the permissions the user has.

        :param exclude: a list with excluded permissions. default is None.
        """
        pass

    def ban(self):
        """Bans the uesr.Returns True upon success"""
        #TODO: ban user
        pass

        #if not self.get_permissions()['banned']:

    def unban(self):
        """Unbans the user. Returns True upon success."""
        #TODO: unban user
        pass

    def save(self, groups=None):
        """Saves a user. If a list with groups is provided, it will add those
        to the secondary groups from the user.
        :param groups: A list with groups that should be added to the secondary groups from user.
        """
        # TODO: groups
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Deletes the User"""

        #TODO: delete user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username




"""========================================================================

        The Post Model

========================================================================"""

class Post(db.Model):
    __tablename__ = "posts"
    __searchable__ = ['content','username']

    id = db.Column(db.Integer,primary_key=True)
    category_id = db.Column(db.Integer,
                         db.ForeignKey("categorys.id",
                                        use_alter=True,
                                        name="post_topic_id"))
    title = db.Column(db.String(255),nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=True)
    content = db.Column(db.Text,nullable=False)
    date_published = db.Column(db.DateTime,default=datetime.utcnow())
    date_updated = db.Column(db.DateTime,default=datetime.utcnow())
    locked = db.Column(db.Boolean,default=False)
    #comments = db.relationship('Comment',backref='post',lazy='dynamic')

    #TODO other property tobe added

    @property
    def url(self):
        """Returns the url for the post"""
        return url_for("view_post",post_id=self.id)

    def save(self,author=None,category=None):
        """Save a Post and returns the Post object. If no parameters are
        given, it will only update the post.

        :param author: The user who published the post

        :param category: The category the post belongs to
        """

        #update the post
    #TODO is the update time modified?
        if self.id:
            db.session.add(self)
            db.session.commit()
            return self

        #Set the category and author id
        self.category_id = category.id
        self.author_id = author.id
        self.author_nick = author.nick

        # Set the last_updated  time.
        self.date_updated = datetime.utcnow()

        self.date_published = datetime.utcnow()

        # Update the post count of the author and category
        if author:
            self.author_id = author.id
            author.post_count +=1
            db.session.add(author)

        if category:
            self.category_id = category.id
            category.post_count +=1
            db.session.add(category)

        # Insert and commit the post
        db.session.add(self)
        db.session.commit()

        return self


    def delete(self):
        """Delete a post"""

        # update the post counts
        author = self.author
        category = self.category
        author.post_count -= 1
        category.post_count -=1

        db.session.add(author)
        db.session.add(category)

        # delete the post
        db.session.delete(self)
        db.session.commit()

        return self




"""===========================================================================

        The category Model

============================================================================"""

class Category(db.Model):
    __tablename__ = "categorys"
    __searchable__ = ['name','description']

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),nullable=False,unique=True)
    description = db.Column(db.Text,nullable=True)
    post_count = db.Column(db.Integer,default=0)

    posts = db.relationship('Post',backref='category',lazy='dynamic')

    @property
    def url(self):
        '''Returns the url for the category'''
        return url_for('category',category_name=self.name)

    def save(self):
        '''Saves a category'''

        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        #TODO : change all posts' category to default
        pass





