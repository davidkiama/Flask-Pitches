from cgitb import text
from flask_login import UserMixin
from app import db


class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    profile_pic = db.Column(db.String(), nullable=False, default='default.jpg')
    pitches = db.relationship('Pitch', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)


class Pitch (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    category = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    comments = db.relationship(
        'Comment', backref='pitch', passive_deletes=True)


class Comment (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey(
        'pitch.id', ondelete='CASCADE'), nullable=False)
