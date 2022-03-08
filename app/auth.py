
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from flask_mail import Message
import os

from .models import User
from . import db
from .email import mail


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email').lower()
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User with that email does not exist')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        flash('Incorect password.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes then...
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup_post():

    if request.method == 'POST':

        email = request.form.get('email').lower()
        username = request.form.get('username').lower()
        password = request.form.get('password')

        # if this returns a user, then the email already exists in database
        user_by_email = User.query.filter_by(email=email).first()
        user_by_username = User.query.filter_by(username=username).first()

        if user_by_email:  # if user is found,we redirect to try again
            flash('Email already exists')
            return redirect(url_for('auth.signup'))

        if user_by_username:  # if user is found,we redirect to try again
            flash('Username already taken')
            return redirect(url_for('auth.signup'))

        user = User(email=email, username=username,
                    password=generate_password_hash(password, method='sha256'))

        # msg = Message(subject='Welcome', sender=os.environ.get(
        #     'SENDER_EMAIL'), recipients=[email], body=f'Hello {username},\n Welcome to the Pitches App. Thanks for signing up!')
        # mail.send(msg)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template('signup.html')
