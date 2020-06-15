from flask import Flask, request, g, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
api = Blueprint('api', __name__)

login = LoginManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/5432/obadb'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import routes, models
