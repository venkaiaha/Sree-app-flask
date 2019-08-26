""" Staff related operations """

import logging
from flask import request
from flask_restplus import Resource

from .models import Staff
import datetime, uuid
from app import get_jwt_identity, jwt_required

LOG = logging.getLogger(__name__)
api = Staff.api  
import dateutil.parser

@api.route('')
class StaffList(Resource):
    """Operations over staff list"""
    @classmethod
    @jwt_required
    @api.doc('list_staff')
    def get(cls):
        """ List all staff registered """
        user = get_jwt_identity()
        print(user)
        
        if user['role'] == 'administrator':
            msg = "Staff details viewed successfully"
            LOG.info('msg : %s',  msg)
            l=Staff.get_staffs()
            # print("rossum")
            # for i in l:
            #     i['created_at'] = dateutil.parser.parse(i['created_at']).isoformat()
            return l
        else:
            msg = 'Access Denied'
            LOG.info(msg + '{} {} tried to access Staff details. '.format(user['role'] , user['_id']))
            return {"msg": msg}

    @classmethod
    @api.expect(Staff.staff)
    @api.doc('create_staff')
    def post(cls):
        """ Register new staff """
        if Staff.check_staff(request.json):
            if Staff.add_staff(request.json):
                msg = 'Successful'
                LOG.info('Creating Staff record : %s', msg)
                return {"msg": msg}
            else:
                msg = 'Server error'
                LOG.info('msg : %s',  msg)
                return {"msg ": msg}
        else:
            msg = "Staff with employ_id already exit"
            LOG.info('msg : %s', msg)
            return {"msg": msg}


@api.route('/<_id>')
@api.param('_id', 'The staff identifier')
class StaffOper(Resource):
    """ Operations over staff """
    @classmethod
    @jwt_required
    @api.doc('view_staff_details')
    @api.marshal_with(Staff.staff)
    def get(cls, _id):
        """Fetch staff info given its identifier"""
        staff_obj = Staff.get_staff(_id)
        if staff_obj:
            msg = "Staff details successfully displayed"
            LOG.info('msg: %s',str(_id) + ' ' + msg)
            return staff_obj
        else: 
            msg = "Staff not found"
            LOG.info('msg: %s',str(_id) + ' ' + msg)
            return {'msg':msg}
@api.route('/staff_id')
class StaffDetails(Resource):
    """ Operations over staff """
    @classmethod
    @jwt_required
    @api.doc('view_staff_details')
    @api.marshal_with(Staff.staff)
    def get(cls):
        user = get_jwt_identity()
        _id=user['_id']
        """Fetch staff info given its identifier"""
        staff_obj = Staff.get_staff(_id)
        if staff_obj:
            msg = "Staff details successfully displayed"
            LOG.info('msg: %s',str(_id) + ' ' + msg)
            return staff_obj
        else: 
            msg = "Staff not found"
            LOG.info('msg: %s',str(_id) + ' ' + msg)
            return {'msg':msg}

    # @classmethod
    # @jwt_required
    # @api.doc('update_staff')
    # @api.expect(Staff.staff)
    # def put(cls, _id):
    #     """
    #     Updates a staff

    #     Use this method to change the details of a staff

    #     * Send a JSON object with the new details in the request body.

    #     ```
    #     {
    #       "key": "value"
    #     }
    #     ```

    #     * Specify the ID of the staff to modify in the request URL path
    #     """
    #     staff_obj = Staff.get_staff(_id)
    #     if staff_obj:
    #         Staff.update_staff(_id, request.json)
    #         LOG.info('Updated staff: %s', str(request.json))
    #         return None
    #     LOG.info('Staff not found: %s', str(_id))
    #     return None

    @classmethod
    @jwt_required
    @api.doc('delete_staff')
    def delete(cls, _id):
        """ Deletes a staff record given its identifier """
        staff_obj = Staff.get_staff(_id)
        if staff_obj:
            Staff.delete_staff(_id)
            msg = 'Deleted staff record'
            LOG.info('msg: %s', msg + ' ' + str(_id))
            return {'msg':msg}
        else:
            msg = 'Staff record not found'
            LOG.info('msg: %s', msg + ' ' + str(_id))
            return {'msg':msg} 