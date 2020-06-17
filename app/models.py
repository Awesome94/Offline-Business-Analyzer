from . import db
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    password = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')


class Business(db.Model):
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    abreviation = db.Column(db.String)
    company_address = db.Column(db.String)
    Country = db.Column(db.String)
    Countries_of_operation = db.Column(db.String)
    annual_sales_revenue = db.Column(db.String)
    Entity = db.Column(db.String)
    accounting_software = db.Column(db.String)

class Transactions(db.Model):
    __tablename__ = 'transaction_details'

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    transaction = db.Column(db.String)
    status = db.Column(db.String)
    due_date = db.Column(db.String)
    customer_or_supplier = db.Column(db.String)
    item = db.Column(db.String)
    quantity = db.Column(db.String)
    unit_amount = db.Column(db.String)
    total_transaction_amount = db.Column(db.String)
