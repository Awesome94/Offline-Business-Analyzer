from werkzeug.security import generate_password_hash
from flask import jsonify, make_response, request, current_app, url_for
from . import api
from app.models import User
from app.helpers import response
from app.model_schemas import user_schema

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
    return "user registered successfully"


@api.route('/login', methods=['POST'])
def login_user():
    try:
        # Get the user object using their email
        user = User.query.filter_by(email=request.json.get('email')).first()
        # Try to authenticate the found user using their password
        if user and user.verify_password(request.json.get('password')):
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
            response = {
                'message': 'Invalid email or password, Please try again'
            }
            return make_response(jsonify(response)), 401
    except Exception as e:
        # Create a response containing an string error message
        response = {
            'message': str(e)
        }
        # Return a server error using the HTTP Error Code 500 (Internal Server Error)
        return make_response(jsonify(response)), 500


@api.route('/logout', methods=['POST'])
def log_out(self):
    return "logout successful"


@api.route('/users/all')
def get_users():
    users = User.query.all()
    return "this is awesoem"
    return jsonify(users.to_json())


@api.route('/users/<int:id>')
def get_user(id):
    import pdb; pdb.set_trace()
    user = User.query.filter_by(id=id)
    result = user_schema.dump(user)
    return jsonify(result)


@api.route('/users/<int:id>/business/all')
def get_all_businesses():
    """
    return all business that belong to a given user
    """


@api.route('/users/<int:id>/business/')
def get_business_from_id():
    """
    get business by id that belongs to a particular user
    """
    pass
