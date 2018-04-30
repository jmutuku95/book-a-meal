'''home bueprint'''
from flask_restful import Resource, Api
from flask import request

# local imports
from ..models.user import User
from ..models.admin import Admin
from .. import  DATABASE
from ..models import ItemAlreadyExists
from . import Blueprint

# Blueprint instance representing authentication blueprint


class UserRegistrationResource(Resource):
    '''Manage user registration when method is POST'''
    def post(self):
        '''handle the POST request to register users'''
        try:
            post_data = request.get_json(force=True)
            username = post_data.get('username')
            password = post_data.get('password')
            email = post_data.get('email')
            admin = post_data.get('admin', '')
            if admin:
                # register user using Admin model
                admin = Admin(
                    username=username, password=password, email=email,
                    admin=admin)
                try:
                    DATABASE.add(item=admin)
                except ItemAlreadyExists as error:
                    return {
                        'message': 'User already exists',
                        'error': str(error)
                    }, 202
                return {
                    'message': 'Admin registration succesful, proceed to login'
                }, 201

            # register normal user
            user = User(username=username, password=password, email=email)
            try:
                DATABASE.add(item=user)
            except Exception as error:
                return {
                    'message': 'User already exists',
                    'error': str(error)
                }, 202
            return {
                'message': 'User registration succesful, proceed to login'
                }, 201

        except Exception as error:
            return {
                'message': 'Encountered an error during registration',
                'Error': str(error)
            }, 400


class LoginResource(Resource):
    '''Manage user log in'''
    def post(self):
        '''Handles POST requests'''
        try:
            post_data = request.get_json(force=True)
            username = post_data.get('username', '')
            email = post_data.get('email', '')
            password = post_data.get('password')
            if username:
                user = DATABASE.get_user_by_username(username)
            elif email:
                user = DATABASE.get_user_by_email(email)
            else:
                user = None
            if user and User.validate_password(user, password):
                access_token = user.generate_token().decode()
                return {
                    'message': 'Successfully logged in',
                    'access_token': access_token
                }, 200
            return {
                'message': 'The username/email or password provided is not correct'}, 401
        except Exception as error:
            return {
                'message': 'Encountered an error during log in',
                'Error': str(error)
            }, 400

AUTH_API = Blueprint('app.views.authresource', __name__)
api = Api(AUTH_API)
api.add_resource(UserRegistrationResource, '/signup', endpoint='signup')
api.add_resource(LoginResource, '/signin', endpoint='signin')