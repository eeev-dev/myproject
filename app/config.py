import os

class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/uploads/'
    SERVER_PATH = ROOT + UPLOAD_PATH

    USER = os.environ.get('POSTGRES_USER', 'zebra')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'zebra')
    HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    PORT = int(os.environ.get('POSTGRES_PORT', 5432))
    DB = os.environ.get('POSTGRES_DB', 'mydb')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = '6et82g89gb20g8gv9hv-2-2j293j'
    SQLALCHEMY_TRACK_MODIFICATIONS = True