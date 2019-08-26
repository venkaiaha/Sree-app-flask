
from flask_restplus import Namespace, fields
import  datetime, uuid
import app
from app.api.staff.models import Staff
from app.api.company.models import Company
from app.api.customer.models import Customer

class Task:
    api = Namespace('task', description='Operation related to tasks')

    status_track = api.model('status_track',
                    {
                        'status':fields.String,
                        'status_time': fields.DateTime,
                        'from_employ_role':fields.String,
                        'from_employ':fields.String,
                        'to_employ_role':fields.String,
                        'to_employ': fields.String,
                        'note': fields.String,
                        'time_taken':fields.Integer,
                    })
                    
    task = api.inherit('task', status_track,
                    {
                        '_id': fields.String,
                        'created_at': fields.DateTime,
                        'c_id': fields.String(required = True),
                        'c_type': fields.String(required = True),
                        'c_name': fields.String(required = True),
                        'case': fields.String(required=True),
                        'active': fields.Boolean,
                    })

    check_resp = api.inherit('check_resp',task, {'docs': fields.List(fields.String)})
    
    status_resp = api.model('status_resp',
                    {
                        'msg': fields.String
                    })
    
    submit = api.model('submit',
                    {
                        '_id':fields.String(required=True),
                        'note':fields.String(required=True),
                        'submit_flag':fields.String(required=True),
                        'time_taken':fields.Integer(required=True),
                    })

    @classmethod
    def check_task(cls,data):
        """Check the existance of a task """
        user = app.App.mongodb.db.task.find_one({'c_id':data['c_id'],'case':data['case']})
        if user == None:
            return True
        else:
            return False
      
    @classmethod
    def create(cls,data):
        """ Create task """
        data['_id'] = str(uuid.uuid4())
        data['created_at'] = data['status_time'] =  datetime.datetime.utcnow().isoformat()
        data['time_taken'] = app.App.REG_TIME      # time taken for registration should be fixed later 
        data['status_track'] = [{    
                            "status": data['status'],
                            "status_time": data['status_time'],
                            "from_employ_role": data['from_employ_role'],
                            "from_employ": data['from_employ'],
                            "to_employ_role": data['to_employ_role'],
                            "to_employ": data['to_employ'],
                            'note': data['note'],
                            'time_taken': data['time_taken']
                        }] 

        inserted = app.App.mongodb.db.task.insert_one(data)
        return inserted.acknowledged

    @classmethod
    def get_tasks(cls):
        """ List all tasks initiated """
        return app.App.mongodb.db.task.find({"active":True})
        
    @classmethod
    def get_task(cls, _id):
        """ View task given by task identifier  """
        return app.App.mongodb.db.task.find_one({'_id': _id})
    
    @classmethod
    def get_pending_tasks(cls):
        """ List all tasks unaccepted """
        return app.App.mongodb.db.task.find({"active":True,"status" : "bookkeeper_pending"})


    @classmethod
    def get_claim_status(cls, c_id):
        """ View tasks given by its claim identifier """   
        return list(app.App.mongodb.db.task.find({'c_id': c_id, 'active': True}))
    
    @classmethod
    def update_status(cls, task_id, data):
        """ Update status of the task given by its task identifier """
        updated = app.App.mongodb.db.task.update_one({'_id': task_id}, {"$set":data,"$push":{"status_track":data}})
        return updated.acknowledged

    @classmethod
    def update_timetrack(cls, data, master_data):
        """ For time record of submitted work"""
        staff = {}
        staff['s_id'] = data['from_employ']
        staff['s_role'] = data['from_employ_role']
        staff['status'] = data['status']
        staff['submitted_at'] = data['status_time']
        staff['note'] = data['note']
        staff['c_id'] = master_data['c_id']
        staff['c_name'] = master_data['c_name']
        staff['c_type'] = master_data['c_type']
        staff['case'] = master_data['case']
        staff['time_taken'] = data['time_taken']
        app.App.mongodb.db.timetrack.insert_one(staff)

    @classmethod
    def work_status(cls, _id):
        """Work status of user"""
        return list(app.App.mongodb.db.task.find({'to_employ':_id, 'active':True}))

    @classmethod
    def staff_status(cls,operator=False):
        """ Gives the work status of employees """
        check_list = ['bookkeeper',"accountant"]
        if operator == True:
            check_list.append('operator')
        staff = {}
        for doc in Staff.get_staffs():
            if doc['role'] in check_list:
                doc = {doc['_id']:{"_id":doc['_id'],"name":doc['name'],"role":doc['role'], 'type':[], 'task_id_list':[], 'task_list':[], 'count': 0 }}
                staff.update(doc)

        tasks = {}
        for doc in cls.get_tasks():
            doc.pop('status_track')
            if doc['to_employ'] not in tasks:
                tasks[doc['to_employ']] = {'type':[doc['c_type']], 'task_id_list': [doc['_id']],'task_list': [doc['c_name']], 'count': 1}
            else:
                tasks[doc['to_employ']]['task_id_list'].append(doc['_id'])
                tasks[doc['to_employ']]['task_list'].append(doc['c_name'])
                tasks[doc['to_employ']]['type'].append(doc['c_type'])
                tasks[doc['to_employ']]['count'] += 1
        
        for k, v in tasks.items():
            if k in staff:
                staff[k].update(v)
        return staff       
            
    @classmethod
    def preferred(cls, c_id, c_type):
        """ To get preferred staff for particular claim """
        if c_type == 'company':
            p_accountant = Company.get_company(c_id)
            return p_accountant['preferred_accountant'] if p_accountant != None else None
        elif c_type =='customer':
            p_accountant = Customer.get_customer(c_id)
            return p_accountant['preferred_accountant'] if p_accountant != None else None

    @classmethod
    def auto_allot(cls):
        staff = cls.staff_status()
        l = []
        for k, v in staff.items():
            if v['role'] == 'accountant':
                l.append(v)        
        d = []  
        for doc in l:
            if doc['count'] == min(l, key=lambda x:x['count'])['count']:
                d.append(doc)
        return d   