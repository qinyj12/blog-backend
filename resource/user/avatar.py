from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse, request
from database import database_tables, database_factory
from ..token import token_verify
from werkzeug.datastructures import FileStorage
import pathlib

app = Blueprint('avatar', __name__, url_prefix = '/avatar')
api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.session
# 拿到表类
database_user = database_tables.User

class Avatar(Resource):
    # 修改用户头像
    def post(self):
        # 从files中拿到前端上传的avatar
        parser.add_argument('avatar', type = FileStorage, location = ['files'])
        # 拿到前端传来的token
        parser.add_argument('X-Token', location = ['headers'])
        args = parser.parse_args()
        arg_avatar = args['avatar']
        arg_token = args['X-Token']
        # 解析token中的信息
        token_verified = token_verify.verify_token(arg_token)
        user_id = token_verified['id']
        save_dir = './static/user/' + str(user_id)
        # 创建名为user_id的目录，用来保存头像。如果目录已存在的话，就不用创建了
        pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True) 
        # 此处要指定保存的位置和文件名
        arg_avatar.save(save_dir + '/avatar.png')
        print(arg_avatar.read())

        return {
            'code': 20000,
            'data': 'avatar'
        }

api.add_resource(Avatar, '/')