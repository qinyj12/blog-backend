#导入依赖包
from flask import Blueprint, render_template, make_response, redirect, g, url_for, current_app, copy_current_request_context
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory
# 不知道为什么，这里直接from token绝对导入就是不行，要相对导入才可以
from ..token import token_create
from ..token import token_verify
from ..token import token_ensure
from ..mail import mail
import threading
from database.ensure_database_integrity import ensure_database_tables

app = Blueprint('login', __name__, url_prefix = '/login')
api = Api(app)
parser = reqparse.RequestParser()
# 拿到session
database_session = database_factory.session
# 拿到表类
database_user = database_tables.User
database_mail_code = database_tables.Mail_Code

# 涉及到登录的函数，post用于验证用户名密码，get用于解析token
class Login(Resource):
    def __init__(self):
        self.user_info = {
            'id': 0,
            'name': 'unnamed', 
            'avatar': '', 
            'introduction': '',
            'roles': ''
        }
    # post用于验证用户名密码，验证通过后加密返回
    def post(self):
        # 先后从'json'和'args'中拿到提交的数据，分别对应的是post和get方法
        parser.add_argument('username', type = str, location = ['json', 'args'])
        parser.add_argument('password', type = str, location = ['json', 'args'])
        args = parser.parse_args()
        arg_username = args['username']
        arg_password = args['password']

        # 去数据库判断用户名和密码是否一致，返回的是database对象，直接target_user.id/name/avatar就能拿到数据
        target_user = database_session.query(database_user).filter_by(name = arg_username, password = arg_password).scalar()
        # 如果通过
        if target_user:
            database_session.close()
            # 从数据库拿到数据，然后赋值给已定义好的user_info模板
            self.user_info['id'] = target_user.id
            self.user_info['name'] = target_user.name
            self.user_info['avatar'] = target_user.avatar
            self.user_info['introduction'] = target_user.introduction
            self.user_info['roles'] = target_user.roles
            # 加密user_info为token
            user_token = token_create.create_token(self.user_info)
            # 因为要redirect的同时设置cookie，用make_response更轻松
            # resp = make_response(redirect(url_for('.login')))
            # resp.set_cookie('Token', user_token, 100)
            resp = {
                'code': 20000, 
                'data': {'token': user_token}
            }
            return resp, 200
        # 如果用户名和密码不一致
        else:
            return {'code': 50008, 'message': '用户名和密码不一致'}, 200

    # 使用装饰器，确保前端cookie中存在名为blog_backend_token的token
    # 前端定义的就是通过get方法把token传参过来。
    @token_ensure.ensure_exist_target_token('token', ['json', 'cookies', 'args'])
    # get用于解析token
    def get(self):
        # print('通过装饰器判断，开始解析token')
        # 从前端拿到token后
        parser.add_argument('token', type = str, location = ['json', 'cookies', 'args'])
        args = parser.parse_args()
        arg_token = args['token']
        # 拿到token后，解密
        token_decrypt = token_verify.verify_token(arg_token)
        print('拿到解密后的token ', token_decrypt)
        resp = {
            'code': 20000,
            'data': token_decrypt
        }
        # print('getInfo')
        return resp, 200
        # return make_response(render_template('user_info.html', username = username['username']))

class Signup_With_Email(Resource):
    # 引入装饰器，确保存在User表
    @ensure_database_tables('User')
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