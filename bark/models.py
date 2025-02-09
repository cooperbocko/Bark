from email.policy import default
from flask import current_app
from datetime import datetime, timedelta, timezone
from bark import db, login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer


# Association table for User-Course Many-to-Many relationship
user_courses = db.Table('user_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

# Association table for User-Attendance Many-to-Many relationship
user_attendances = db.Table('user_attendances',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('attendance_id', db.Integer, db.ForeignKey('attendance.id'), primary_key=True)
)


#For Login Manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    #variables
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    
    #relationships
    #many to many
    courses = db.relationship('Course', secondary=user_courses, backref='users', lazy='select')
    #many to many
    attendances = db.relationship('Attendance', secondary=user_attendances, backref='users', lazy='select')
    #one to many
    
    
    #methods
    def get_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'email': self.email, 'password': self.password, 'type': self.type, 'is_validated': self.is_validated})
    
    @staticmethod
    def verify_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user = s.loads(token, max_age=expires_sec)
        except:
            return None
        return user
    
    def __repr__(self):
        return f"User: {self.email},  {self.type}"
    

class Course(db.Model):
    #variables
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(120), nullable=False)
    
    #relationships
    #many to many
    #users = db.relationship('User', secondary=user_courses, backref=db.backref('courses', lazy=True), lazy='dynamic')
    #users = db.relationship('User', secondary=user_courses, back_populates='courses', lazy=True)
    #one to many
    attendances = db.relationship('Attendance', backref='course', lazy=True)
    
    #methods
    def __repr__(self):
        return f"Course: {self.title},  {self.code}, {self.attendances}"
    
class Attendance(db.Model):
    #variables
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    code = db.Column(db.String(120), nullable=False)
    expires = db.Column(db.Boolean, nullable=False)
    expiretime = db.Column(db.DateTime, default=datetime.now(timezone.utc) + timedelta(minutes=10))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    
    #relationships
    #many to many
    #users = db.relationship('User', secondary=user_attendances, backref=db.backref('attendances', lazy=True), lazy='dynamic')
    #users = db.relationship('User', secondary=user_attendances, back_populates='attendances', lazy=True)
    
    #methods
    def __repr__(self):
        return f"Attendance: {self.date},  {self.code}, {self.expires}, {self.expiretime}, {self.course_id}"
    
