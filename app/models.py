from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin

from app import db, token_gen
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
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_token(self, expiration=3600):
        import pdb
        pdb.set_trace()
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
        self.abreviation = abreviation
        self.company_address = company_address
        self.country = country
        self.countries = countries
        self.annual_sales_revenue = annual_sales_revenue
        self.accounting_software = accounting_software
        # self.user_id = user_id

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
    __tablename__ = 'transaction_details'

    class Name(IntEnum):
        order = 1
        order_payement = 2
        bill = 3
        bill_payement = 4

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.SmallInteger, default=Name.order.value, nullable=False)
    status = db.Column(db.String)
    due_date = db.Column(db.String)
    transaction_date = db.Column(db.String)
    customer_or_supplier = db.Column(db.String)
    item = db.Column(db.String)
    quantity = db.Column(db.String)
    unit_amount = db.Column(db.String)
    total_transaction_amount = db.Column(db.String)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))

    business = db.relationship(
        'Business',
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

    def get_all():
        return Business.query.all()

    def get_transaction(id):
        return Business.query.filter_by(id=id)

    def get_business_transactions(id):
        return Business.query.filter_by(business_id=id)

    def get_top_items_by_quantity(days=30):
        """
        Transaction should be an order. 
        and must have the highest  unit quantity
        """
        items = Transactions.query.filter(Transactions.transaction_date == date.today(
        ) - timedelta(days=days), Transactions.transaction == "order").all()

        return items

    def get_top_items_by_value(days=30):
        """
        Transaction should be an order. 
        and must have the highest  unit Amount
        """
        pass

    def get_incoming_amount(days=30):
        """
        get sum of all transaction from a given period of time 
        """
        pass

    def get_outgoing_amount(days=30):
        """
        get sum of all bill payement transactions for a given user
        """
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(id):
        transaction = Transactions.session.query.filter_by(id=id)
        db.session.delete(transaction)
        db.session.commit()
