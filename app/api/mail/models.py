from flask_restplus import Namespace

import app

from flask_mail import Message

class Email:
    api = Namespace('mail', description='for sending emails')

    @classmethod
    def send_mail(cls, subject, _msg, _to, _from):
        ''' Send mails to customers '''
        try: 
            _to = _to if type(_to) == list else [_to]
            msg = Message(str(subject), sender = _from , recipients = _to )
            msg.body = str(_msg) + "\n\n" + "Regards" + "\n" + "Sri Accounting"
            app.App.mail.send(msg)
            info = "success"
        except Exception as e:
            info = str(e)
        return str(info)