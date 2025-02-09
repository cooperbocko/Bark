from datetime import datetime, timezone
from flask import render_template, Blueprint
from bark import db, bcrypt
from bark.models import User, Course, Attendance

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home')

#Create Dummy Data
@main.route("/create")
def create():
    hashed_password = bcrypt.generate_password_hash("test").decode('utf-8')
    testuser = User(email = 'test@gmail.com', password = hashed_password, type = 'Student')
    testcourse = Course(title = 'test', code = 'test')
    testattendance = Attendance(date = datetime.now(timezone.utc), code = 'test', expires = False)
    db.session.add(testuser)
    db.session.add(testattendance)
    db.session.add(testcourse)
    
    testuser.courses.append(testcourse)
    testuser.attendances.append(testattendance)
    testcourse.attendances.append(testattendance)
    db.session.commit()
    
    users = User.query.all()
    courses = Course.query.all()
    attendances = Attendance.query.all()
    print(users)
    print(courses)
    print(attendances)
    
    print("attend users: ")
    print(testattendance.users)
    return render_template('create.html', posts = users)