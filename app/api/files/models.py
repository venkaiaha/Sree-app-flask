from flask import request, send_from_directory
from flask_restplus import Namespace, fields

import app
import os, datetime

PATH = app.App.PROJECT_ROOT
ROOT_FOLDER = app.App.ROOT_FOLDER

class IO:
    api = Namespace('files', description='Operations related to companies')

    CUSTOMER_DIR = app.App.CUSTOMER_DIR
    COMPANY_DIR = app.App.COMPANY_DIR
    STAFF_DIR = app.App.STAFF_DIR
    ALLOWED_EXTENSIONS = app.App.ALLOWED_EXTENSIONS

    @classmethod
    def create(cls):
        try:        
            if not os.path.exists(ROOT_FOLDER):
                os.mkdir(ROOT_FOLDER)
            if not os.path.exists(cls.CUSTOMER_DIR):
                os.mkdir(os.path.join(os.path.join(ROOT_FOLDER,r"customer")))
            if not os.path.exists(cls.COMPANY_DIR):
                os.mkdir(os.path.join(os.path.join(ROOT_FOLDER,r"company"))) 
            if not os.path.exists(cls.STAFF_DIR):
                os.mkdir(os.path.join(os.path.join(ROOT_FOLDER,r"staff")))
            
            msg = "Static directory Integrity check completed succesfully"
            flag = True
        except Exception as e:
            msg = str(e)
            flag = False
        return msg, flag

    @classmethod        
    def create_company_dir(cls):
        companies = [doc['_id'] for doc in app.api.company.models.Company.get_companies()]
        try:    
            for doc in companies:
                root_path = cls.COMPANY_DIR
                company_fold = os.path.join(os.path.join(root_path,str(doc)))
                if not os.path.exists(company_fold):
                    os.mkdir(os.path.join(root_path,str(doc)))
            msg = "Company directory Integrity check completed succesfully"
            flag = True
        except Exception as e:
            msg = str(e)
            flag = False
        return msg, flag
    
    @classmethod    
    def create_customer_dir(cls):
        customers = [doc['_id'] for doc in app.api.customer.models.Customer.get_customers()]
        try:
            for doc in customers:
                root_path = cls.CUSTOMER_DIR
                customer_fold = os.path.join(os.path.join(root_path,str(doc)))
                if not os.path.exists(customer_fold):
                    os.mkdir(os.path.join(root_path,str(doc)))
            
            msg = "Customer directory Integrity check completed succesfully"
            flag = True
        except Exception as e:
            msg = str(e)
            flag = False
        return msg, flag
    
    @classmethod
    def create_staff_dir(cls):    
        staff = [doc['_id'] for doc in app.api.staff.models.Staff.get_staffs()]
        try:
            for doc in staff:
                root_path = cls.STAFF_DIR
                staff_fold = os.path.join(os.path.join(root_path,str(doc)))
                if not os.path.exists(staff_fold):
                    os.mkdir(os.path.join(root_path,str(doc)))
            
            msg = "Staff directory Integrity check completed succesfully"
            flag = True
        except Exception as e:
            msg = str(e)
            flag = False
        return msg, flag
    
    @classmethod
    def check_path(cls, path):
        if os.path.exists(path):
            return True
        else:
            return False

    @classmethod
    def create_path(cls,path):
        try:
            os.makedirs(path)
            return True
        except:
            return False

    @classmethod
    def allowed_file(cls, file):
            return '.' in file and file.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS
         

    @classmethod
    def upload(cls, filebuff, path, filename):
        if filebuff and cls.allowed_file(filebuff.filename):
            filebuff.save(os.path.join(path, filename))
            return "uploaded successfully"
        else:
            return "not in allowed extensions"

    @classmethod
    def path_gen(cls, c_id, c_type, case):
        path = None
        if c_type == 'company':
            path = os.path.join(cls.COMPANY_DIR, c_id, case)
        elif c_type == 'customer':
            path = os.path.join(cls.CUSTOMER_DIR, c_id, case)
        print('path_gen: ',path)
        return path

    @classmethod
    def get_files(cls, path, doc):
        return send_from_directory(path , doc, as_attachment=True) 



    