from werkzeug.security import generate_password_hash
from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/users')
def get_users():
    users = User.query.all()
    return "this is awesoem"
    return jsonify(users.to_json())