from flask import current_app, jsonify, abort
from flask_restful import Resource, reqparse
from ..service.service import UserService


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='Username')
parser.add_argument('email', type=str, help='Email')
parser.add_argument('password', type=str, help='User password')
parser.add_argument('first_name', type=str, help='First name')
parser.add_argument('second_name', type=str, help='Second name')
parser.add_argument('confirmed', type=bool, help='Email confirmation status')


class UserResourse(Resource):
    """UserResource"""

    def get(self, id: int=None):
        """
        UserResourse GET method. Retrieves all users found in the db, 
        unless the id path parameter is passed. In case the id is provided
        returns the user with the given id. In case the user with the id 
        is absent, returns the 404 response

        :param id: User ID to get, optional
        :returns: User, 200 HTTP status code
        """
        if not id:
            users = UserService.get_all()
            current_app.logger.debug('Retrieving all users')
            return jsonify({'users': [user.to_json() for user in users]})

        user = UserService.get_by_id(id)
        if user is None:
            abort(404)
        current_app.logger.debug(f'Retrieving user with id: {id}')
        return jsonify(user.to_json())

    def post(self):
        """
        UserResource POST method. Adds a new User to the database.
        Returns 400 HTTP status code in case the POST request misses 
        the following fields: 'username', 'email', 'password'

        :returns: 201 HTTP status code if success,
        otherwise - 400 HTTP status code
        """
        args = parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']
        if not (username and email and password):
            return {'error': 'bad request'}, 400

        if UserService.get_by_field(username=username):
            return {'error': 'bad request - such username is already taken'}, 400
        if UserService.get_by_field(email=email):
            return {'error': 'bad request - such email is already taken'}, 400

        user = UserService.create(username=username, 
                                  email=email, 
                                  password=password)
        current_app.logger.debug(f'New user has been created (id:{user.id}')
        return {'success': f'User (id:{user.id}) has been created successfully'}, 201
    
    def put(self, id: int=None):
        """
        UserResourse UPDATE method. Updates the User,
        and returns the User and 204 HTTP status code.
        Requires 'username', 'confirmed', 'first_name' and 'second_name' fileds.
        If the User is not found with the given id, 
        404 HTTP status code is returned
        If User id is not provided, 400 HTTP status code is returned
        In case the PUT request contains 'username' field that 
        is already taken by another user 400 HTTP status code is returned

        :param id: User ID
        :returns: 204 HTTP status code.
        If User is not found - 404 HTTP status code
        If User id is not provided - 400 HTTP status code
        In case the 'username' field in the PUT request contains
        data that is already taken by another User - 400 HTTP status code
        In case not all required fileds provided - 400 HTTP status code
        """
        if not id:
            return {'error': 'bad request - missing a User id'}, 400
        
        user = UserService.get_by_id(id)
        if user is None:
            abort(404)

        args = parser.parse_args()
        username = args['username']
        confirmed = args['confirmed']
        first_name = args['first_name']
        second_name = args['second_name']

        if not (username and confirmed and first_name and second_name):
            return {'error': 'bad request - not all required fields are provided'}, 400

        if username != user.username and \
            UserService.get_by_field(username=username):
            return {'error': 'bad request - such username is already taken'}, 400

        UserService.update(user,
                           username=username, 
                           confirmed=confirmed,
                           first_name=first_name,
                           second_name=second_name)
        current_app.logger.debug(f'User (id:{user.id}) has been updated ')
        return '', 204
    
    def delete(self, id: int=None):
        """
        User DELETE method. Removes the User from the database
        If the User is not found with the given id, 
        404 HTTP status code is returned
        If User id is not provided, 400 HTTP status code is returned

        :param id: User ID
        :returns: 204 HTTP status code
        If User is not found - 404 HTTP status code
        If User id is not provided - 400 HTTP status code
        """
        if not id:
            return {'error': 'bad request - missing a User id'}, 400
        
        user = UserService.get_by_id(id)
        if user is None:
            abort(404)

        UserService.delete(user)
        current_app.logger.debug(f'User (id:{user.id}) has been deleted')
        return '', 204
