
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os


from app import app
from . import db
from .models import Pitch, Comment

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


# To prevent users from uploading files with malicious extensions, we use the
ALLOWED_EXTENSIONS = {'MPG', 'MP4', 'MPEG', 'MPE', 'MPV', 'WEBM' 'OGG',
                      'AAC', 'WAV', 'WMA', 'MP4', 'AVI', 'MOV', 'WMV', 'FLV', 'SWF', 'M4A'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS


@main.route('/create_pitch', methods=['GET', 'POST'])
@login_required
def create_pitch():

    if request.method == 'POST':
        category = request.form.get('category')

        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('main.create_pitch'))

        file = request.files['file']

        if not allowed_file(file.filename):
            flash('Video only')
            return redirect(url_for('main.create_pitch'))

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if filename and category:

            pitch = Pitch(filename=filename, category=category,
                          author=current_user.id)

            db.session.add(pitch)
            db.session.commit()

            return redirect(url_for('main.profile'))

    return render_template('upload_pitch.html', user=current_user)


@main.route('/create-comment/<pitch_id>', methods=['POST'])
@login_required
def create_comment(pitch_id):
    comment = request.form.get('comment')
    pitch = Pitch.query.filter_by(id=pitch_id).first()

    if comment and pitch:
        new_comment = Comment(comment=comment, author=current_user.id,
                              pitch_id=pitch_id)
        db.session.add(new_comment)
        db.session.commit()

    return redirect(url_for('main.index'))
