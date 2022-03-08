
from flask import Flask, jsonify
from flask_mail import Mail, Message
import os

from app import app

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get('SENDER_EMAIL'),
    "MAIL_PASSWORD": os.environ.get('EMAIL_PWD')
}

app.config.update(mail_settings)
mail = Mail(app)


# import smtplib
# import os

# sender_email = os.environ.get('SENDER_EMAIL')
# email_pwd = os.environ.get('EMAIL_PWD')

# def send_email(receiver_email, username):
#     message = f'Welcome {username} to the Pitches App. Thanks for signing up!'
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.login(sender_email, email_pwd)
#     server.sendmail(sender_email, receiver_email, message)
