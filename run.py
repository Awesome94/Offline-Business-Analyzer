import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import sys
import click

from flask_migrate import Migrate, upgrade
from flask_script import Manager


from app import create_app, db
from app.models import User, Business

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Business=Business)

@app.cli.command()
def deploy():
    # migrate database to latest revision
    upgrade()