#导入依赖包
from flask import Blueprint, render_template, make_response, redirect
from flask.helpers import url_for
from flask_restful import Api, Resource, reqparse
from database import orm
from ..token import token_create
from ..token import token_verify
from ..token import token_ensure


app = Blueprint('login', __name__, url_prefix = '/login')
api = Api(app)
parser = reqparse.RequestParser()
database_orm = orm.initialize_orm()
database_session = database_orm['session']
database_user = database_orm['user']

class Login(Resource):
    def post(self):
        # 从'form'中拿到提交的数据
        parser.add_argument('username', type = str, location = 'form')
        args = parser.parse_args()
        arg_username = args['username']

        # 生成token
        user_token = token_create.create_token(arg_username)
        # 把token放在返回头里
        # return '已登录： %s' % arg_username, 200, {'Set-Cookie':'Token=' + user_token + ';Max-Age=' + str(10)}
        # 因为要redirect的同时设置cookie，用make_response更轻松
        resp = make_response(redirect(url_for('.login')))
        resp.set_cookie('Token', user_token, 10)
        return resp
        ######## 需要先验证提交的数据，通过后作为token放在返回头里

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

api.add_resource(Login, '/')
api.add_resource(Signup_With_Email, '/signup')