import app
import logging

from flask import jsonify
from flask_restplus import Resource
from .models import Search

LOG = logging.getLogger(__name__)
api = Search.api 

@api.route('/<c_type>/<tag>')
class Search(Resource):
    @api.doc("search")
    def get(self,c_type, tag):
        result = []
        if c_type == "company":
            search_resp = app.App.mongodb.db.company.find( { '$text': { '$search': tag } } ).sort('_id')
            
        elif c_type == "customer":
            search_resp = app.App.mongodb.db.customer.find( { '$text': { '$search': tag } } ).sort('_id')
        
        for doc in search_resp:
            result.append(doc)

        return jsonify(result)