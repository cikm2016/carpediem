"""
Initialize Flask app

"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask_oauth import OAuth
from app import settings

app = Flask(__name__)
app.config.from_object('app.settings.Production')

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

import controllers, models
