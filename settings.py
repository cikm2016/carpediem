"""
settings.py

Configuration for Flask app

"""
import os
from datetime import timedelta


class Config(object):
	# Set secret key to use session
	SECRET_KEY = os.urandom(24)
	debug = False
	PERMANENT_SESSION_LIFETIME = timedelta(days=10)


class Production(Config):
	debug = True
	CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://yyko:dake-1004@localhost:3306/hygdb?charset=utf8&use_unicode=0"
	migration_directory = 'migrations'

