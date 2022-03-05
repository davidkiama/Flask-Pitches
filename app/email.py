

import smtplib

import os

sender_email = os.environ.get('SENDER_EMAIL')
email_pwd = os.environ.get('EMAIL_PWD')


def send_email(receiver_email, username):
    message = f'Welcome {username} to the Pitches App. Thanks for signing up!'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, email_pwd)
    server.sendmail(sender_email, receiver_email, message)
