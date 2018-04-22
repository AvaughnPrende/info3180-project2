from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app  = Flask(__name__)

app.config['SECRET_KEY'] = "8Mfj4PXls5kRglU"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://bestinfogroup:password123@localhost/project2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
app.config['WTF_CSRF_ENABLED'] = False

db = SQLAlchemy(app)
UPLOAD_FOLDER = "./app/static/images"
import models

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views