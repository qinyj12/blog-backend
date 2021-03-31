#导入依赖包
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory
# 不知道为什么，这里直接from token绝对导入就是不行，要相对导入才可以
from ..token import token_create
from ..token import token_verify

app = Blueprint('token', __name__, url_prefix = '/token')
api = Api(app)
parser = reqparse.RequestParser()
# 拿到session
database_session = database_factory.session
# 拿到表类
database_user = database_tables.User

class Token(Resource):
    # 更新前端用户信息（token）
    # @token_ensure.ensure_exist_target_token('token', ['json', 'cookies', 'args']) # 首先确保存在token
    def get(self):
        # 首先获取前端的token
        parser.add_argument('X-Token', location = ['headers'])
        args = parser.parse_args()
        arg_token = args['X-Token']
        # 拿到token后，解密
        token_decrypt = token_verify.verify_token(arg_token)
        # print('拿到解密后的token ', token_decrypt)

        # 去数据库找到id == token['id']的那条记录
        target_user = database_session.query(database_user).filter_by(id = token_decrypt['id']).scalar()
        # 如果找到
        if target_user:
            print(target_user.avatar)
            database_session.close()
            user_info = {
                'id': target_user.id,
                'name': target_user.name, 
                'avatar': target_user.avatar, 
                'introduction': target_user.introduction,
                'roles': target_user.roles
            }
            user_token = token_create.create_token(user_info)
            # 最后把数据库的记录返回给前端
            resp = {
                'code': 20000, 
                'data': {
                    'info': user_info,
                    'token': user_token
                }
            }
            return resp, 200
        else:
            return {'code': 50008, 'message': '用户不存在'}, 200

api.add_resource(Token, '/update')