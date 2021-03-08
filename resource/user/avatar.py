from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse, request
from database import  database_tables, database_factory
import base64

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
        # 因为是post方法，要从form中拿到前端上传的avatar
        # parser.add_argument('avatar', location = ['form'])
        # args = parser.parse_args()
        # arg_avatar = args['avatar']

        print(dict(request.form))

        # with open('demo.png', 'wb') as _:
        #     _.write(base64.b64encode(arg_avatar))
        return {
            'code': 20000,
            'data': 'avatar'
        }

api.add_resource(Avatar, '/')