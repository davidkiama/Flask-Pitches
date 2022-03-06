from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db

from .models import Pitch


main = Blueprint('main', __name__)


@main.route('/')
def index():

    pitches = Pitch.query.all()

    return render_template('index.html', pitches=pitches)


@main.route('/profile')
@login_required
def profile():

    pitches = Pitch.query.filter_by(author=current_user.id).all()
    return render_template('profile.html', username=current_user.username, pitches=pitches)


@main.route('/create_pitch', methods=['GET', 'POST'])
@login_required
def create_pitch():

    title = request.form.get('title')
    content = request.form.get('content')
    category = request.form.get('category')

    if title and content and category:
        pitch = Pitch(title=title, content=content,
                      category=category, author=current_user.id)
        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('main.profile'))

    return render_template('upload_pitch.html', user=current_user)
