import logging
import app
import os
import base64
from flask import request, jsonify
from flask_restplus import Resource

from .models import IO

LOG = logging.getLogger(__name__)
api = IO.api

@api.route('/structure')
class Create(Resource):
    @classmethod
    def get(cls):
        """ Create folder structure for document uploads"""   
        main_msg, main_flag = IO.create()
        LOG.info('msg: %s', main_msg)
        if main_flag:
            msg, flag = IO.create_company_dir()
            LOG.info('msg: %s', msg)
            msg, flag = IO.create_customer_dir()
            LOG.info('msg: %s', msg)
            msg, flag = IO.create_staff_dir()
            LOG.info('msg: %s', msg)
            return {'msg': "Successful"}
        else: 
            LOG.info('msg: %s', main_msg)
            return {'msg': main_msg}

@api.route('/upload')
class Upload(Resource):
    @classmethod
    def post(cls):
        """ For documents upload after registration"""  
        # try:
        c_id = request.form['c_id']
        c_type = request.form['c_type']
        case = request.form['case']
        files = [item for item in request.form['files'].split(",")]
        files = list(set(files))
        path = IO.path_gen(c_id, c_type, case)
        if not IO.check_path(path):
            IO.create_path(path)
        msg = ""
        for f in files:
            filebuff = request.files.get(f,None)
            if filebuff:
                filename = case + '_' + f + '.' + str(filebuff.filename.rsplit('.')[-1]).lower()
                res  = IO.upload(filebuff, path, filename)
            else:
                res = "This file not exist"
            msg += f + " ==> " + res + ", "
        LOG.info('msg: %s', msg)
        return {'msg': msg}
        # except Exception as e:
        #     msg = str(e)
        #     LOG.info('msg: %s', msg)
        #     return {'msg': msg}

@api.route('/view')
class View(Resource):
    @classmethod
    def post(cls):
        """ For viewing documents uploaded for a particular case identified by claim identifier """
        c_id = request.json['c_id']
        c_type = request.json['c_type']
        case = request.json['case']
        path = IO.path_gen(c_id, c_type, case)
        if IO.check_path(path):
            files =  [item.rsplit('_', 1)[-1] for item in os.listdir(path)]
            fi = []
            names = []
            if len(files) == 0:
                return jsonify({'msg':'No documents uploaded', 'flag': False})
            else:
                for filename in files:
                    filepath = os.path.join(path, case + "_" + filename)
                    with open(filepath, 'rb') as f:
                        a = base64.b64encode(f.read())
                    a = bytes.decode(a)
                    fi.append(a)
                    names.append(filename)
                return jsonify({"names":names, "encoding": "base64", "files": fi, 'msg': 'success', 'flag': True})
        

     

            
