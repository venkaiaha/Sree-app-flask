""" APP start module  """

import os
import logging
import pkgutil
import importlib

from flask import Flask
from flask.logging import default_handler
from flask_pymongo import PyMongo

from flask_cors import CORS
from config import CONFIG_NAME_MAPPER

from flask import Flask, jsonify, request
from flask_jwt import JWT, current_identity
from flask_jwt_extended import (
            JWTManager, jwt_required, create_access_token,
            jwt_refresh_token_required, create_refresh_token,
            get_jwt_identity, set_access_cookies,
            set_refresh_cookies, unset_jwt_cookies, get_raw_jwt)

from flask_bcrypt import Bcrypt
from flask_mail import Mail

# from flask_elasticsearch import Elasticsearch

LOG = logging.getLogger(__name__)

class App: 
    """ APP class   """
    @classmethod
    def __init__(cls):
        cls.mongodb = None
        cls.jwt = None
        cls.bcrypt = None
        cls.mail = None

    @classmethod
    def create_app(cls, flask_config_name):
        """ Entry point to the application  """
        app = Flask(__name__)
        app.config.from_object(CONFIG_NAME_MAPPER[flask_config_name])

        # setup for Elasticsearch
        # es = Elasticsearch()
        # app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        #                         if app.config['ELASTICSEARCH_URL'] else None


        # Configure root logger with flask app default handler and log level from config
        root = logging.getLogger()
        root.addHandler(default_handler)
        root.setLevel(app.config['LOG_LEVEL'])

        # Add log file handler
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(logging.Formatter( \
            '[ %(asctime)s ] - %(name)s - %(filename)s - %(process)s - %(threadName)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'))
        root.addHandler(file_handler)

        cls.mongodb = PyMongo(app)

        # Setup the Flask-JWT-Extended extension
        
        cls.jwt = JWTManager(app)
        
        cls.mail = Mail(app)

        cls.cors = CORS(app)

        # set up flask bcrypt

        cls.bcrypt = Bcrypt(app)

        # setup for static folder creation

        cls.PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        cls.ROOT_FOLDER = os.path.join(os.path.join(cls.PROJECT_ROOT,r'static'))
        cls.CUSTOMER_DIR = os.path.join(os.path.join(cls.ROOT_FOLDER, r'customer'))
        cls.COMPANY_DIR = os.path.join(os.path.join(cls.ROOT_FOLDER, r'company'))
        cls.STAFF_DIR = os.path.join(os.path.join(cls.ROOT_FOLDER, r'staff'))   
        cls.ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg']
        
        # default time setup 
        cls.REG_TIME = 10 # in mins
        

        # elastic search setup
        # cls.es = Elasticsearch()
                
        # Register all blueprints
        for module_loader, name, ispkg in pkgutil.iter_modules(path=__path__, prefix=__name__ + '.'):
            app.register_blueprint(importlib.import_module(name).create_module())

        LOG.info('Application started')

        return app