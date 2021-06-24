from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory

app = Blueprint('phone', __name__, url_prefix = '/phone')
api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.DBSession()
# 拿到表类
database_user = database_tables.User

# 用于用户电话的函数，修改电话
class Phone(Resource):
    def post(self):
        # 先从url中拿到目标电话和目标用户
        parser.add_argument('phone', type = str, location = ['args'])
        parser.add_argument('targetUser', location = ['args'])
        args = parser.parse_args()
        arg_phone = args['phone']
        user_id = args['targetUser']

        # 调用函数，判断电话是否符合标准，并且是否未在数据库出现。如果符合条件
        if if_phone_not_repeated(arg_phone) and if_phone_legal(arg_phone):
            # 找到对应的用户
            target_user = database_session.query(database_user).filter_by(id = user_id).scalar()
            # 修改数据库中的phone字段
            target_user.phone = arg_phone
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
                'data': {'if_available': False, 'result': '电话重复或者不合法'}
            }

# 判断电话是否重复
def if_phone_not_repeated(phone_input):
    if database_session.query(database_user).filter_by(phone = phone_input).all():
        return False
    else:
        return True

# 判断电话是否标准（不含空格）
def if_phone_legal(phone_input):
    if ' ' not in phone_input and len(phone_input) == 11 and phone_input[0] == '1':
        return True
    else:
        return False

api.add_resource(Phone, '/')