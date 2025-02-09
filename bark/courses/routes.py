from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from bark import db
from bark.models import Course
from bark.courses.forms import CreateCourseForm, JoinCourseForm

courses = Blueprint('courses', __name__)

#Display all of the user's courses
@courses.route('/courses')
@login_required
def my_courses():
    #get courses from current user
    courses = current_user.courses
    
    #load html
    return render_template('courses.html', title = 'Courses', courses = courses)

#Let professors add courses
@courses.route('/courses/create_course' , methods=['GET', 'POST'])
@login_required
def create_course():
    #check if user is a student
    if current_user.type == 'Student':
        return redirect(url_for('courses.my_courses'))
    
    #get CreateCourseForm
    form = CreateCourseForm()
    
    #submitting the form
    if form.validate_on_submit():
        course = Course(title = form.title.data, code = form.code.data)
        db.session.add(course)
        current_user.courses.append(course)
        db.session.commit()
        flash(f'New Course Created!', 'success')
        return redirect(url_for('courses.my_courses'))
    
    #load form
    return render_template('create_course.html', title = 'Create Course', form = form)
    
        
#Let students join courses
@courses.route('/courses/join_course', methods=['GET', 'POST'])
@login_required
def join_course():
    #check if user is a professor
    if current_user.type == 'Professor':
        return redirect(url_for('courses.my_courses'))
    
    #get JoinCourseForm
    form = JoinCourseForm()
    
    #submitting the form
    if form.validate_on_submit():
        course = Course.query.filter_by(code=form.code.data).first()
        if course:
            current_user.courses.append(course)
            db.session.commit()
            flash(f'New Course Joined!', 'success')
            return redirect(url_for('courses.my_courses'))
        else:
            flash(f'No course found!', 'failure')
    
    #load form
    return render_template('join_course.html', title = 'Join Course', form = form)

@courses.route('/courses/<int:course_id>')
@login_required
def view_course(course_id):
    return render_template('home.html', title = 'Join Course')