# from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, make_response, request, current_app, url_for
from . import api
from app.models import User
from app.helpers import response, token_required
from app.model_schemas import user_schema
from .errors import unauthorized


@api.route('/')
def index():
    return response('success', "Welcome to offline Business application", 200)


@api.route('/register', methods=['POST'])
def register_user():
    user = User.query.filter_by(email=request.json.get('email')).first()
    if not user:
        try:
            post_data = request.json
            email = post_data.get("email")
            firstname = post_data.get("firstname")
            lastname = post_data.get("lastname")
            password = post_data.get("password")
            user = User(firstname, lastname, email, password)
            user.save()
            return response('success', 'account created successfully', 201)
        except Exception as e:
            result = {
                'message': str(e)
            }
            return make_response(jsonify(result)), 401
    else:
        return response('User already exists', 'Please Login', 202)


@api.route('/login', methods=['POST'])
def login_user():
    try:
        # Get the user object using their email
        user = User.query.filter_by(email=request.json.get('email')).first()
        password = request.json.get('password')
        # Try to authenticate the found user using their password
        if user and user.verify_password(password):
            # Generate the access token. This will be used as the authorization header
            access_token = user.generate_token(user.id)
            if access_token:
                response = {
                    'message': 'You logged in successfully.',
                    'access_token': access_token
                }

                return make_response(jsonify(response)), 200
        else:
            # User does not exist. so error message
            return unauthorized('Invalid email or password, Please try again')
    except Exception as e:
        # Create a response containing an string error message
        response = {
            'message': str(e)
        }
        # Return a server error using the HTTP Error Code 500 (Internal Server Error)
        return unauthorized('invalid username or password, Try again')


@api.route('/logout', methods=['POST'])
@token_required
def log_out(self):
    return "logout successful"


@api.route('/users/all')
def get_users():
    users = User.get_all()
    result = user_schema.dump(users)
    return jsonify(result)


@api.route('/users/<int:id>')
@token_required
def get_user(id):
    user = User.get_user(id)
    result = user_schema.dump(user)
    return jsonify(result)
