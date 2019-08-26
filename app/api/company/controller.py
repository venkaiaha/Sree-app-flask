""" Company related operations """

import logging
from flask import request
from flask_restplus import Resource

from .models import Company
from app import get_jwt_identity, jwt_required


LOG = logging.getLogger(__name__)
api = Company.api  

@api.route('')
class CompanyList(Resource):
    """Operations over company list"""
    @classmethod
    @api.doc('list_companies')
    @jwt_required
    def get(cls):
        """ List all companies registered """
        LOG.info('msg : %s', "Company records viewed successfully.")
        l=Company.get_companies()
        for i in l:
            i['created_at'] = i['created_at'].isoformat()
        return l

    @classmethod
    @api.expect(Company.company)
    @api.doc('create_company')
    def post(cls):
        """  Register new company """
        if Company.check_company(request.json):
            if Company.create_company(request.json):
                msg = "Company record created successfully"
                LOG.info('msg : %s', msg) 
                return {"msg": msg}
            else:
                msg = 'Server error'
                LOG.info('msg : %s',  msg)
                return {"msg ": msg}
        else:
            msg = "Company record already exit"
            LOG.info('msg : %s', msg)
            return {"msg": msg}
        
@api.route('/<_id>')
@api.param('_id', 'The company identifier')
class CompanyOper(Resource):
    """ Operations over company """
    @classmethod
    @jwt_required
    @api.doc('view_company_details')
    def get(cls, _id):
        """Fetch company info given its identifier"""
        company_obj = Company.get_company(_id)
        if company_obj:
            msg = "Company record viewed successfully"
            LOG.info('msg: %s',str(_id) + ' ' + msg)
            return company_obj
        else: 
            msg = "Company not found"
            LOG.info('msg: %s',str(_id) + ' ' + msg)
            return {'msg':msg}

    # @classmethod
    # @jwt_required
    # @api.doc('update_company')
    # @api.expect(Company.company)
    # def put(cls, _id):
    #     """
    #     Updates company details

    #     Use this method to change the details of existing compnay

    #     * Send a JSON object with the new details in the request body.

    #     ```
    #     {
    #       "key": "value"
    #     }
    #     ```

    #     * Specify the ID of the company to modify in the request URL path
    #     """
    #     user = get_jwt_identity()
    #     _id = user['_id']
    #     role = user['role']
    #     if role in ['operator','bookkeeper', 'admin']:
    #         if Company.check_company(request.json):
    #             company_obj = Company.get_company(_id)
    #             if company_obj:
    #                 Company.update_company(_id, request.json)
    #                 msg = 'Updated company'
    #                 LOG.info('msg: %s', msg + " by " + str(_id))
    #                 return {'msg':msg}
    #             else:
    #                 msg = "Company not updated"
    #                 LOG.info('msg: %s', msg)
    #                 return {'msg':msg}
    #         else:
    #             msg = "Compaany not exit"
    #             LOG.info('Result : %s', msg)
    #             return {"msg": msg}
    #     else:
    #         msg = "Permission Denied"
    #         LOG.info('WARNING : %s', msg)
    #         return {"msg": msg}   
            
    @classmethod
    @jwt_required
    @api.doc('delete_company')
    def delete(cls, _id):
        """ Deletes a company record given its identifier """
        company_obj = Company.get_company(_id)
        if company_obj:
            Company.delete_company(_id)
            msg = 'Deleted company record'
            LOG.info('msg: %s', msg + ' ' + str(_id))
            return {'msg':msg}
        else:
            msg = 'Company record not found'
            LOG.info('msg: %s', msg + ' ' + str(_id))
            return {'msg':msg}