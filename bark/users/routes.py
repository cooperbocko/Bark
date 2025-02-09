from flask import render_template, url_for, flash, redirect, request, Blueprint
from bark import db, bcrypt
from bark.users.forms import RegistrationForm, LoginForm
from bark.models import User
from flask_login import login_user, current_user, logout_user, login_required
from bark.users.utils import send_authentication_email
users = Blueprint('users', __name__)

#Creates user and sends email to validate the email.
@users.route("/register", methods=['GET', 'POST'])
def register():
    #check that user is not currently logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    #get registration form
    form = RegistrationForm()
    
    #submitting form
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email = form.email.data, password = hashed_password, type = 'Student')
        send_authentication_email(user)
        flash(f'Email sent for authentication', 'info')
        return redirect(url_for('users.login'))

    #load form 
    return render_template('register.html', title = 'Register', form = form)

#Validates the user
@users.route("/register/<token>", methods=['GET', 'POST'])
def validate_user(token):
    #check that user is not currently logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    #check if valid token is provided
    userdict = User.verify_token(token)
    if not userdict:
        flash(f'Invalid or expired token! Please register again!', 'warning')
        return redirect(url_for('users.register'))
        
    print(userdict)
    #if valid token provided, update user
    user = User(email = userdict["email"], password = userdict["password"], type = userdict["type"])
    db.session.add(user)
    db.session.commit()
    flash(f'User validated! You may now log in!')
    return redirect(url_for('users.login'))

#Login the user
@users.route("/login", methods=['GET', 'POST'])
def login():
    #check that user is not currently logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    #get login form
    form = LoginForm()
    
    #submitting form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged In!', 'success')
            return redirect(url_for('next_page')) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login Failed!', 'failure')
    
    #load form
    return render_template('login.html', title = 'Login', form = form)

#Logout User
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


    