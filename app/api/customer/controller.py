""" Customer related operations """

import logging
from flask import request
from flask_restplus import Resource

from .models import Customer
from app import get_jwt_identity, jwt_required

LOG = logging.getLogger(__name__)

api = Customer.api 

@api.route('')
class CustomerList(Resource):
    """Operations over the customer list"""
    @classmethod
    @jwt_required
    @api.doc('list_customers')
    def get(cls):
        """List all customers registered"""
        LOG.info('msg : %s',"Customer records viewed successfully")
        l=Customer.get_customers()
        for i in l:
            i['created_at'] = i['created_at'].isoformat()
        return l

    @classmethod
    @jwt_required
    @api.expect(Customer.customer)
    @api.doc('create_customer')
    def post(cls):
        """ Register a new customer """
        if Customer.check_customer(request.json):
            if Customer.create_customer(request.json):
                msg = 'Customer record viewed successfully'
                LOG.info('msg : %s', msg)
                return {"msg": msg}
            else:
                msg = 'Server Error'
                LOG.info('msg : %s',  msg)
                return {"msg ": msg}
        else:
            msg = "Customer record already exit"
            LOG.info('msg : %s', msg)
            return {"msg": msg}


@api.route('/<_id>')
@api.param('_id', 'The customer identifier')
class CustomerOper(Resource):
    """Operations over a customer item"""
    @classmethod
    @jwt_required
    @api.doc('view_customer_details')
    def get(cls, _id):
        """Fetch customer details given its identifier"""
        customer_obj = Customer.get_customer(_id)
        if customer_obj:
            msg = "Customer details successfully displayed"
            LOG.info('msg: %s',msg)
            return customer_obj
        else: 
            msg = "Customer not found"
            LOG.info('msg: %s',str(_id) + ' ' + msg)
            return {'msg':msg}

    # @classmethod
    # @jwt_required
    # @api.doc('update_customer')
    # @api.expect(Customer.customer)
    # def put(cls, _id):
    #     """
    #     Updates a customer

    #     Use this method to change the details of a customer

    #     * Send a JSON object with the new details in the request body.

    #     ```
    #     {
    #       "key": "value"
    #     }
    #     ```

    #     * Specify the ID of the customer to modify in the request URL path
    #     """
    #     customer_obj = Customer.get_customer(_id)
    #     if customer_obj:
    #         Customer.update_customer(_id, request.json)
    #         LOG.info('Updated customer: %s', str(request.json))
    #         return None
    #     LOG.info('Customer not found: %s', str(_id))
    #     return None

    @classmethod
    @jwt_required
    @api.doc('delete_customer')
    @api.marshal_with(Customer.customer)
    @api.response(204, 'Customer successfully deleted.')
    def delete(cls, _id):
        """ Deletes a customer record given its identifier """
        customer_obj = Customer.get_customer(_id)
        if customer_obj:
            Customer.delete_customer(_id)
            msg = 'Deleted customer record'
            LOG.info('msg: %s', msg + ' ' + str(_id))
            return {'msg':msg}
        else:
            msg = 'Customer record not found'
            LOG.info('msg: %s', msg + ' ' + str(_id))
            return {'msg':msg}