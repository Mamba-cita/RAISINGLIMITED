from flask import Flask
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_migrate import Migrate
from flask_ckeditor import CKEditor



app = Flask(__name__)




app.config['SECRET_KEY'] = 'gigi'
ckeditor = CKEditor(app)



app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get ('SQLALCHEMY_DATABASE_URI')
#online db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b3ce1f92dab14b:2b89e72b@us-cdbr-east-06.cleardb.net/heroku_32bfd973b92d25e?reconnect=true'
db = SQLAlchemy(app)




#initialize db
db = SQLAlchemy(app)
migrate = Migrate(app,db)

login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'






from app import views
from app import models
from app import forms