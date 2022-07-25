from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_ckeditor import CKEditor



app = Flask(__name__)



app.config['SECRET_KEY'] = 'gigi'
ckeditor = CKEditor(app)


#db connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/man"
#initialize db
db = SQLAlchemy(app)


login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'






from app import views
from app import models
from app import forms