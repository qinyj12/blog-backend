from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse, request
from database import database_tables, database_factory
from ..token import token_verify
from werkzeug.datastructures import FileStorage
import pathlib
import time

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
        # 先找到对应的用户
        target_user = database_session.query(database_user).filter_by(id = user_id).scalar()
        if target_user:
            # 先拿到老的avatar名字，"http://127.xxx/./static/user/1/avatar/xx.png"=>"./static/user/1/avatar/xx.png"
            old_avatar = target_user.avatar.strip('http://127.0.0.1:5000/')

            # 找到/static/user/1/avatar/目录
            save_dir = './static/user/' + str(user_id) + '/avatar/' 
            # 创建名为user_id的目录，用来保存头像。如果目录已存在的话，就不用创建了
            pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True) 
            # 保存新的avatar，并加时间戳，防止因为链接一成不变导致前端缓存无法改变
            avatar_filename = 'avatar_' + str(int(time.time())) +'.png'
            avatar_fullpath = save_dir + avatar_filename
            arg_avatar.save(avatar_fullpath)
            print(arg_avatar.read())

            # 再修改数据库
            target_user.avatar = 'http://127.0.0.1:5000/' + avatar_fullpath
            database_session.commit()
            database_session.close()

            # 最后删除老的avatar
            import os
            os.remove(old_avatar)
        else:
            return {'code': 50008, 'message': '用户不存在'}, 200

        return {
            'code': 20000,
            'data': 'avatar'
        }

api.add_resource(Avatar, '/')