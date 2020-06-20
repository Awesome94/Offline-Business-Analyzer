import os
from flask import Flask, flash, request, make_response, jsonify
from app import token_gen
from app.models import User
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = token_gen.loads(token)
            current_user = User.query.filter_by(id=data['id'])
        except:
            return jsonify({'message': 'Token is Invalid'}), 403
        return f(current_user, *args, **kwargs)
    return decorated


def response(status, message, status_code):
    return make_response(jsonify({
        'status': status,
        'message': message,
    })), status_code
