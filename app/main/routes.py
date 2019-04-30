from flask import Blueprint,render_template, request,url_for,redirect,flash
from app.models import Pitch,Comment,User
from app.users.routes import Register,Login
from app.users.forms import FollowForm
from app import bcrypt,db
from flask_login import login_user
from flask_mail import Message
from ..email import mail_message
from ..requests import get_quote


main = Blueprint('main',__name__)


@main.route("/",methods=['GET','POST'])
@main.route("/home",methods=['GET','POST'])
def home():
    posts = Pitch.query.all()
    comments = Comment.query.all()
    hashtags= Pitch.query.filter_by(hashtags='property').all()
    quote_object = get_quote()
    # author= quote_object["author"]
    quote = quote_object["quote"]
    print(quote)
    
    # if current_user.is_authenticated:
    #     return redirect(url_for('circles'))
    registerForm = Register()
    if registerForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registerForm.password.data).decode('utf-8')
        user = User(username = registerForm.username.data, email = registerForm.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login!','success')
        mail_message("Welcome to watchlist","email/welcome_user",user.email,user=user)
        return redirect(url_for('main.home'))
    # else:
    #     flash('Registration Unsuccessful. Details you entered are already taken','danger')
    
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    #form=form, registerForm=registerForm

    return render_template('home.html', title='login',form=form, registerForm=registerForm ,posts=posts, comments=comments,hashtags=hashtags,quote=quote)

@main.route("/account/<int:post_id>",methods=['GET','POST'])
def account(post_id):
    post = Pitch.query.get_or_404(post_id)
    allposts = Pitch.query.all()
    # form = FollowForm()
    # if form.validate_on_submit():
    #     current_user.following[] = 
        
    return render_template('programmeraccount.html',post=post, allposts=allposts)

