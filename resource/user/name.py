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
class Name_Availability(Resource):
    def get(self):
        # 先从url中拿到目标用户名
        parser.add_argument('name', type = str, location = ['args'])
        args = parser.parse_args()
        arg_name = args['name']

        # 调用函数，判断用户名是否已在数据库出现。如果已出现
        if if_name_not_repeated(arg_name) and if_name_legal(arg_name):
            return {
                'code': 20000,
                'data': '可用'
            }                                                                                                                                          
        else:
            return {
                'code': 20000,
                'data': '不可用，用户名重复或者包含空格'
            }

# 判断用户名是否重复
def if_name_not_repeated(name_input):
    if database_session.query(database_user).filter_by(name = name_input).scalar():
        return False
    else:
        return True

# 判断用户名是否标准（不含空格）
def if_name_legal(name_input):
    if ' ' in name_input:
        return False
    else:
        return True

api.add_resource(Name_Availability, '/availability')