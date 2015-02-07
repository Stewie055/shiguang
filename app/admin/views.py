from flask import Blueprint,render_template,abort,redirect,url_for,request
from app.models import Category,User,Post
from app.forms import PostForm
from app.admin.forms import UserForm,CategoryForm


admin = Blueprint('admin',__name__,
                    template_folder='templates')

@admin.route('/')
def index():
    return redirect(url_for('admin.show_users'))

@admin.route('/categorys')
def show_categorys():
    categorys = Category.query.all()
    return render_template('admin/categorys.html',categorys=categorys)

@admin.route('/category/<int:category_id>')
def show_category():
    #TODO: show posts under a category
    pass

@admin.route('/category/<int:category_id>/delete')
def delete_category():
    #TODO: delete a category. How to deal with the posts under the category?
    pass

@admin.route('/category/new',methods=['GET','POST'])
@admin.route('/category/<int:category_id>/edit',methods=['GET','POST'])
def edit_category(category_id=None):
    '''Add or Edit the category
    when a category id is passed, the category will be eidited.
    Ortherwise a new category will be created
    :param category_id: The id of the category
    '''
    if category_id:
        category = Category.query.get(category_id)
    else:
        category = Category()
    form = CategoryForm()
    if form.validate_on_submit():
        form.populate_obj(category)
        category.save()
        return redirect(url_for('admin.show_categorys'))
    print(form.errors)
    return render_template('admin/edit-category.html',form=form,category=category)


@admin.route('/users')
@admin.route('/users/<int:page>')
def show_users(page=1):
    users_page = User.query.paginate(page)
    return render_template('admin/users.html',pagination=users_page)

@admin.route('/user/<int:user_id>')
def user_detail(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('admin/user-detail.html',user=user)
    flash("User not found","danger")
    abort(404)


@admin.route('/user/<int:user_id>/delete')
def delete_user():
    #TODO: Is it a nessecery to delete a user? Or just ban it.
    pass

@admin.route('/user/<int:user_id>/edit',methods=['GET','POST'])
def edit_user(user_id=None):
    if user_id:
        user = User.query.get(user_id)
    else:
        user = User()
    form = UserForm(request.form,user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.save()
        return redirect(url_for('admin.show_users'))
    print(form.errors)
    return render_template('admin/edit-user.html',form=form,user=user)

@admin.route('/posts/',defaults={'page':1})
@admin.route('/posts/page/<int:page>')
def show_posts(page):
    posts_page = Post.query.order_by(Post.id.desc()).paginate(page)
    return render_template('admin/posts.html',pagination=posts_page)

@admin.route('/post/<int:post_id>')
def view_post(post_id):
    return redirect(url_for('view_post',post_id=post_id))

@admin.route('/post/<int:post_id>/edit',methods=['GET','POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    if post:
        form = PostForm(request.form,post)
        form.category_id.choices = [(g.id,g.name) for g in Category.query.order_by('id')]
        if form.validate_on_submit():
            form.populate_obj(post)
            post.save()
            return redirect(url_for('admin.show_posts'))
        return render_template('admin/edit-post.html',form=form)
    flash('The post does not exists')
    abort(404)
    pass

@admin.route('/post/<int:post_id>/delete')
def delete_post(post_id):
    '''delete a post by the administrator
    :param post_id the id of the post
    '''
    post = Post.query.get(post_id)
    post.delete()
    return redirect('admin.show_posts')
