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

# 获取所有用户的list
class AllUserList(Resource):
    def get(self):
        # 取多少条信息？
        # parser.add_argument('range', type = str, location = ['args'])
        # args = parser.parse_args()
        # arg_user_range = args['range']
        # target_user_list = database_user
        res = list(
            map(
                lambda x: 
                    {
                        'id': x.id,
                        'name': x.name, 
                        'email': x.email,
                        'phone': x.phone,
                        'avatar': x.avatar,
                        'roles': x.roles,
                        'introduction': x.introduction
                    }, 
                    database_session.query(database_user)[0:2]
            )
        )
        print(res)
        database_session.close()

api.add_resource(AllUserList, '/')