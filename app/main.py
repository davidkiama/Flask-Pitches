from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import os

from app import app
from . import db
from .models import Downvote, Pitch, Comment, Upvote

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

    if request.method == 'POST':
        category = request.form.get('category')
        text = request.form.get('text')

        print(len(text))
        if len(text) > 255:
            flash('Pitch is too long. Max 255 characters.')
            return redirect(url_for('main.create_pitch'))
        pitch = Pitch(text=text, category=category, author=current_user.id)

        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('main.profile'))

    return render_template('create_pitch.html', user=current_user)


@main.route('/create-comment/<pitch_id>', methods=['POST'])
@login_required
def create_comment(pitch_id):
    comment = request.form.get('text')
    pitch = Pitch.query.filter_by(id=pitch_id).first()

    if comment and pitch:
        new_comment = Comment(text=comment, author=current_user.id,
                              pitch_id=pitch_id)
        db.session.add(new_comment)
        db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/upvote/<pitch_id>', methods=['POST'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.filter_by(id=pitch_id).first()

    # check if user has upvoted the pitch
    if current_user.id in [upvote.user_id for upvote in pitch.upvotes]:
        # remove the user's upvote
        print('User has already upvoted')
        upvote = Upvote.query.filter_by(user_id=current_user.id).first()
        db.session.delete(upvote)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        # add the user's upvote
        upvote = Upvote(user_id=current_user.id, pitch_id=pitch_id)
        db.session.add(upvote)
        db.session.commit()
        return redirect(url_for('main.index'))


@main.route('/downvote/<pitch_id>', methods=['POST'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.filter_by(id=pitch_id).first()

    # check if user has downvoted the pitch
    if current_user.id in [downvote.user_id for downvote in pitch.downvotes]:
        # remove the user's down
        downvote = Downvote.query.filter_by(user_id=current_user.id).first()
        db.session.delete(downvote)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        # add the user's downvote
        downvote = Downvote(user_id=current_user.id, pitch_id=pitch_id)
        db.session.add(downvote)
        db.session.commit()
        return redirect(url_for('main.index'))


@main.route('/category/<category>')
def category(category):
    pitches = Pitch.query.filter_by(category=category).all()
    return render_template('category.html', pitches=pitches, category=category)
