from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin
from flask_heroku import Heroku
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "JackNDustin"
csrf.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"
class Login(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username =db.Column(db.String(30),unique=True)
    password = db.Column(db.String(30))
class User(db.Model):
    my_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username =db.Column(db.String(30),unique=True)
    l_name = db.Column(db.String(30))
    f_name = db.Column(db.String(30))
    email = db.Column(db.String(30),unique=True)
class WishList(db.Model):
    wish_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    name = db.Column(db.String(30))
    comments = db.Column(db.String(100))
class Product(db.Model):
    product_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Float)
    category = db.Column(db.String(30))
    url = db.Column(db.String(30))
class Granted(db.Model):
    gid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    product_id = db.Column(db.Integer)
    wishList_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
