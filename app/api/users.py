from werkzeug.security import generate_password_hash
from flask import jsonify, make_response, request, current_app, url_for
from . import api
from ..models import User
from app.helpers import response


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
            user = User(email=email, firstname=firstname,
                        lastname=lastname,
                        password=password
                        )
            user.save()
        except Exception as e:
            result = {
                'message': str(e)
            }
            return make_response(jsonify(result)), 401
    else:
        return response('User already exists', 'Please Login', 202)
    return "user registered successfully"


@api.route('/v1/login', methods=['POST'])
def login_user():
    try:
        # Get the user object using their email
        user = User.query.filter_by(email=request.json.get('email')).first()
        # Try to authenticate the found user using their password
        if user and user.password_is_valid(request.json.get('password')):
            # Generate the access token. This will be used as the authorization header
            access_token = user.generate_token(user.id)
            if access_token:
                response = {
                    'message': 'You logged in successfully.',
                    'access_token': access_token.decode()
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


@api.route('/v1/logout', methods=['POST'])
def log_out(self):
    return "logout successful"


@api.route('/users')
def get_users():
    users = User.query.all()
    return "this is awesoem"
    return jsonify(users.to_json())


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/business/all')
def get_all_businesses(id):
    """
    return all business that belong to a given user
    """


@api.route('/users/<int:id>/business/<int:id>')
def get_business_from_id(id):
    """
    get business by id that belongs to a particular user
    """
    pass
