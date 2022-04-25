import os
import json


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    FLASK_APP = 'teleraan-ocr'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    SECRET_KEY = '&#zw1ysGmyOMYHNQ5^smr&1U#99YuN&3pM^G3wxfsjSUe6#BZCuBBjRKKssmQznt'
    ENV = os.environ.get('ENV', 'development')
    DEBUG = os.environ.get('DEBUG', False)
    TESTING = os.environ.get('TESTING', False)
    LANG = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    APP_TIMEZONE = os.environ.get('APP_TIMEZONE', "Asia/Shanghai")
    # 限制大小
    MAX_CONTENT_LENGTH = 1024 * 1024

    # 容器内的日志配置
    APP_LOG_FILENAME = os.environ.get('APP_LOG_FILENAME', '/tmp/app.log')
    APP_LOG_MODE = os.environ.get('APP_LOG_MODE', 'a')
    APP_LOG_MAX_BYTES = int(os.environ.get('APP_LOG_MAX_BYTES', 52428800))
    APP_LOG_BACKUP_COUNT = int(os.environ.get('APP_LOG_BACKUP_COUNT', 3))
    APP_LOG_DELAY = bool(int(os.environ.get('APP_LOG_DELAY', 1)))

    DATABASE_HOST = os.environ.get('DATABASE_HOST', '127.0.0.1')
    DATABASE_USER = os.environ.get('DATABASE_USER', 'teletraan')
    DATABASE_PORT = int(os.environ.get('DATABASE_PORT', 3306))
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'Teletraan-OCR@1024')
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'teletraan')

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', True)

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return "mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}" \
               "@{DATABASE_HOST}:{DATABASE_PORT}" \
               "/{DATABASE_NAME}?charset=UTF8MB4&autocommit=true" \
            .format(DATABASE_USER=self.DATABASE_USER,
                    DATABASE_PASSWORD=self.DATABASE_PASSWORD,
                    DATABASE_HOST=self.DATABASE_HOST,
                    DATABASE_PORT=self.DATABASE_PORT,
                    DATABASE_NAME=self.DATABASE_NAME)

    def to_json(self):
        data = {
            'FLASK_ENV': self.FLASK_ENV,
            'FLASK_APP': self.FLASK_APP,
            'SECRET_KEY': self.SECRET_KEY,
            'DATABASE_HOST': self.DATABASE_HOST,
            'DATABASE_PORT': self.DATABASE_PORT,
            'DATABASE_USER': self.DATABASE_USER,
            'DATABASE_PASSWORD': self.DATABASE_PASSWORD,
            'DATABASE_NAME': self.DATABASE_NAME,
            'APP_LOG_FILENAME': self.APP_LOG_FILENAME,
            'SQLALCHEMY_DATABASE_URI': self.SQLALCHEMY_DATABASE_URI
        }

        return data

    def init_app(self, app):

        if not getattr(self, 'FLASK_ENV'):
            raise EnvironmentError('请初始化系统环境变量. source env.sh')

        app.config.from_object(self)

        if getattr(self, 'DEBUG'):
            print(json.dumps(self.to_json(), default=str, indent=4))
