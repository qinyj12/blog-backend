from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory

app = Blueprint('name', __name__, url_prefix = '/name')
api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.session
# 拿到表类
database_user = database_tables.User

# 用于用户名的函数，get用于验证用户名是否重复
class Name(Resource):
    def get(self):
        # 先从url中拿到目标用户名
        parser.add_argument('name', type = str, location = ['args'])
        args = parser.parse_args()
        arg_name = args['name']

        # 判断目标用户名是否已在数据出现，如果已经出现
        if database_session.query(database_user).filter_by(name = arg_name).scalar():
            # 还需要和前端匹配接口格式
            return '重复'
        else:
            return '单一'

api.add_resource(Name, '/')