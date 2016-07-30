import os

DATABASE_ENGINE = 'django.db.backends.sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'openbudget.sqlite3')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

SECRET_KEY = 't1f^-^$a!)fbwl##x1v@n#*cqgy(&k85_grju+az2eb*m%a+v0'

DEBUG = True
ALLOWED_HOSTS = []
