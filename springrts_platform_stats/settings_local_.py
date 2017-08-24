import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 's3cr3t'
DEBUG = False
ALLOWED_HOSTS = []

DATABASES = dict(
    default=dict(
        ENGINE='django.db.backends.mysql',
        NAME='xxx',
        USER='xxx',
        PASSWORD='xxx',
        HOST='127.0.0.1', PORT='3306'
    ),
    OPTIONS={'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}
)

ACCOUNT_SALT = b's3cr3t'
