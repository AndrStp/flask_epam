from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort, request, \
    jsonify, current_app
from flask_login import login_required, current_user
from . import main_bp
from ..models.course import Course
from ..service.service import UserService, CourseService
from .forms import CourseForm, CourseSearchForm


@main_bp.app_errorhandler(404)
def not_found(e):
    """App-wide 404 error handling.
    Returns json response if request is in json format.
    Otherwise renders errors/404.html template"""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'not found'}), 404
    return render_template('errors/404.html'), 404


@main_bp.app_errorhandler(500)
def internal_error(e):
    """App-wide 500 error handling.
    Returns json response if request is in json format.
    Otherwise renders errors/500.html template"""
    current_app.logger.debug('An internal server error occured')
    if request.path.startswith('/api/'):
        return jsonify({'error': 'not allowed'}), 500
    return render_template('errors/500.html'), 500


@main_bp.route('/')
def index():
    """Route for landing page"""
    return render_template('index.html', title='EDU Landing page')


@main_bp.route('/about')
def about():
    """Route for about page"""
    return render_template('about.html', title='About')


@main_bp.route('/courses')
def courses():
    """Route for all courses availiable"""
    page = request.args.get('page', 1, type=int)
    pagination = Course.query.order_by(Course.date_created.desc()).paginate(
        page, per_page=8, error_out=False)
    courses = pagination.items
    return render_template('courses.html', title=f'Courses - Page{page}',
                           courses=courses, pagination=pagination)


@main_bp.route('/courses/search', methods=['GET', 'POST'])
def search_courses():
    """Route for course search form and results"""
    form = CourseSearchForm()
    if form.validate_on_submit():
        filters = {k: v for k, v in form.data.items()
                   if v and k not in ['username', 'submit', 'csrf_token',
                                      'start_date', 'end_date']}

        if filters.get('exam') == 'true':
            filters['exam'] = True 
        elif filters.get('exam') == 'false':
            filters['exam'] = False
        
        if form.username.data:
            user = UserService.get_by_field(username=form.username.data)
            if not user:
                flash(f'There is no user with username: {form.username.data}',
                      'danger')
                return redirect(url_for('main.courses'))
            filters['author_id'] = user.id
        
        start_date = form.start_date.data
        end_date = form.end_date.data
        if start_date or end_date:
            # fill in missing dates
            if not end_date:
                end_date = datetime.date(datetime.utcnow())
            if not start_date:
                start_date = datetime(2021, 12, 1).date()
            courses = (Course.query.filter_by(**filters)
                                .filter(Course.date_created.between(start_date,
                                                                    end_date))
                                .order_by(Course.date_created.desc()).all())
        else:
            courses = (Course.query.filter_by(**filters)
                                .order_by(Course.date_created.desc()).all())
        if courses:
            flash(f'{len(courses)} courses has been found', 'success')
        else:
            flash('No courses has been found', 'danger')
        return render_template('courses.html', title='Filtered Courses',
                               courses=courses)
    return render_template('search_courses.html', title='Search for a course',
                           form=form)


@main_bp.route('/course/<int:course_id>')
def course(course_id: int):
    """Route for specific course page"""
    course = CourseService.get_by_id(course_id)
    if not course:
        abort(404)

    course_users = course.users
    return render_template('course_page.html',
                           title=course.label,
                           course=course,
                           course_users=course_users)


@main_bp.route('/course/create', methods=['GET', 'POST'])
@login_required
def create_course():
    """Route for creating a course"""
    form = CourseForm(course=None)
    if form.validate_on_submit():
        course = CourseService.create(label=form.label.data,
                                      exam=form.exam.data,
                                      level=form.level.data,
                                      small_desc=form.small_desc.data,
                                      author_id=current_user._get_current_object().id)
        flash(f'{course.label.capitalize()} course has been added', 'success')
        current_app.logger.debug(f'User: \'{current_user.username}\' '\
            f'has created the Course: \'{course.label}\'')
        return redirect(url_for('main.course', course_id=course.id))
    return render_template('create_course.html', 
                           title='Create New Course',
                           form=form)


@main_bp.route('/course/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id: int):
    """Route for editing a course"""
    course = CourseService.get_by_id(course_id)
    if not course:
        abort(404)

    if course.author == current_user._get_current_object():
        form = CourseForm(course=course)
        if form.validate_on_submit():
            CourseService.update(course,
                                 label=form.label.data,
                                 small_desc=form.small_desc.data,
                                 exam=form.exam.data,
                                 level=form.level.data,)
            flash(f'Course {course} has been updated', 'success')
            current_app.logger.debug(f'User: \'{current_user.username}\' '\
                f'has editied the Course: \'{course.label}\'')
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


@main_bp.route('/course/delete/<int:course_id>')
@login_required
def delete_course(course_id: int):
    """Route for deleting a course"""
    course = CourseService.get_by_id(course_id)
    if not course:
        abort(404)

    if course.author == current_user._get_current_object():
        CourseService.delete(course)
        flash(f'Course {course} has been updated', 'success')
        current_app.logger.debug(f'User: \'{current_user.username}\' '\
            f'has deleted the Course: \'{course.label}\'')
    else:
        flash('Denied: You cannot delete this course', 'danger')
    return redirect(url_for('main.dashboard'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Route for user dashboard"""
    courses_author = current_user.courses_author
    courses_user = current_user.courses_student.all()
    return render_template('dashboard.html',
                           title='dashboard',
                           courses_author=courses_author,
                           courses_user=courses_user)


@main_bp.route('/enroll/<int:course_id>')
@login_required
def enroll(course_id: int):
    """Enroll current user from a given course"""
    course = CourseService.get_by_id(course_id)
    if not course:
        abort(404)

    if course.enroll(current_user._get_current_object()):
        flash(f'You have enrolled to the {course.label}', 'success')
        current_app.logger.debug(f'User: \'{current_user.username}\' '\
            f'has enrolled to the Course: \'{course.label}\'')
    else: 
        flash(f'Denied: You seems have already enrolled to the {course.label}', 'danger')
    return redirect(url_for('main.dashboard'))


@main_bp.route('/unenroll/<int:course_id>') 
@login_required
def unenroll(course_id: int):
    """Unenroll current user from a given course"""
    course = CourseService.get_by_id(course_id)
    if not course:
        abort(404)
    if course.unenroll(current_user._get_current_object()):
        flash(f'You have unenrolled from the {course.label}', 'success')
        current_app.logger.debug(f'User: \'{current_user.username}\' '\
            f'has unenrolled from the Course: \'{course.label}\'')
    else: 
        flash(f'Denied: You seems have not enrolled to the {course.label}', 'danger')
    return redirect(url_for('main.dashboard'))


@main_bp.route('/expell/<int:user_id>/from/<int:course_id>')
@login_required
def expell(user_id: int, course_id: int):
    """Expell the user from the given course"""
    user = UserService.get_by_id(user_id)
    course = CourseService.get_by_id(course_id)
    if not (course and user): 
        abort(404)
    if course.author == current_user._get_current_object():
        if course.expell(user):
            flash(f'{user} has been expelled from the course!', 'success')
            current_app.logger.debug(f'User: \'{current_user.username}\' '\
                f'has been expelled from the Course: \'{course.label}\'')
        else:
            flash(f'{user} is not enrolled to the {course}', 'danger')
    else:
        flash('Denied: You are not the author of the course!', 'danger')
    return redirect(url_for('main.course', course_id=course.id))
