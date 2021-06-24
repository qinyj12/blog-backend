from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory

app = Blueprint('userid', __name__, url_prefix = '/user/id')
api = Api(app)
parser = reqparse.RequestParser()

database_session = database_factory.DBSession()
database_user = database_tables.User

# 根据userID获取具体某个用户的全部信息
class IdUserInfo(Resource):
    def __init__(self):
        self.user_info = {
            'id': None,
            'name': 'unnamed', 
            'email': '',
            'phone': '',
            'avatar': '',
            'roles': '',
            'introduction': ''
        }
    # 根据id查询用户信息
    def get(self):
        parser.add_argument('userid', type = str, location = ['args'])
        args = parser.parse_args()
        arg_id = int(args['userid'])
        target_user = database_session.query(database_user).filter_by(id = arg_id).scalar()
        # 如果能在数据库找到
        if target_user:
            # 从数据库拿到数据，然后赋值给已定义好的user_info模板
            self.user_info['id'] = target_user.id
            self.user_info['name'] = target_user.name
            self.user_info['email'] = target_user.email
            self.user_info['phone'] = target_user.phone
            self.user_info['avatar'] = target_user.avatar
            self.user_info['roles'] = target_user.roles
            self.user_info['introduction'] = target_user.introduction
            resp = {
                'code': 20000,
                'data': self.user_info
            }
            database_session.close()
            return resp, 200
        else:
            database_session.close()
            resp = {
                'code': 50000,
                'message': '根据id查找用户出错'
            }
            return resp, 200

api.add_resource(IdUserInfo, '/')
