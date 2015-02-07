from flask_wtf import Form,RecaptchaField
from wtforms import StringField, PasswordField,IntegerField,TextAreaField
from wtforms.validators import InputRequired,Email,EqualTo,Length,Regexp,\
        AnyOf,Optional,NumberRange,ValidationError
from flask.ext.login import current_user
from app.models import User,Category

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



class UserForm(Form):
    username = StringField('Username',validators=[
        InputRequired(),
        Length(min=3,max=30),
        Regexp('^[a-z0-9A-z_]+$')])
    email = StringField('Email',validators=[
        InputRequired(message='Need a email'),
        Email(),
        Length(max=100)])
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

class CategoryForm(Form):
    name = StringField('Category Name',validators=[
        InputRequired(),
        Length(max=40)])
    description = StringField('Category decription',validators=[
        Optional()])

    def validate_name(form,field):
    #    print(field.data)
        if Category.query.filter_by(name=field.data).count():
            raise ValidationError('This category already exists.')



