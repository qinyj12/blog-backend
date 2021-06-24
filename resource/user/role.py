from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory

app = Blueprint('role', __name__, url_prefix = '/role')
api = Api(app)
parser = reqparse.RequestParser()
# 拿到session
database_session = database_factory.DBSession()
# 拿到表类
database_user = database_tables.User

# 用于用户权限的函数，修改电话
class Role(Resource):
    def __init__(self):
        self.user_roles = ['管理员', '作者']

    def post(self):
        # 先从url中拿到目标电话和目标用户
        parser.add_argument('role', type = str, location = ['args'])
        parser.add_argument('targetUser', location = ['args'])
        args = parser.parse_args()
        arg_role = args['role']
        user_id = args['targetUser']
        # 判断权限是否符合标准。如果符合条件
        if arg_role in self.user_roles:
            # 找到对应的用户
            target_user = database_session.query(database_user).filter_by(id = user_id).scalar()
            # 修改数据库中的role字段
            target_user.roles = arg_role
            database_session.commit()
            database_session.close()
            return {
                'code': 20000,
                'data': {'if_available': True, 'result': '修改成功'}
            }                                                                                                                                          
        else:
            database_session.close()
            return {
                'code': 20000,
                'data': {'if_available': False, 'result': '权限不合法'}
            }

api.add_resource(Role, '/')