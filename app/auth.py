
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user


from .models import User
from . import db
from .email import send_email


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
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
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:  # if user is found,we redirect to try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=username,
                    password=generate_password_hash(password, method='sha256'))

    send_email(email, username)

    # add new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))
