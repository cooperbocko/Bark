import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from bark.models import Attendance, Course
from flask_login import current_user

class CreateAttendanceForm(FlaskForm):
    code = PasswordField('Code', 
                             validators=[DataRequired()])
    expires = BooleanField('Expires?', validators=[DataRequired()])
    expirestime = IntegerField('Expires Time?')
    submit = SubmitField('Create Course')
    

class CheckAttendanceForm(FlaskForm):
    code = PasswordField('Code', 
                             validators=[DataRequired()])
    submit = SubmitField('Create Course')
    
    def validate_attendance(self, code):
        attendance = Attendance.query.filter_by(code=code.data).first()
        if not attendance:
            raise ValidationError('No attendance found!')
        if attendance.expiretime < datetime.now(datetime.timezone.utc):
            raise ValidationError('Code expired!')
    