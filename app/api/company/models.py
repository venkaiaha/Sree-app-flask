"""  Company model  """

from flask import jsonify
from flask_restplus import Namespace, fields
import uuid, datetime
import app

class Company:
    api = Namespace('company', description='Operations related to companies')
    
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

    company = api.model('company',{
            'company_name':fields.String(required = True),  
            'owner_name':fields.String(required = True),
            'dob':fields.Date,
            'gender': fields.String(required = True),
            'nationality':fields.String(required = True),
            'abn':fields.String(required = True),
            'acn':fields.String(required = True),
            'tfn':fields.String(required = True),
            'business_name': fields.String(required = True),
            'business_address':fields.Nested(address,required = True),
            'registered_address': fields.Nested(address,required = True),
            'formation_date':fields.Date(required = True),
            'gst': fields.Boolean(required = True),
            'payer':fields.Boolean(required = True),
            'bas_period': fields.String(required = True),
            'phone':fields.Nested(phone,required = True),
            'email':fields.String(required = True),
            'preferred_bookkeeper': fields.String,
            'preferred_accountant': fields.String,
            '_id': fields.String,
            'created_at': fields.DateTime,
        })

    response = api.model('response',
                    {
                        'msg': fields.String    
                    })

    @classmethod
    def check_company(cls, data):
        """Check the existance of company """
        company = app.App.mongodb.db.company.find_one({'acn':data['acn']})
        if company == None:
            return True
        else:
            return False    
    
    @classmethod
    def create_company(cls, data):
        """Create a company"""
        data['_id'] = str(uuid.uuid4())
        data['created_at'] = datetime.datetime.utcnow()
        created = app.App.mongodb.db.company.insert_one(data)
        return created.acknowledged

    @classmethod
    def get_companies(cls):
        """List all company records"""
        cursor = app.App.mongodb.db.company.find({})
        resp = [doc for doc in cursor]
        return resp

    @classmethod
    def get_company(cls, _id):
        """View company details given by identifier"""
        return app.App.mongodb.db.company.find_one({'_id': _id})
    
    # @classmethod
    # def update_company(cls, _id, data):
    #     """Update a company name"""
    #     data = app.App.mongodb.db.company.find_one({'_id': _id})
    #     updated = app.App.mongodb.db.companyDateTime.update_one({'_id': _id}, \
    #         {'$set': {'name': data['name']}})
    #     return updated.acknowledged

    @classmethod
    def delete_company(cls, _id):
        """Delete a company"""
        return app.App.mongodb.db.company.delete_one({'_id': _id})

    
