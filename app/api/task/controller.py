import logging
import os, datetime
from flask import request, jsonify
from flask_restplus import Resource

from .models import Task
from app.api.files.models import IO
from app.api.company.models import Company
from app.api.customer.models import Customer
from app.api.staff.models import Staff
from app import get_jwt_identity, jwt_required
import random

LOG = logging.getLogger(__name__)

api = Task.api  

@api.route('/allocate')
class TaskList(Resource):
    """Operations over task allocated list"""
    @classmethod
    @jwt_required
    @api.doc('list_task_allocated')
    @api.marshal_list_with(Task.task)
    def get(cls):
        """List all task initiated"""
        user = get_jwt_identity()
        if user['role'] in ['operator', 'administrator']:
            obj = Task.get_tasks()
            tasks = []
            for doc in obj:
                tasks.append(doc)
            return tasks
        else:
            obj = Task.get_pending_tasks()
            tasks = []
            for doc in obj:
                tasks.append(doc)
            return tasks

    @classmethod
    @jwt_required
    @api.expect(Task.task)
    @api.marshal_with(Task.status_resp)
    def post(cls):
        """  Creates a new task for allocation  """
        user = get_jwt_identity()
        data = request.json
        data['from_employ'] = user['_id']
        data['from_employ_role'] = user['role']
        data['to_employ_role'] = ''
        data['to_employ'] = ''
        data['status'] = 'bookkeeper_pending'
        data['note'] = 'task_initiated'
        data['active'] = True
        if user['role'] in ['operator','bookkeeper', 'administrator']:
            if Task.check_task(data):
                if Task.create(data):
                    Task.update_timetrack(data, data)
                    msg = "Successful"
                    LOG.info('Task Allocation : %s', msg)
                    return {"msg": msg}
                else:
                    msg = 'Server Error'
                    LOG.info('Message : %s',  msg)
                    return {"msg": msg}
            else:
                msg = "Claim is already under progress"
                LOG.info('Result : %s', msg)
                return {"msg": msg}
        else:
            msg = "Permission Denied"
            LOG.info('WARNING : %s', msg)
            return {"msg": msg}


@api.route('/<_id>')
@api.param('_id', 'The allocation identifier')
class TaskView(Resource):
    """Operations over task(s)"""
    @classmethod
    @jwt_required
    @api.doc('get_task')
    @api.marshal_with(Task.task)
    def get(cls, _id):
        """Fetch details of task given its identifier"""
        alloc_obj = Task.get_task(_id)
        if alloc_obj:
            LOG.info('Allocation not found: %s', str(_id))
            return None

@api.param('c_id', 'The claim identifier')
class ClaimView(Resource):
    @classmethod
    @jwt_required
    @api.doc('get_claim_status')
    def get(cls, c_id):
        return None

@api.route('/claim/status/<c_id>')
class StatusView(ClaimView):
    @jwt_required
    @api.doc('get_status_view')
    @api.marshal_with(Task.check_resp)
    def get(self, c_id):
        """Get status view of claim given its identifier"""
        claim_obj = list(Task.get_claim_status(c_id))
        l = []
        path = None
        for doc in claim_obj:
            path = IO.path_gen(doc['c_id'],doc['c_type'],doc['case']) # path_gen method is from files models
            try:
                # print(os.listdir(path))
                doc['docs'] = [item.rsplit('_', 1)[-1].rsplit('.', 1)[0] for item in os.listdir(path)]
            except:
                doc['docs'] = []
            l.append(doc)
        LOG.info('msg: %s', "document check successful")
        return  l   # path removed 

@api.route('/claim/track/<c_id>')
class TrackView(ClaimView):
    @jwt_required
    @api.doc('get_track_view')
    #@api.marshal_list_with(Task.status_track)
    def get(self, c_id):
        """Get track view of claim given its identifier """
        claim_obj = list(Task.get_claim_status(c_id))
        l = []
        for doc in claim_obj:
            path = IO.path_gen(doc['c_id'],doc['c_type'],doc['case']) # path_gen method is from files models
            try:
                doc['docs'] = [item.rsplit('_', 1)[-1].rsplit('.', 1)[0] for item in os.listdir(path)]
            except:
                doc['docs'] = []
            l.append(doc)
        LOG.info('msg: %s', "document check successful")
        return  jsonify([{"case":doc['case'],"status_track":doc['status_track']} for doc in l])

@api.route('/accept/<_id>')
class Accept(Resource):
    @classmethod
    @jwt_required
    @api.doc('accept_task')
    @api.marshal_with(Task.status_resp)
    def put(cls, _id):
        """To accept tasks allocated to the user"""
        user = get_jwt_identity()
        #body = request.json
        if user['role'] in ['bookkeeper', 'accountant']:
            master_data = Task.get_task(_id)
            
            if master_data != None:
                data = master_data['status_track'][-1]
                data['time_taken'] = 0
                data['status_time'] = datetime.datetime.utcnow().isoformat()

                if user['role'] == 'bookkeeper' and data['status'] in ['bookkeeper_pending','bookkeeper_hold','accountant_revert']:
                    c_id = master_data['c_id']
                    c_type = master_data['c_type']
                    c_name = master_data['c_name']
                    data['status'] = "bookkeeper_inreview"
                    data['note'] = "Accepted by bookkeeper"
                    data['from_employ_role'] = master_data['from_employ_role']
                    data['from_employ'] = master_data['from_employ']
                    data['to_employ_role'] = user['role'] 
                    data['to_employ'] = user['_id']                 

                elif user['role'] == 'accountant' and data['status'] in ['accountant_pending','accountant_hold']:
                    c_id = master_data['c_id']
                    c_type = master_data['c_type'] 
                    c_name = master_data['c_name'] 
                    data['status'] = "accountant_inreview"
                    data['from_employ_role'] = master_data['from_employ_role']
                    data['from_employ'] = master_data['from_employ']
                     
                else:
                    msg = "Out of scope error"
                    LOG.info('msg: %s', str(_id) + " " + msg)
                    return {"msg":msg}

                if Task.update_status(_id, data):
                    Task.update_timetrack(data, master_data)
                    msg = "Successful"
                    LOG.info('msg: %s', str(_id) + " " + msg)
                    return {"msg":msg}
                else:
                    msg = "server error"
                    LOG.info('msg: %s', str(_id) + " " + msg)
                    return {"msg":msg}
            else:
                msg = "Task doesn't exists"
                LOG.info('msg: %s', str(_id) + " " + msg)
                return {"msg":msg}
        else:
            msg = "unauthorized"
            LOG.info('msg: %s', str(_id) + " " + msg)
            return {"msg":msg}

@api.route('/submit')
class Submit(Resource):
    @classmethod
    @jwt_required
    @api.doc('submit_task')
    @api.expect(Task.submit)
    @api.marshal_with(Task.status_resp)
    def put(cls):
        """For Hold | Revert | Submit operations of allocated tasks"""
        user = get_jwt_identity()
        body = request.json
        _id = body['_id']
        body.pop('_id')
        if user['role'] in ['bookkeeper','accountant']:
            master_data = Task.get_task(_id)
            master_data['time_taken'] = body['time_taken'] ## if model|method modified do changes accordingly
            if master_data != None:
                data = master_data['status_track'][-1]
                data['status_time'] = datetime.datetime.utcnow().isoformat()
                data['note'] = body['note']
                data['from_employ_role'] = user['role']
                data['from_employ'] = user['_id']
                data['to_employ_role'] = ""
                data['to_employ'] = ""
                if user['role'] == 'bookkeeper' and data['status'] == 'bookkeeper_inreview':
                    if body['submit_flag'] == 'ok':
                        data['status'] = "accountant_pending"
                        data['to_employ_role'] = 'accountant'
                        data['time_taken'] = body['time_taken']
                        c_id = master_data['c_id']
                        c_type = master_data['c_type']
                        p_accountant = Task.preferred(c_id,c_type)
                        if p_accountant:
                            accountant = p_accountant
                        else:
                            accountant = random.choice(Task.auto_allot()) ## for auto allocation of accountant
                            data['to_employ'] = accountant['_id']    
                    elif body['submit_flag'] == 'hold':
                        data['status'] = "bookkeeper_hold"
                        data['to_employ_role'] = user['role']
                        data['to_employ'] = user['_id']
                        data['time_taken'] = body['time_taken']
                    else:
                        msg = "cannot be reverted"
                        LOG.info('msg: %s', str(_id) + " " + msg)
                        return {"msg":msg}

                elif user['role'] == 'accountant' and data['status'] == 'accountant_inreview':
                    if body['submit_flag'] == 'ok':
                        data['status'] = "finished"                 
                    elif body['submit_flag'] == 'hold':
                        data['status'] = "accountant_hold"
                        data['to_employ_role'] = user['role']
                        data['to_employ'] = user['_id']
                    else:
                        data['status'] = "accountant_revert"
                        data1 = master_data['status_track'][0]
                        data['to_employ_role'] = data1['to_employ_role']
                        data['to_employ'] = data1['to_employ']
                else:
                    msg = "Out of scope error"
                    LOG.info('msg: %s', str(_id) + " " + msg)
                    return {"msg":msg}
                
                if Task.update_status(_id, data):
                    Task.update_timetrack(data, master_data)
                    msg = "Successful"
                    LOG.info('msg: %s', str(_id) + " " + msg)

                    return {"msg":msg}
                else:
                    msg = "server error"
                    LOG.info('msg: %s', str(_id) + " " + msg)
                    return {"msg":msg}
            else:
                msg = "Task doesn't exists"
                LOG.info('msg: %s', str(_id) + " " + msg)
                return {"msg":msg}
        else:
            msg = "unauthorized"
            LOG.info('msg: %s', str(_id) + " " + msg)
            return {"msg":msg}
            
@api.route('/status')
class WorkStatus(Resource):
    @classmethod
    @jwt_required
    @api.doc('work_status')
    @api.marshal_list_with(Task.task, skip_none=True)
    def get(cls):
        """Show the work status of user after login"""
        user = get_jwt_identity()
        return Task.work_status(user['_id'])

@api.route('/status/staff')
class StaffStatus(Resource):
    @classmethod
    @jwt_required
    @api.doc('staff_status')
    def get(cls):
        """Show the work status of all users"""
        user =  get_jwt_identity()
        if user['role'] == 'operator':
            return jsonify(Task.staff_status())
        if user['role'] == 'administrator':
            status = jsonify(Task.staff_status(operator = True))
            return status
        