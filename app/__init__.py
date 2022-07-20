from flask import Flask
from  flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL


app = Flask(__name__)



app.config['SECRET_KEY'] = 'gigi'


#db connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/man"
db = SQLAlchemy(app)





from app import views
from app import models
from app import forms