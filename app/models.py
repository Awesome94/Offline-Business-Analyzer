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
    email = db.Column(db.String(120), index=True, unique=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def get_user(id):
        return User.query.filter_by(id=id)

    def get_all():
        return User.query.all()
    
    def delete_user(id):
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

    
    def __repr__(self):
        return '<User {}>'.format(self.firstname)


class Business(db.Model):
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    abreviation = db.Column(db.String)
    company_address = db.Column(db.String)
    country = db.Column(db.String)
    countries = db.Column(db.JSON, nullable=True)
    annual_sales_revenue = db.Column(db.String)
    Entity = db.Column(db.String)
    accounting_software = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship(
        'user',
        backref=db.backref('businesses', lazy='dynamic'),
        uselist=False
    )

    def __init__(self, **kwargs):
        self.name = name
        self.abreviation = abreviation
        self.company_address = company_address
        self.Country = Country
        self.countries = countries
        self.annual_sales_revenue = annual_sales_revenue
        self.accounting_software = accounting_software
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def get_all():
        return Business.query.all()
    
    def get_business(id):
        return Business.query.filter_by(id=id)

class Transactions(db.Model):
    __tablename__ = 'transaction_details'

    id = db.Column(db.Integer, primary_key=True)
    transaction = db.Column(db.String)
    status = db.Column(db.String)
    due_date = db.Column(db.String)
    customer_or_supplier = db.Column(db.String)
    item = db.Column(db.String)
    quantity = db.Column(db.String)
    unit_amount = db.Column(db.String)
    total_transaction_amount = db.Column(db.String)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))

    business = db.relationship(
        'business',
        backref=db.backref('transaction_details', lazy='dynamic'),
        uselist=False
    )

    def __init__(self, **kwargs):
        self.transaction = transaction 
        self.status = status
        self.due_date = due_date
        self.customer_or_supplier = customer_or_supplier
        self.item = item
        self.quantity = quantity
        self.unit_amount = unit_amount
        self.total_transaction_amount = total_transaction_amount
        self.business_id = business_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def get_all():
        return Business.query.all()
    
    def get_transaction(id):
        return Business.query.filter_by(id=id)
    
    def get_business_transactions(id):
        return Business.query.filter_by(business_id=id)