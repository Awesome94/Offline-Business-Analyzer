import os
import pandas as pd

from flask import jsonify, abort, request, current_app, make_response
from . import api
from ..models import Business, Transaction
from app.helpers import response, token_required
from flask_login import current_user
from app.model_schemas import business_schema
from app import db
from werkzeug.utils import secure_filename
from datetime import date, datetime, timedelta


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
    # if Transaction.get_title(file.filename):
    #     return response('Already exists', 'File with title %s has already been uploaded' % file.filename, 400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        reader = csv.reader(file)
        try:
            data = pd.read_csv(file, usecols=HEADERS, delimiter=',')
            data['business_id'] = id
            data['file_name'] = file.filename
            data['Due Date'] = pd.to_datetime(
                data['Due Date'], format="%m/%d/%y", infer_datetime_format=True)
            data['Transaction Date'] = pd.to_datetime(
                data['Transaction Date'], format="%m/%d/%y", infer_datetime_format=True)
            data.rename(columns={
                'Transaction': 'transaction',
                'ID': 'transaction_id',
                'Status': 'status',
                'Transaction Date': 'transaction_date',
                'Due Date': 'due_date',
                'Customer or Supplier': 'customer_or_supplier',
                'Item': 'item',
                'Quantity': 'quantity',
                'Unit Amount': 'unit_amount',
                'Total Transaction Amount': 'total_transaction_amount'
            }, inplace=True)
            data.to_sql('transactions', con=db.engine, if_exists='append',
                        index=False, chunksize=1000)
        except Exception as e:
            result = {
                'message': str(e)
            }
            return make_response(jsonify(result)), 401
        return response('success', 'file uploaded successfully', 201)
    return response('bad request', 'Only .csv files allowed', 400)


@api.route('/business/<int:id>/<filename>', methods=['DELETE'])
@token_required
def delete_uploaded_data(current_user, id, filename):
    try:
        if not current_user.is_admin:
            if not Business.query.filter_by(id=id).first().user_id == current_user.id:
                return response('Unauthorized', 'User does not have the rights to perform requested action', '401')
        Transaction.delete(filename, id)
        return response('Success', 'data deleted successfully', 200)
    except Exception as e:
        return {
            'message': str(e)
        }


@api.route('/business/<int:id>/uploads', methods=['GET'])
@token_required
def show_uploaded_files(current_user, id):
    file_names = []
    if not current_user.is_admin:
        if not Business.query.filter_by(id=id).first().user_id == current_user.id:
            return response('Unauthorized', 'User does not have the rights to perform requested action', '401')
    result = Transaction.get_business_transactions(id)
    for item in result:
        if item.file_name in file_names:
            continue
        file_names.append(item.file_name)
    return {
        'titles': file_names
    }


@api.route('/business/amount/incoming/<int:days>', methods=['GET'])
@token_required
def show_incoming(current_user, days):
    try:
        total_amount = Transaction.get_incoming_amount(days)
        return {
            'Incoming amount': total_amount
        }
    except Exception as e:
        return {
            'message': str(e)
        }


api.route('/business/amount/outgoing/<int:days>')
@token_required
def show_outgoing(days):
    try:
        total_amount = Transaction.get_outgoing_amount(days)
        return {
            'Incoming amount': total_amount
        }
    except Exception as e:
        return {
            'message': str(e)
        }
