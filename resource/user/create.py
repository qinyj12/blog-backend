# 创建一个新用户
from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory

app = Blueprint('CreateUser', __name__, url_prefix = '/user')
api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.session
# 拿到表类
database_user = database_tables.User

# 新建用户
class UserCreator(Resource):
    def __init__(self):
        # 定义新增用户必填的字段
        self.user_info = {
            'name': 'undefined',
            'password': 'undefined',
            'roles': 'undefined',
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif?imageView2/1/w/80/h/80'
        }
    def put(self):
        parser.add_argument('name', type = str, location = ['args'])
        parser.add_argument('password', type = str, location = ['args'])
        parser.add_argument('role', type = str, location = ['args'])
        args = parser.parse_args()
        arg_name = args['name']
        arg_passwd = args['password']
        arg_role = args['role']
        self.user_info['name'] = arg_name
        self.user_info['password'] = arg_passwd
        self.user_info['roles'] = arg_role

        database_session.add(
            database_user(
                name = self.user_info['name'],
                password = self.user_info['password'],
                roles = self.user_info['roles'],
                avatar = self.user_info['avatar']
            )
        )
        try:
            database_session.commit()
            database_session.close()
            return {
                'code': 20000,
                'data': {'result': '新增成功'}
            }
        except:
            database_session.rollback()
            database_session.close()
            return {
                'code': 20000,
                'data': {'result': '失败'}
            }

api.add_resource(UserCreator, '/create')