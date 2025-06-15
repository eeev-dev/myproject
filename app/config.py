import os

class Config(object):
    APPNAME = 'app'
    ROOT = os.path.dirname(os.path.abspath(__file__))
    SERVER_PATH = os.path.join(ROOT, 'static', 'uploads')
    UPLOAD_PATH = os.path.join(ROOT, 'static', 'files')

    USER = os.environ.get('POSTGRES_USER', 'zebra')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'zebra')
    HOST = os.environ.get('POSTGRES_HOST', 'postgres')
    PORT = int(os.environ.get('POSTGRES_PORT', 5432))
    DB = os.environ.get('POSTGRES_DB', 'mydb')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = '6et82g89gb20g8gv9hv-2-2j293j'
    SQLALCHEMY_TRACK_MODIFICATIONS = True