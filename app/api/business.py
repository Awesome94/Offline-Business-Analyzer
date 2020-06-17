from flask import jsonify, request, current_app
from . import api
from ..models import Business

@api.route('/business/register', methods=['POST'])
def register_business():
    pass

@api.route('/business/<int:id>')
def get_business(id):
    """
    Get particular business with specified ID.
    """
    pass

@api.route('/businesses')
def get_all_businesses():
    """
    return all businesses
    """
    pass
