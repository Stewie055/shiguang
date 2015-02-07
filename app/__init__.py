from flask import Flask
import os
from werkzeug import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy
from contextlib import closing
import sqlite3
from flask.ext.login import LoginManager


#UPLOAD_FOLDER = 'app/static/image'
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object('config')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(app.root_path, 'test.db')
#app.config['DATABASE'] = os.path.join(app.root_path, 'test.db')



db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


#====== init db ========================================

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schemql.sql',mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

from app import views

from app.admin import admin

app.register_blueprint(admin,url_prefix='/admin')
