from flask import jsonify, abort, request, current_app, make_response
from . import api
from ..models import Business, Transaction
from app.helpers import response, token_required
import os
import csv
from flask_login import current_user
from app.model_schemas import business_schema
from app import db
from werkzeug.utils import secure_filename

import pandas as pd

UPLOAD_DIRECTORY = "/Users/awesome/BusinessAnalyzer/oba-python-api/tests/"
HEADERS = ['Transaction', 'ID', 'Status', 'Transaction Date', 'Due Date', 'Customer or Supplier',
           'Item', 'Quantity', 'Unit Amount', 'Total Transaction Amount']

ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/business/register', methods=['POST'])
def register():
    business = None
    if not business:
        try:
            post_data = request.json
            name = post_data.get("name")
            abbreviation = post_data.get("abbreviation")
            company_address = post_data.get("company_address")
            country = post_data.get("country")
            countries = post_data.get("countries_of_operation")
            annual_sales_revenue = post_data.get("annual_sales_revenue")
            software = post_data.get("software")
            business = Business(name=name, abbreviation=abbreviation,
                                company_address=company_address, country=country,
                                countries=countries, annual_sales_revenue=annual_sales_revenue,
                                accounting_software=software
                                )
            business.save()
            return response('success', 'Business registered successfully', 201)
        except Exception as e:
            result = {
                'message': str(e)
            }
            return make_response(jsonify(result)), 401
    else:
        return response('business name already exists try a different name', 202)
    return "Business registered successfully"


@api.route('/business/<int:id>')
@token_required
def get_business(current_user, id):
    if not isinstance(id, int):
        return response('Bad request', 'Id must be integer', 500)
    if current_user.is_admin:
        result = Business.get_business(id)
    else:
        Business.get_current_user_business(id)
    return jsonify(business_schema.dump(result))


@api.route('/businesses/all')
@token_required
def get_all_businesses(current_user):
    """
    return all businesses if current user is admin, we return all businesses else we
    only return bussinesses that belong to the current user. 
    """
    if current_user.is_admin:
        result = Business.get_all()
    else:
        result = Business.get_current_all_user_business(current_user.id)
    return jsonify(business_schema.dump(result))


@api.route('/business/<int:id>/upload', methods=['POST'])
@token_required
def upload_transaction_details(current_user, id):
    if 'file' not in request.files:
        return response('bad request', 'No file in request', 400)

    file = request.files['file']

    if file.filename == '':
        return response('bad request', 'No file selected for uploading', 400)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        reader = csv.reader(file)
        data = pd.read_csv(file, usecols=HEADERS, delimiter=',')
        data['business_id'] = id
        data.rename(columns={
            'Transaction':'transaction', 
            'ID':'transaction_id', 
            'Status':'status', 
            'Transaction Date':'transaction_date', 
            'Due Date':'due_date',
            'Customer or Supplier':'customer_or_supplier',
            'Item':'item', 
            'Quantity':'quantity', 
            'Unit Amount':'unit_amount', 
            'Total Transaction Amount':'total_transaction_amount'
        })
        try:
            data.to_sql('transactions', con=db.engine, if_exists='append',
                        index=False, chunksize=1000)
        except Exception as e:
            result = {
                'message': str(e)
            }
            return make_response(jsonify(result)), 401
        return response('success', 'file uploaded successfully', 201)
    return response('bad request', 'Only .csv files allowed', 400)


@api.route('/business/amount/incoming/<int:days>')
@token_required
def show_incoming(days):
    result = Business.get_incoming_amount(days)
    return


api.route('/business/amount/outgoing/<int:days>')


@token_required
def show_outgoing(days):
    result = Business.get_outgoing_amount(days)
    return
