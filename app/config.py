import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    APPNAME = 'app'
    ROOT = os.path.dirname(os.path.abspath(__file__))
    SERVER_PATH = os.path.join(ROOT, 'static', 'uploads')
    UPLOAD_PATH = os.path.join(ROOT, 'static', 'files')

    USER = os.environ.get('POSTGRES_USER')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    HOST = os.environ.get('POSTGRES_HOST')
    PORT = int(os.environ.get('POSTGRES_PORT'))
    DB = os.environ.get('POSTGRES_DB')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = '6et82g89gb20g8gv9hv-2-2j293j'
    SQLALCHEMY_TRACK_MODIFICATIONS = True