"""
settings.py

Configuration for Flask app

"""


class Config(object):
	# Set secret key to use session
	SECRET_KEY = "secret_keyasdlkfjakfj12314lkj12341"
	debug = False


class Production(Config):
	debug = True
	CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://yyko:dake-1004@localhost:3306/hygdb?charset=utf8&use_unicode=0"
	migration_directory = 'migrations'

