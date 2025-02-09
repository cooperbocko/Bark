from datetime import datetime, timedelta, timezone
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from bark import db
from bark.attendances.forms import CheckAttendanceForm, CreateAttendanceForm
from bark.models import Attendance, Course
from bark.courses.forms import CreateCourseForm, JoinCourseForm

attendances = Blueprint('attendances', __name__)

@attendances.route('/attendances/create/<int:course_id>',  methods=['GET', 'POST'])
@login_required
def create_attendance(course_id):
    #check if user is a student
    if current_user.type == 'Student':
        return redirect(url_for('courses.view_course', course_id = course_id))
    
    form = CreateAttendanceForm()
    
    if form.validate_on_submit():
        course = Course.query.filter_by(id=course_id).first()
        attendance = Attendance(date = datetime.now(timezone.utc), 
                                code = form.code.data, 
                                expires = form.expires.data, 
                                expiretime = datetime.now(timezone.utc) + timedelta(minutes = form.expirestime.data))
        db.session.add(attendance) 
        course.attendances.append(attendance)
        db.session.commit()
        flash(f'Created Attendance!', 'success')
        return redirect(url_for('courses.view_course', course_id = course_id))
    
    #load form
    return render_template('create_attendance.html', title = 'Create Attendance', form = form)

@attendances.route('/attendances/check/<int:course_id>', methods=['GET', 'POST'])
@login_required
def check_attendance(course_id):
    #check if user is a student
    if current_user.type == 'Professor':
        return redirect(url_for('courses.view_course', course_id = course_id))
    
    form = CheckAttendanceForm()
    
    if form.validate_on_submit():
        
        attendance = Attendance.query.filter_by(code=form.code.data).first()
        current_user.attendances.append(attendance)
        db.session.commit()
        flash(f'Created Attendance!', 'success')
        return redirect(url_for('courses.view_course', course_id = course_id))
    
    #load form
    return render_template('check_attendance.html', title = 'Check Attendance', form = form)