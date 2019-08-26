""" Staff model """

from flask import jsonify
from flask_restplus import Namespace, fields
import datetime, uuid
import app
import dateutil.parser


class Staff:
    api = Namespace('staff', description='Operations related to Staff')
    
    staff = api.model('staff',{
            'surname': fields.String(required = True),
            'name': fields.String(required = True),
            'role': fields.String(required = True),
            'employ_id': fields.String(required = True),
            'password': fields.String(required = True,min_length=6),  # pattern='^[a-z0-9-]+$'
            'phone': fields.String,
            'email': fields.String,
            'created_at': fields.DateTime,
            '_id': fields.String,     
        })

    @classmethod
    def check_staff(cls, data):
        """Check the existance of staff """
        user = app.App.mongodb.db.staff.find_one({"employ_id":data['employ_id']})
        if user == None:
            return True
        else:
            return False
    
    @classmethod
    def add_staff(cls, data):
        """Add new staff record"""
        data['password'] = app.App.bcrypt.generate_password_hash(data['password'])
        data['_id']= str(uuid.uuid4())
        data['created_at'] = datetime.datetime.utcnow()
        created = app.App.mongodb.db.staff.insert_one(data)
        return created.acknowledged
    
    @classmethod
    def get_staffs(cls):
        """List all staff records"""
        cursor = app.App.mongodb.db.staff.find()
        data = []
        for doc in cursor:
            doc['password'] = str(doc['password'])
            doc['created_at'] =doc['created_at'].isoformat()
            data.append(doc)
        return data

    @classmethod
    def get_staff(cls, _id):
        
        """View staff details given by identifier"""
        return app.App.mongodb.db.staff.find_one({'_id': _id})

    # @classmethod
    # def update_staff(cls, _id, data):
    #     """Update staff"""
    #     app.App.mongodb.db.staff.update_one({'_id': _id}, {'$set': {'employ_id': data['employ_id'],'password':data['password']}})

    @classmethod
    def delete_staff(cls, _id):
        """Delete staff record"""
        app.App.mongodb.db.staff.delete_one({'_id': _id})

    

