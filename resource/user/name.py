from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory
from ..token import token_verify

app = Blueprint('name', __name__, url_prefix = '/name')
api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.session
# 拿到表类
database_user = database_tables.User

# 用于用户名的函数，修改用户名
class Name(Resource):
    def post(self):
        # 先从url中拿到目标用户名
        parser.add_argument('name', type = str, location = ['args'])
        parser.add_argument('targetUser', location = ['args'])
        args = parser.parse_args()
        arg_name = args['name']
        user_id = args['targetUser']
        print(user_id)

        # 调用函数，判断用户名是否符合标准，并且是否未在数据库出现。如果符合条件
        if if_name_not_repeated(arg_name) and if_name_legal(arg_name):
            # 找到对应的用户
            target_user = database_session.query(database_user).filter_by(id = user_id).scalar()
            # 修改数据库中的name字段
            target_user.name = arg_name
            database_session.commit()
            database_session.close()
            return {
                'code': 20000,
                'data': {'if_available': True, 'result': '修改成功'}
            }                                                                                                                                          
        else:
            return {
                'code': 20000,
                'data': {'if_available': False, 'result': '用户名重复或者包含空格'}
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

api.add_resource(Name, '/')