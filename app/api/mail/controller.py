import app
import logging
from flask_restplus import Resource
from .models import Email
from app import jwt_required

LOG = logging.getLogger(__name__)

api = Email.api

@api.route('/send')
class SendMail(Resource):
    @classmethod
    @jwt_required
    @api.doc('send_emails')
    def get(cls, subject, _msg, _to, _from):
        """ For sending emails"""
        return app.App.mail.send_mail(subject, _msg, _to, _from)


