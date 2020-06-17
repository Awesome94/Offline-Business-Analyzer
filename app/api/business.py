from flask import jsonify, request, current_app, make_response
from . import api
from ..models import Business
from app.helpers import response


@api.route('/business/register', methods=['POST'])
def register():
    business = Business.query.filter_by(email=request.json.get('name')).first()
    if not business:
        try:
            post_data = request.json
            name = post_data.get("name")
            abbreviation = post_data.get("abbreviation")
            company_address = post_data.get("company_address")
            country = post_data.get("country")
            operations = post_data.get("countries_of_operation")
            annual_sales_revenue = post_data.get("annual_sales_revenue")
            software = post_data.get("software")
            business = Business(name=name, abbreviation=abbreviation,
                        company_address=company_address, country=country,
                        countries_of_operation=operations, annual_sales_revenue=annual_sales_revenue,
                        accounting_software=software
                        )
            business.save()
        except Exception as e:
            result = {
                'message': str(e)
            }
            return make_response(jsonify(result)), 401
    else:
        return response('business name already exists try a different name', 202)
    return "Business registered successfully"


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
