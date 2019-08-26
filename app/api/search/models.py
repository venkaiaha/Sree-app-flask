from flask_restplus import Namespace

import app

class Search:
    api = Namespace('search', description='For search operations')