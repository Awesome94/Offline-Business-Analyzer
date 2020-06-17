import os 
from flask import Flask, flash, request, make_response, jsonify

def response(status, message, status_code):
    return make_response(jsonify({
        'status': status,
        'message': message,
    })), status_code