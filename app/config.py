import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    APPNAME = 'app'
    ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_PATH = os.path.join(ROOT, 'static', 'files')            # шаблон рапорта
    INSTRUCTION_PATH = os.path.join(ROOT, 'instruction')           # шаг 4: текст инструкции и приложения к ней (не static — отдаётся только через API)
    APP_PATH = os.path.join(ROOT, 'static', 'app')                 # шаг 6: установочный файл приложения

    ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

    USER = os.environ.get('POSTGRES_USER')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    HOST = os.environ.get('POSTGRES_HOST')
    PORT = int(os.environ.get('POSTGRES_PORT') or 5432)
    DB = os.environ.get('POSTGRES_DB')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = '6et82g89gb20g8gv9hv-2-2j293j'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
