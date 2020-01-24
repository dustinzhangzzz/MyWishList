from flask import Flask, request,render_template,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import jsonify
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user,logout_user, login_required,current_user
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import json
from urllib.parse import urljoin,urlparse
from datetime import datetime
from data import Login, User, Product, Granted, WishList
from flask_heroku import Heroku
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Login.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email has already been used, please use another email')

class ListForm(FlaskForm):
    myemail = StringField("Retrive WishLists Using User's email", validators=[DataRequired()])
    find_list = SubmitField("Find Wish List", validators=[DataRequired()])

    def validate_myemail(self,myemail):
        user = User.query.filter_by(email = myemail.data).first()
        if user is None:
            raise ValidationError('We cannot find this email.')
class titleForm(FlaskForm):
    title = StringField("Please enter a new WishList name ")
    search = SubmitField("Create list")

csrf = CSRFProtect()
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "JackNDustin"
csrf.init_app(app)
heroku = Heroku(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test2.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(int(user_id))
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Login.query.filter_by(username=username).first()
        if not user or password!=user.password:
            flash("User Name or Password is wrong")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        print(current_user.username)
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Login(username=form.username.data, password=form.password.data)
        logged_user = User(username=form.username.data,f_name = form.first_name.data, l_name = form.last_name.data, email = form.email.data)
        register.logged_user = logged_user
        db.session.add(logged_user)
        db.session.commit()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are now logged out!")
    return redirect(url_for('login'))
@app.route("/index", methods=['POST','GET'])
@login_required
def index():
    form = ListForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.myemail.data).first()
        userid = user.my_id
        firstName = user.f_name
        lastName = user.l_name
        name = firstName + " "+lastName
        wishLists = WishList.query.filter_by(user_id=userid).all()
        for item in wishLists:
            print(item.comments)
        wishListDic = {}
        for wishes in wishLists:
            title = wishes.name
            time = wishes.time
            comment = wishes.comments
            key = title +","+str(time)+","+comment
            products = db.session.execute("select * from Product join Granted on Product.product_id = Granted.product_id where wishList_id =:param",{"param":wishes.wish_id}).fetchall()
            wishListDic[key] = products
        return render_template("list.html", dictionary = wishListDic, user = name)
    return render_template("index.html",form1=form)
@app.route('/newlist', methods=['POST','GET'])
@login_required
def newlist():
    return render_template("newlist.html")
@app.route('/search/<item>', methods=['POST','GET'])
@login_required
def search(item):
    print('working')
    try:
        api = Finding(appid="Xiaoxuan-MywishLi-PRD-6b31d5c2d-eacef9e4", config_file=None)
        response = api.execute('findItemsAdvanced', {'keywords': item})
        dict = response.dict()
        res = dict["searchResult"]["item"]
        for item in res:
            product = Product(product_id = item["itemId"], name = item["title"], price = item["sellingStatus"]["currentPrice"]["value"], category = item["primaryCategory"]["categoryName"], url = item["viewItemURL"])
            try:
                db.session.add(product)
                db.session.commit()
            except:
                db.session.rollback()
    except ConnectionError as e:
        return e
    return json.dumps(res)
@app.route('/add/<productlist>/<title>/<comment>',methods=['POST','GET'])
@login_required
def add(productlist,title,comment):
    list = json.loads(productlist)
    user = User.query.filter_by(username =current_user.username ).first()
    id = user.my_id
    wish = WishList(user_id = id,time = datetime.now(),name = title,comments =comment)
    try:
        db.session.add(wish)
        db.session.commit()
        print("right")
    except:
        db.session.rollback()
        print("wrong")
    for items in list:
        grant = Granted(product_id = items, wishList_id = wish.wish_id,time = datetime.now())
        try:
            db.session.add(grant)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"error": "occur when adding granted!"}), 400
    return jsonify({"body": "sucess!"}), 200
if __name__=="__main__":
    app.run(debug=True)
