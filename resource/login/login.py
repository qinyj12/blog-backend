#导入依赖包
from flask import Blueprint, render_template, make_response, redirect, g, url_for, current_app, copy_current_request_context
from flask_restful import Api, Resource, reqparse
from database import database_session, database_tables
from ..token import token_create
from ..token import token_verify
from ..token import token_ensure
from ..mail import mail
import threading

app = Blueprint('login', __name__, url_prefix = '/login')
api = Api(app)
parser = reqparse.RequestParser()

database_session = database_session.session

database_user = database_tables.User
database_mail_code = database_tables.Mail_Code

class Login(Resource):
    def post(self):
        # 从'form'中拿到提交的数据
        parser.add_argument('username', type = str, location = 'form')
        parser.add_argument('password', type = str, location = 'form')
        args = parser.parse_args()
        arg_username = args['username']
        arg_password = args['password']

        # 去数据库判断用户名和密码是否一致，如果通过
        if database_session.query(database_user).filter_by(name = arg_username, password = arg_password).scalar():
            database_session.close()
            # 生成token
            user_token = token_create.create_token(arg_username)
            # 因为要redirect的同时设置cookie，用make_response更轻松
            resp = make_response(redirect(url_for('.login')))
            resp.set_cookie('Token', user_token, 10)
            return resp
        # 如果用户名和密码不一致
        else:
            return '用户名和密码不一致', 401

    # 快使用装饰器，嚯嚯哈嘿
    @token_ensure.ensure_exist
    # 如果cookie里没有保存Token
    def get(self):
        parser.add_argument('Token', type = str, location = 'cookies')
        args = parser.parse_args()
        arg_token = args['Token']
        username = token_verify.verify_token(arg_token)
        return make_response(render_template('user_info.html', username = username['username']))

class Signup_With_Email(Resource):
    def post(self):
        # 从'form'中拿到提交的数据
        parser.add_argument('username', type = str, location = 'form')
        parser.add_argument('password', type = str, location = 'form')
        args = parser.parse_args()
        arg_username = args['username']
        arg_password = args['password']

        # 存入数据库
        new_user = database_user(
            name = arg_username,
            password = arg_password
        )
        database_session.add(new_user)
        try:
            database_session.commit()
            database_session.close()
            return '记录成功'
        except Exception as e:
            database_session.rollback()
            database_session.close()
            return str(e), 500

    def get(self):
        return make_response(render_template('signup.html'))

class Test_Mail(Resource):
    def post(self):
        parser.add_argument('user_mail_address', type = str)
        args = parser.parse_args()
        arg_user_mail_address = args['user_mail_address']
        
        # 因为这里要用多线程，所以会脱离上下文，用copy_current_request_context装饰器来保留当前的上下文
        @copy_current_request_context
        def send_mail_and_record_random_num(target_mail_address):
            # 发送邮件，并把结果（4位随机字符串）赋值给r
            r = mail.send_mail(target_mail_address)
            # 接口返回的是一个tuple，tuple不可改变，所以用作记录非常合适
            if r:
                new_code_in_database = database_mail_code(mail_code = r)
                database_session.add(new_code_in_database)
                database_session.commit()
                database_session.close()
            else:
                database_session.rollback()
                database_session.close()

        # 使用多线程
        threading.Thread(target = send_mail_and_record_random_num, args = (arg_user_mail_address,)).start()
        # 多线程开始以后，就不必等待邮件发送完毕以后再返回结果了
        return '发送成功'

    def get(self):
        return make_response('\
            <form method="post"enctype="multipart/form-data">\
                <input type="text" name="user_mail_address">\
                <input type="submit" value="发送邮件">\
            </form>'
        )

api.add_resource(Login, '/')
api.add_resource(Signup_With_Email, '/signup')
api.add_resource(Test_Mail, '/mail')