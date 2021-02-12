import os


SECRET_KEY = os.environ.get('BBBS_SECRET_KEY', 'PLEASE CHANGE ME')
SECRET_SALT = os.environ.get('BBBS_SECRET_SALT', 'CHANGEME')
SQLALCHEMY_DATABASE_URI = os.environ.get('BBBS_DB_STRING', 'sqlite:///test.db')
