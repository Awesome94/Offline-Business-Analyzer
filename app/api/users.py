from werkzeug.security import generate_password_hash
from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User

@api.route('/', methods=['GET'])
def index():
    return "this is awesomer than you"

@api.route('/users')
def get_users():
    users = User.query.all()
    return "this is awesoem"
    return jsonify(users.to_json())

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/register', methods=['POST'])
def register_user():
    return "user registered successfully"

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