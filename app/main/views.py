from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from . import main
from app import db
from app.models.course import Course
from app.models.user import User
from .forms import CourseForm


@main.app_errorhandler(404)
def page_not_found(e):
    """App-wide 404 error handling"""
    return render_template('errors/404.html'), 404


@main.app_errorhandler(500)
def page_not_found(e):
    """App-wide 500 error handling"""
    return render_template('errors/500.html'), 500


@main.route('/')
def index():
    """Route for landing page"""
    return render_template('index.html', title='EDU Landing page')


@main.route('/about')
def about():
    """Route for about page"""
    return render_template('about.html', title='About')


@main.route('/courses')
def courses():
    """Route for all courses availiable"""
    page = request.args.get('page', 1, type=int)
    pagination = Course.query.order_by(Course.date_created.desc()).paginate(
        page, per_page=8, error_out=False)
    courses = pagination.items
    return render_template('courses.html', title=f'Courses - Page{page}', 
                           courses=courses, pagination=pagination)


@main.route('/course/<int:course_id>')
def course(course_id: int):
    """Route for specific course page"""
    course = Course.query.get_or_404(course_id)
    return render_template('course_page.html', title=course.label, course=course)


@main.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    """Route for creating a course"""
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(label=form.label.data,
                        exam=form.exam.data,
                        level=form.level.data,
                        small_desc=form.small_desc.data,
                        author_id=current_user._get_current_object().id)
        db.session.add(course)
        db.session.commit()
        flash(f'{course.label.capitalize()} course has been added', 'success')
        return redirect(url_for('main.course', course_id=course.id))
    return render_template('create_course.html', 
                           title='Create New Course',
                           form=form)


@main.route('/course/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id: int):
    """Route for editing a course"""
    course = Course.query.get_or_404(course_id)
    if course.author == current_user._get_current_object():
        form = CourseForm(course=course)
        if form.validate_on_submit():
            course.label = form.label.data
            course.small_desc = form.small_desc.data
            course.exam = form.exam.data
            course.level = form.level.data
            db.session.add(course)
            db.session.commit()
            flash(f'Course {course} has been updated', 'success')
            return redirect(url_for('main.course', course_id=course.id))
        form.label.data = course.label
        form.small_desc.data = course.small_desc
        form.exam.data = course.exam
        form.level.data = course.level
        return render_template('edit_course.html', 
                               title=f'Edit {course.label} course', 
                               form=form,
                               course=course)
    else:
        flash('Denied: You cannot edit this course', 'danger')
    return redirect(url_for('main.dashboard'))


@main.route('/course/delete/<int:course_id>')
@login_required
def delete_course(course_id: int):
    """Route for deleting a course"""
    course = Course.query.get_or_404(course_id)
    if course.author == current_user._get_current_object(): 
        db.session.delete(course)
        db.session.commit()
        flash(f'Course {course} has been updated', 'success')
    else:
        flash('Denied: You cannot delete this course', 'danger')
    return redirect(url_for('main.dashboard'))


@main.route('/dashboard')
@login_required
def dashboard():
    """Route for user dashboard"""
    return render_template('dashboard.html', title='dashboard')


@main.route('/enroll/<int:course_id>')
@login_required
def enroll(course_id: int):
    """Enroll current user from a given course"""
    course = Course.query.get_or_404(course_id)
    if course.enroll(current_user._get_current_object()):
        flash(f'You have enrolled to the {course.label}', 'success')
    else: 
        flash(f'Denied: You seems have already enrolled to the {course.label}', 'danger')
    return redirect(url_for('main.dashboard'))


@main.route('/unenroll/<int:course_id>') 
@login_required
def unenroll(course_id: int):
    """Unenroll current user from a given course"""
    course = Course.query.get_or_404(course_id)
    if course.unenroll(current_user._get_current_object()):
        flash(f'You have unenrolled from the {course.label}', 'success')
    else: 
        flash(f'Denied: You seems have not enrolled to the {course.label}', 'danger')
    return redirect(url_for('main.dashboard'))


@main.route('/expell/<int:user_id>/from/<int:course_id>')
@login_required
def expell(user_id: int, course_id: int):
    """Expell the user from the given course"""
    user = User.query.get_or_404(user_id)
    course = Course.query.get_or_404(course_id)
    if course.author == current_user._get_current_object():
        course.users.remove(user)
        db.session.commit()
        flash(f'{user} has been expelled from the course!', 'success')
    else:
        flash('Denied: You are not the author of the course!', 'danger')
    return redirect(url_for('main.course', course_id=course.id))