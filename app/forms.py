from flask_wtf import Form,RecaptchaField
from wtforms import StringField, PasswordField,IntegerField,TextAreaField,SelectField
from wtforms.validators import InputRequired,Email,EqualTo,Length,Regexp,\
        AnyOf,Optional,NumberRange,ValidationError
from flask.ext.login import current_user
from .models import User,Category



RESERVED_WORDS = [
    'root', 'admin', 'bot', 'robot', 'master', 'webmaster',
    'account', 'people', 'user', 'users', 'project', 'projects',
    'search', 'action', 'favorite', 'like', 'love', 'none',
    'team', 'teams', 'group', 'groups', 'organization',
    'organizations', 'package', 'packages', 'org', 'com', 'net',
    'help', 'doc', 'docs', 'document', 'documentation', 'blog',
    'bbs', 'forum', 'forums', 'static', 'assets', 'repository',

    'public', 'private',
    'mac', 'windows', 'ios', 'lab',
]

class LoginForm(Form):
    username = StringField('username',validators=[
        InputRequired(message='Need a username'),
        Length(min=3,max=20)])
    password = PasswordField('password',validators=[
        InputRequired(message='Need a password')])
    #recaptcha = RecaptchaField()

class RegisterForm(LoginForm):
    username = StringField('Username',validators=[
        InputRequired(),
        Length(min=3,max=30),
        Regexp('^[a-z0-9A-z_]+$')])
    email = StringField('Email',validators=[
        InputRequired(message='Need a email'),
        Email(),
        Length(max=100)])
    password = PasswordField('New Password',validators=[
        InputRequired(message='Need a password'),
        EqualTo('confirm',message='Passwords must match')])
    confirm = PasswordField('Reqeat Password')

    def validate_username(form,field):
        data = field.data.lower()
        if data in RESERVED_WORDS:
            raise ValidationError('This is a reserved name.')
        if User.query.filter_by(username=field.data).count():
            raise ValidationError('This name has been registered.')

    def validate_email(form,field):
        if User.query.filter_by(email=field.data.lower()).count():
            raise ValidationError('This email has been registered.')


class ProfileForm(Form):
    nick = StringField('nick',validators=[
        Optional(),
        Length(max=80)])
    gender = StringField('gender',validators=[
        Optional(),
        AnyOf(['male','female'])])
    age = IntegerField('age',validators=[
        Optional(),
        NumberRange(0,100)])
    department = StringField('department',validators=[
        Optional(),
        Length(max=120)])
    phone = StringField('phone',validators=[
        Optional()])
    qq = IntegerField('qq',validators=[
        Optional()])


class ChangePasswordForm(Form):
    old_password = PasswordField("Old Password",validators=[
        InputRequired(message="需要输入密码")])

    new_password = PasswordField("Password",validators=[
        InputRequired(),
        EqualTo('confirm_new_password',message="密码必须相同")])

    confirm_new_password = PasswordField('Confirm New Password')

    def validate_old_password(form,field):
        if not current_user.check_password(field.data):
            raise ValidationError('Password is wrong.')


class PostForm(Form):
    title = StringField('Post Title',validators=[
        InputRequired(),
        Length(max=225)])
    content = TextAreaField('Post Title',validators=[
        InputRequired()
        ])
    category_id = SelectField('Category id',coerce=int,validators=[
        InputRequired()])





'''====== The admin fetures ============'''

#class CategoryForm(Form):
#    name = StringField('Category Name',validators=[
#        InputRequired(),
#        Length(max=40)])
#    description = StringField('Category decription',validators=[
#        Optional()])

    #def validate_name(form,field):
    #    print(field.data)
    #    if Category.query.filter_by(name=field.data).count():
    #        raise ValidationError('This category already exists.')








