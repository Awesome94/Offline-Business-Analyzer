from flask import jsonify, abort, request, current_app, make_response
from . import api
from ..models import Business
from app.helpers import response, token_required
import os
import csv
from flask_login import current_user
from app.model_schemas import business_schema

UPLOAD_DIRECTORY = "/Users/awesome/BusinessAnalyzer/oba-python-api/tests/"
HEADERS = ['transaction', 'id', 'status', 'due date', 'customer or supplier',
           'item', 'quantity', 'unit amount', 'total transaction', 'amount']


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


@api.route('/business/upload/<filename>', methods=['POST'])
@token_required
def upload_transaction_details(filename):
    if "/" in filename:
        abort(400, "no subdirectories directories allowed")
    with open(os.path.join(UPLOAD_DIRECTORY, filename)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                for x in HEADERS:
                    if x.lower() not in row:
                        return response('Failed', 'missing required headers', 400)
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(
                    f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
    return response('success', 'file uploaded successfully', 201)


@api.route('/business/amount/incoming/<int:days>')
def show_incoming(days):
    pass


api.route('/business/amount/outgoing/<int:days>')
def show_outgoing(days):
    pass


# def show_outgoing(days):
#     result = Transaction.query.filter_by()
#     pass

# Order payememnt: receipt of payement from customer against the order
# Bill payement: payement of bill request going to supplier.
