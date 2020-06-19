from app.models import User, Business, Transactions
from app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'lastname', 'firstname')

class BusinessSchema(ma.Schema):
    class Meta:
        fields = ()

class TransactionsSchema(ma.Schema):
    class Meta:
        field = ()

user_schema = UserSchema()
user_schema = UserSchema(many=True)

business_schema = BusinessSchema()
business_schema = BusinessSchema(many=True)

transactions_schema = TransactionsSchema()
transactions_schema = TransactionsSchema(many=True)
