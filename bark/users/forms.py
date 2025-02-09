from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from bark.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), 
                                    Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                             validators=[DataRequired(), 
                                         EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        #check for uga email ending.
        #if not email.data.endswith("@uga.edu"):
        #    raise ValidationError('Not a uga email!')
        user = User.query.filter_by(email=email.data).first()
        if user: 
            raise ValidationError('Email already exists!')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), 
                                    Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')