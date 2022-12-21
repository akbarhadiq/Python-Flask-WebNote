# different python files for different functions of the website. hmmm nice
# uses flask blueprint
# how :

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db #--> db is instansiated in __init__.py
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # filter the user that have inputted email
        user = User.query.filter_by(email=email).first()

        # if you found user then check the password
        if user:
            # check the password if user exists
            if check_password_hash(user.password, password):
                flash("Logged in succesfully!", category='success')
                login_user(user, remember=True) # remember saves the logged in user in a browser session
                return redirect(url_for('views.home'))
            else:
          
                flash("Incorrect password, try again!", category='error')
        # if user does note exist
        else:
            flash("That email does not exist!", category="error")

    return render_template("login.html", text="Test", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":

        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        # check if there are users previously registering by that email
        user = User.query.filter_by(email=email).first()

        if user: 
            # if there are already previous user using that email, then flash an error message
            flash("User already exist!", category="error")
        else: 
            # check the input value
            if len(email) < 4:
                flash("Email is not valid", category='error')
            elif len(firstName) < 2:
                flash("First name must be greater than 1 characters", category="error")
            elif password1 != password2:
                flash("Passwords don't match", category="error")
            elif len(password1) < 7:
                flash("Password must be greater than 7 characters")
            else:
                # if input value validates then,
                # add user to the database
                new_user = User(
                    email=email,
                    first_name=firstName,
                    password=generate_password_hash(password=password1, method="sha256")
                )
                db.session.add(new_user)
                db.session.commit()
                flash("Account successfully created", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
                # redirect to home
            

    return render_template("sign_up.html", user=current_user)