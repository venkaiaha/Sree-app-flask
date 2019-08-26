"""  Authentication related operations  """

import logging
import datetime
import app

from flask import request, jsonify
from flask_restplus import Resource

from .models import Auth
from app import jwt_required, set_access_cookies, set_refresh_cookies,\
    unset_jwt_cookies, jwt_refresh_token_required, get_jwt_identity, \
    create_access_token, get_raw_jwt

LOG = logging.getLogger(__name__)
api = Auth.api 
jwt = app.App.jwt

blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@api.route('/login')
class Login(Resource):
    """ Create session for user """
    @classmethod
    @api.doc("user_login")
    @api.expect(Auth.auth_body)
    def post(cls):
        """  Authorize users given by username and password  """
        data, role = Auth.authorise(request.json)
        if data['login'] == True:
            resp = Auth.create_token(data['_id'], role)
            resp.update(data)
            access_token = resp['access_token']
            refresh_token = resp['refresh_token']
            resp = jsonify(resp)
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            LOG.info('Logged in by %s', str(data['_id']+" as "+ data['role']))
            return resp
        else:
            resp ={}
            resp.update(data)
            return resp  

@api.route('/refresh')
class Refresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    @api.doc("refresh_access_token")
    def put(cls):
        """ To refresh the current user access token """
        current_user = get_jwt_identity()
        resp = Auth.create_token(current_user['_id'],current_user['role'], fresh = False)
        access_token = resp['access_token']
        resp = jsonify(resp)
        LOG.info('Access Token refreshed for %s', str(data['_id']))
        return jsonify({'access_token': access_token})

@api.route('/logout')
class Logout(Resource):
    @classmethod
    @api.doc("user_logout")
    @jwt_required
    def delete(cls):
        """To close session of the current user""" 
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        resp = jsonify({"msg": "Successfully logged out"})
        unset_jwt_cookies(resp)
        LOG.info('Logged out by %s', str(data['_id']+" as "+ data['role']))
        return resp
