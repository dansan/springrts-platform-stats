import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 's3cr3t'
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "stats.replays.springrts.com", "replays.springrts.com",
                 "replays-test.springrts.com", "replays.admin-box.com", "replays-test.admin-box.com",
                 "78.46.100.156"]
STATIC_ROOT = '/var/www/.../htdocs/static'

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
