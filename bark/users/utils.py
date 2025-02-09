import os
import secrets
from flask import url_for, current_app
from bark import mail
from flask_mail import Message

def send_authentication_email(user):
    token = user.get_token()
    msg = Message('Bark Registration', 
                  sender='noreply@bark.com', 
                  recipients=[user.email])
    msg.body = 'To authenticate your account, visit the following link: localhost:5000' + url_for('users.validate_user', token=token, external=True) + '\n If you did not make thie request, ignore this email.'
    mail.send(msg)