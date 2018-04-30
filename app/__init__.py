from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app  = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY']                     = "8Mfj4PXls5kRglU"
app.config['SQLALCHEMY_DATABASE_URI']        = 'postgresql://jttntwieccszqe:4a879bbff962b6942f0bf0981d04ee59dd38525a79acb874df17e58ad7982642@ec2-174-129-41-64.compute-1.amazonaws.com:5432/d226uk0b0lsbpq'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)
UPLOAD_FOLDER = "./app/static/images"
import models

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
