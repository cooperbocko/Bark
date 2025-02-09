from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from bark.models import Course
from flask_login import current_user

class CreateCourseForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    code = PasswordField('Code', 
                             validators=[DataRequired()])
    submit = SubmitField('Create Course')
    
    def validate_code(self, code):
        #check if code is already in use
        course = Course.query.filter_by(code=code.data).first()
        if course:
            raise ValidationError('Code already in use!')
        
class JoinCourseForm(FlaskForm):
    code = PasswordField('Code', 
                             validators=[DataRequired()])
    submit = SubmitField('Join Course')
    
    def validate_course(self, code):
        course = Course.query.filter_by(code=code.data).first()
        if course in current_user.courses:
            raise ValidationError('Already joined!')
    