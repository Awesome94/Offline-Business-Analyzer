from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin

from app import db, token_gen, bcrypt
import hashlib
from datetime import date, datetime, timedelta
from enum import IntEnum, Enum


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode()

    def verify_password(self, password):
        status =  bcrypt.check_password_hash(self.password, password)
        return status

    def generate_token(self, expiration=3600):
        token = token_gen.dumps({'confirm': self.id}).decode('utf-8')
        return token

    def get_user(id):
        return User.query.filter_by(id=id)

    def get_all():
        return User.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(id):
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.firstname)


class Business(db.Model):
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    abbreviation = db.Column(db.String)
    company_address = db.Column(db.String)
    country = db.Column(db.String)
    countries = db.Column(db.JSON, nullable=True)
    annual_sales_revenue = db.Column(db.String)
    Entity = db.Column(db.String)
    accounting_software = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship(
        'User',
        backref=db.backref('businesses', lazy='dynamic'),
        uselist=False
    )

    def __init__(self, name, abbreviation, company_address, country, countries, annual_sales_revenue, accounting_software):
        self.name = name
        self.abbreviation = abbreviation
        self.company_address = company_address
        self.country = country
        self.countries = countries
        self.annual_sales_revenue = annual_sales_revenue
        self.accounting_software = accounting_software
        self.user_id = user_id

    def get_all():
        return Business.query.all()

    def get_business(id):
        return Business.query.filter_by(id=id)

    def get_current_user_business(id):
        return Business.query.filter_by(user_id=id).first()

    def get_current_all_user_business(id):
        return Business.query.filter_by(user_id=id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(id):
        business = Business.query.filter_by(id=id).first()
        db.session.delete(business)
        db.session.commit()


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer)
    transaction = db.Column(db.String)
    status = db.Column(db.String)
    due_date = db.Column(db.DateTime)
    transaction_date = db.Column(db.DateTime)
    customer_or_supplier = db.Column(db.String)
    item = db.Column(db.String)
    quantity = db.Column(db.String)
    unit_amount = db.Column(db.String)
    total_transaction_amount = db.Column(db.String)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    file_name = db.Column(db.String)

    business = db.relationship(
        'Business',
        backref=db.backref('transactions', lazy='dynamic', cascade="all,delete"),
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

    def get_all():
        return Business.query.all()

    def get_transaction(id):
        return Business.query.filter_by(id=id)

    def get_business_transactions(id):
        return Transaction.query.filter_by(business_id=id).all()

    def get_top_items_by_quantity(id, limit=5):
        items = Transaction.query.filter_by(business_id=id).order_by(Transaction.quantity.desc()).limit(limit).all()
        return items

    def get_top_items_by_value(id, limit=5):
        items = Transaction.query.filter_by(business_id=id).order_by(Transaction.unit_amount.desc()).limit(limit).all()
        return items
 
    def get_incoming_amount(id, days=30):
        total_sum = []
        items = Transaction.query.filter(Transaction.business_id==id, Transaction.transaction_date >= date.today(
        ) - timedelta(days=days), Transaction.transaction == 'Order').order_by(Transaction.total_transaction_amount.desc()).all()
        for item in items:
            total_sum.append(float(item.total_transaction_amount))
        return sum(total_sum)

    def get_outgoing_amount(id, days=30):
        total_sum = []
        items = Transaction.query.filter(Transaction.transaction_date >= date.today(
        ) - timedelta(days=days), Transaction.business_id==id, Transaction.transaction == 'Bill').order_by(Transaction.total_transaction_amount.desc()).all()
        for item in items:
            total_sum.append(float(item.total_transaction_amount))
        return sum(total_sum)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(filename, id):
        Transaction.query.filter_by(
            file_name=filename, business_id=id).delete()
        db.session.commit()
        
    def get_title(filename):
        return Transaction.query.filter(Transaction.file_name == filename).all()
