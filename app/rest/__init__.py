from flask import Blueprint
from flask_restful import Api


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


from . import users, courses
api.add_resource(users.UserResourse, '/users/', '/users/<int:id>/')
api.add_resource(courses.CourseResourse, 
                 '/courses/', 
                 '/courses/<int:id>/')
api.add_resource(courses.CourseEnrollResource, 
                 '/courses/<int:course_id>/enroll/<int:user_id>/',
                 '/courses/<int:course_id>/unenroll/<int:user_id>/')