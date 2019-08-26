import logging
import datetime
import os

class BaseConfig:
    SECRET_KEY = '@rossum'
    JWT_SECRET_KEY = SECRET_KEY
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=120)
    JWT_COOKIE_CSRF_PROTECT = False
    # JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    DEBUG = False
    
    # Flask settings
    FLASK_DEBUG = True

    # Flask-Restplus and SWAGGER settings
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_DOC_EXPANSION = 'list'
    
    # Logger settings
    LOG_LEVEL = logging.INFO

    # ELASTICSEARCH settings
    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # MAIL CONFIGURATION settings

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'info@rossum.io'
    MAIL_PASSWORD = 'python@777'
    MAIL_DEFAULT_SENDER = 'info@rossum.io'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # MongoDB settings
    MONGO_URI = 'mongodb://localhost:27017/sri-dev'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    # MongoDB settings
    MONGO_URI = 'mongodb://localhost:27017/sri-test'


class ProductionConfig(BaseConfig):
    DEBUG = False

    # Flask settings
    FLASK_DEBUG = False

    # MongoDB settings
    MONGO_URI = 'mongodb://localhost:27017/sri-prod'


CONFIG_NAME_MAPPER = {
                    'development': DevelopmentConfig,
                    'testing': TestingConfig,
                    'production': ProductionConfig,
                    'default': DevelopmentConfig
                    }