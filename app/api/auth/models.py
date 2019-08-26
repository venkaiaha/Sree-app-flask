from flask_restplus import Namespace, fields
import app
import datetime
from app import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies


class Auth:
    api = Namespace('auth', description='For authentication')
    
    auth_body = api.model('auth_body',{
            'username':fields.String(required = True),
            'password':fields.String(required = True),            
        })

    auth_response = api.model('auth_response',{
            'msg':fields.String,
            'access_token':fields.String,  
            'refresh_token':fields.String, 
            'name':fields.String,
            'role':fields.String,
            '_id':fields.String,
            'login': fields.Boolean
        })


    @classmethod
    def get_user(cls, employ_id):
        """add new user"""
        user = app.App.mongodb.db.staff.find_one({"employ_id":employ_id})
        return user

    @classmethod
    def authorise(cls, data):
        """add new user"""
        user = cls.get_user(data['username'])
        if user != None:
            _id = user['_id']     
            name  = user['name']
            role = user['role']
            password = user['password']
            if app.App.bcrypt.check_password_hash(password, data["password"]):
                resp = {'msg': "login success", "_id":_id, "name":name, "role":role, "login":True }
                return resp, role
            else:
                resp = {'msg': "username/password does not match", 'login':False}
                return resp, None
        else:
            resp = {'msg': "username/password does not match", 'login':False}
            return resp, None
            

    @classmethod
    def create_token(cls, _id, role, fresh = True):
        "create access and refresh token for user"
        access_token = create_access_token({ \
                                        "_id":_id, "role":role}, fresh=datetime. \
                                        datetime.utcnow(), expires_delta \
                                        =datetime.timedelta(minutes=120))
        if fresh == True:
            refresh_token = create_refresh_token({ \
                                "_id":_id, "role":role}, \
                                expires_delta=datetime.\
                                timedelta(minutes=180))
        else:
            refresh_token = None
        return {"access_token":access_token, "refresh_token":refresh_token}
        

    

    
       



    
    

