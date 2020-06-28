from app.models import User, Business, Transaction
from app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'lastname', 'firstname')

class BusinessSchema(ma.Schema):
    class Meta:
        fields = ('name','abreviation', 'company_address', 'country', 
        'countries', 'annual_sales_revenue', 'Entity', 
        'accounting_software', 'user_id')

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('name', 'status', 'due_date', 
        'customer_or_supplier', 'item', 'quantity', 
        'unit_amount', 'total_transaction_amount', 
        'business_id')

user_schema = UserSchema()
user_schema = UserSchema(many=True)

business_schema = BusinessSchema()
business_schema = BusinessSchema(many=True)

transactions_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
