from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory

app = Blueprint('userlist', __name__, url_prefix = '/userlist')
api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.session
# 拿到表类
database_user = database_tables.User

import datetime
import json
# 数据库中的signup_time的类型是datetime，无法转化为json格式，需要自定义转码的方法
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d') # 只取年月日
        else:
            return json.JSONEncoder.default(self, obj)


# 获取所有用户的list
class AllUserList(Resource):
    def get(self):
        # 取多少条信息？
        parser.add_argument('range_start', type = str, location = ['args'])
        parser.add_argument('range_end', type = str, location = ['args'])
        args = parser.parse_args()
        range_start = int(args['range_start'])
        range_end = int(args['range_end'])
        user_in_range = list(
            map(
                lambda x: 
                    {
                        'id': x.id,
                        'name': x.name, 
                        'email': x.email,
                        'phone': x.phone,
                        'avatar': x.avatar,
                        'roles': x.roles,
                        'introduction': x.introduction,
                        'signup_time': x.signup_time
                    }, 
                    database_session.query(database_user).order_by(database_user.id.desc())[range_start: range_end]
            )
        )
        from sqlalchemy.sql import func
        user_total_num = database_session.query(func.count(database_user.id)).scalar()
        resp = {
            'code': 20000,
            'data': {
                'totalNum': user_total_num,
                'userInRange': json.dumps(user_in_range, cls=DateEncoder) # 使用自定义的json转码方法
            }
        }
        database_session.close()
        return resp, 200

api.add_resource(AllUserList, '/')