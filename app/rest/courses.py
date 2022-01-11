from flask import current_app, jsonify, abort, request
from flask_restful import Resource, reqparse
from ..service.service import CourseService, UserService
from .utils import time_validation


parser = reqparse.RequestParser()
parser.add_argument('label', type=str, help='Course label')
parser.add_argument('exam', type=bool, help='Exam required?')
parser.add_argument('level', type=str, choices=['I', 'R', 'A'],
                    help='Course difficulty level. Chose one of the following:'\
                         '"I" - Introductory, "R" - Regular, "A" - Advanced')
parser.add_argument('small_desc', type=str, help='Small description. Max 250 chars')
parser.add_argument('created_from', type=str, help='Courses created from X date. ' \
                                           'Format "%Y-%m-%d"')
parser.add_argument('created_to', type=str, help='Courses created to X date. ' \
                                         'Format "%Y-%m-%d"')


class CourseResourse(Resource):
    """CourseResourse"""

    def get(self, id: int=None):
        """
        CourseResourse GET method. Retrieves all courses found in the db, 
        unless the 'id' path parameter is passed. Given the 'id' param
        the course with the given id is returned. 
        In case the course with the id is absent, returns the 404 response.
        If the 'id' param is missing but within the GET request
        'from' or 'to' queries are present, returns the list of courses
        created from 'from' to 'to' dates. Format: "%Y-%m-%d".

        :param id: Course ID to get, optional
        :returns: Course, 200 HTTP status code
        In case the 'id' of non-existent User is given,
        return error message and 404 HTTP status code
        In case either: 1) 'from' or 'to' are provided 
        in incorrect format, or 2) both are incorrect
        error message and 400 HTTP status are returned
        """
        if not id:
            args = parser.parse_args()
            date_from = args.get('created_from')
            date_to = args.get('created_to')
            
            if date_from is None and date_to is None:
                courses = CourseService.get_all()
                current_app.logger.debug('Retrieving all courses')
                return jsonify({'courses': [course.to_json() for course in courses]})

            date_from, date_to = time_validation(date_from, date_to)
            if not (date_from and date_to):
                current_app.logger.debug('Invalid datetime')
                return {'error': 'invalid datetime format'}, 400

            courses = CourseService.get_all_by_date(date_from, date_to)
            current_app.logger.debug('Retrieving all courses from ' \
                                        f'{str(date_from)} to {str(date_to)}')
            return jsonify({'courses': [course.to_json() for course in courses]})

        course = CourseService.get_by_id(id)
        if course is None:
            abort(404)
        current_app.logger.debug(f'Retrieving course with id: {id}')
        return jsonify(course.to_json())

    def post(self, id: int=None):
        """
        CourseResource POST method. Adds a new Course to the database.
        Requires id of the User (author). Returns 201 HTTP status code if success.
        Returns 400 HTTP status code in case the POST request misses 
        the following fields: 'label', 'exam', 'level', 'small_desc'.

        :param id: User ID of the course creator
        :returns: 201 HTTP status code if success.
        otherwise - 400 HTTP status code
        """
        if not id:
            return {'error': 'id is not given'}, 400

        user = UserService.get_by_id(id)
        if not user:
            return {'error': 'user with such id does not exist'}, 400

        args = parser.parse_args()
        label = args['label']
        exam = args['exam']
        level = args['level']
        small_desc = args['small_desc']

        if not (label and level and small_desc):
            return {'error': 'bad request - not all required fields are provided'}, 400

        if CourseService.get_course_by_field(label=label):
            return {'error': 'bad request - the course with such label already exists'}, 400

        course = CourseService.create(label=label, 
                                      level=level,
                                      exam=exam,
                                      small_desc=small_desc,
                                      author_id=id)
        current_app.logger.debug(f'New course (id:{course.id}) has been ' \
            f'created by User (id:{id}')
        return {'success': f'Course (id:{course.id}) has been created successfully'}, 201
    
    def put(self, id: int=None):
        """
        CourseResourse UPDATE method. Updates the Course with course_id,
        and returns 204 HTTP status code if successfully updated
        If the Course is not found with the given course_id, 
        404 HTTP status code is returned
        If course_id is not provided, 400 HTTP status code is returned
        In case the PUT request contains 'label' field 
        that is already taken by another Course, 400 HTTP status code is returned

        :param id: Course ID
        :returns: 204 HTTP status code.
        If Course is not found - 404 HTTP status code
        If Course id is not provided - 400 HTTP status code
        In case the 'label' field in the PUT request contains data that 
        is already taken by another Course - 400 HTTP status code
        """
        if not id:
            return {'error': 'id is not given'}, 400

        course = CourseService.get_by_id(id)
        if not course:
            return {'error': 'course with such id does not exist'}, 400

        args = parser.parse_args()
        label = args['label']
        exam = course.exam if args['exam'] is None else args['exam']
        level = args['level']
        small_desc = args['small_desc']

        if not (label and level and small_desc):
            return {'error': 'bad request - not all required fields are provided'}, 400

        if label != course.label \
                    and CourseService.get_course_by_field(label=label):
            return {'error': 'bad request - the course with such label already exists'}, 400

        CourseService.update(course,
                             label=label, 
                             level=level,
                             exam=exam,
                             small_desc=small_desc)
        current_app.logger.debug(f'Course (id:{course.id}) has been' \
            ' updated successfully')
        return '', 204
    
    def delete(self, id: int=None):
        """
        Course DELETE method. Removes the Course from the database
        If the Course is not found with the given id, 
        404 HTTP status code is returned
        If Course id is not provided, 400 HTTP status code is returned

        :param id: Course ID
        :returns: 204 HTTP status code
        If Course is not found - 404 HTTP status code
        If Course id is not provided - 400 HTTP status code
        """
        if not id:
            return {'error': 'bad request - course id is not provided'}, 400
        
        course = CourseService.get_by_id(id)
        if course is None:
            abort(404)
        
        CourseService.delete(course)
        current_app.logger.debug(f'Course (id:{course.id}) has been deleted')
        return '', 204
    

class CourseEnrollResource(Resource):
    """
    CourseResource for enrollment / unenrollment

    Support PUT request for the following endpoints:
    /course/<int:course_id>/enroll/<int:user_id>
    /course/<int:course_id>/unenroll/<int:user_id>
    """

    def put(self, course_id: int, user_id: int):
        """CourseResourse UPDATE method. Enrolls or Unerolls the User with
        user_id from the Course with course_id, and 
        returns 204 HTTP status code if successfully updated.
        If either the Course or User is not found with the given 
        course_id or user_id 404 HTTP status code is returned
        If either course_id or user_id is not provided, 
        400 HTTP status code is returned
        In case the User is already enrolled to the Course and
        PUT enroll request is sent - 400 HTTP status code is returned.
        The same logic applies to unenroll PUT request for not enrolled one.

        :param course_id: Course ID
        :param user_id: User ID
        :returns: 204 HTTP status code.
        If Course or User is not found - 404 HTTP status code
        If course_id or user_id is not provided - 404 HTTP status code
        In case the User is already enrolled to the Course and
        PUT enroll request is sent - 400 HTTP status code is returned.
        The same logic applies to unenroll PUT request for not enrolled one.
        """

        course = CourseService.get_by_id(course_id)
        user = UserService.get_by_id(user_id)

        if not (course and user):
            return {'error': 'either course or user does not exist or none exists'}, 404

        request_args = request.path.strip('/').split('/')
        method = request_args[4]
        if method == 'enroll':
            if course.is_enrolled(user):
                return {'error': f'User (id:{user.id} is already enrolled'}, 400

            course.enroll(user)
            current_app.logger.debug(f'User (id:{user.id}) has successfully ' \
                f'enrolled to the Course (id:{course.id})')
            return '', 204

        if method == 'unenroll':
            if not course.is_enrolled(user):
                return {'error': f'User (id:{user.id}) is not enrolled'}, 400
            
            course.unenroll(user)
            current_app.logger.debug(f'User (id:{user.id}) has successfully ' \
                f'unenrolled from the Course (id:{course.id})')
            return '', 204
