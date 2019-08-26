"""  Customer model  """
from flask_restplus import Namespace, fields

import app

import datetime, uuid

class Customer:
    api = Namespace('customer', description='Operations related to customers')
    
    spouse = api.model('spouse', {
        'name': fields.String,
        'dob': fields.Date,
        'phone':fields.String,
        'email':fields.String,
        'tfn':fields.String,
    })

    address= api.model('address', {
        'line': fields.String,
        'street': fields.String,
        'city': fields.String,
        'state/territory': fields.String,
        'post_code': fields.String,
    })

    phone = api.model('phone',{
        'mobile': fields.String,
        'home': fields.String,
        'work':fields.String,
    })

    customer = api.model('customer',{
            'salutation': fields.String(required = True),
            'surname': fields.String,
            'name': fields.String(required = True),
            'dob': fields.Date(required = True),
            'gender': fields.String(required = True),
            'nationality': fields.String(required = True),
            "company_name": fields.String(required = True),
            'date_of_joining': fields.Date(required = True),
            'abn': fields.String(required = True),
            'acn': fields.String(required = True),
            'tfn': fields.String(required = True),
            'bas_period': fields.String(required = True),
            'preferred_bookkeeper': fields.String,
            'preferred_accountant': fields.String,
            'external_customer': fields.Boolean(required = True),
            'phone': fields.Nested(phone,required = True),
            'email': fields.String(required = True),
            'address':fields.Nested(address,required = True),
            'marital status': fields.String(required = True),
            'spouse': fields.Nested(spouse),
            'number_of_children': fields.Integer,
            '_id': fields.String,
            'created_at': fields.DateTime,
    })

    @classmethod
    def check_customer(cls, data):
        """Check the existance of a company """
        customer = app.App.mongodb.db.customer.find_one({'tfn':data['tfn']})
        if customer == None:
            return True
        else:
            return False
            
    @classmethod
    def create_customer(cls, data):
        """Create a customer"""
        data['_id']= str(uuid.uuid4())
        data['created_at'] = datetime.datetime.utcnow()
        created = app.App.mongodb.db.customer.insert_one(data)
        return created.acknowledged

    @classmethod
    def get_customer(cls, _id):
        """Get a customer"""
        return app.App.mongodb.db.customer.find_one({'_id': _id})
    
    @classmethod
    def get_customers(cls):
        """List all customers"""
        cursor = app.App.mongodb.db.customer.find({})
        resp = [doc for doc in cursor]
        return resp
        
    # @classmethod
    # def update_customer(cls, _id, data):
    #     """Update a customer"""
    #     app.App.mongodb.db.customer.update_one({'_id': _id}, {'$set': {'name': data['name']}})

    @classmethod
    def delete_customer(cls, _id):
        """Delete a customer"""
        return app.App.mongodb.db.customer.delete_one({'_id': _id})

    