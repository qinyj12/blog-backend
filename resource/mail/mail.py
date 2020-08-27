from resource.login.login import api
from flask_mail import Mail, Message
from flask_restful import Api, Resource
from flask import Blueprint, current_app

app = Blueprint('mail', __name__, url_prefix = '/mail')
api = Api(app)
mail = Mail(current_app)

def send_mail(target_mail_address):
    msg = Message('hello', sender = '1562555013@qq.com', recipients = [target_mail_address])
    msg.html = '<p>testing</p>'
    mail.send(msg)