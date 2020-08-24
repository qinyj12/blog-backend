from flask import Blueprint, render_template, make_response, json, current_app
from flask_restful import Api, Resource, reqparse, fields, marshal_with
import requests

app = Blueprint('login_with_github', __name__, url_prefix = '/oauth')
api = Api(app)
parser = reqparse.RequestParser()

# 自定义一个格式化的数据，这个数据就是返回给前端的response，这里对response的格式、类型等做了限定
user_fields = {
    'id': fields.Integer,
    # 如果给本fields发送的请求中不含有name（实操下来发现就是name = None），则response默认值unnamed
    'name': fields.String(default = 'unnamed'),
    'avatar': fields.String(default = 'null'),
    'bio': fields.String(default = 'null'),
    'email': fields.String(default = 'empty')
}
# 这似乎是一个中间件，资源调用这个中间件，然后中间件再去查询fields
class QueryUser(object):
    # 给参数设置默认值None，这样才能触发fields中的default
    def __init__(self, id, name = None, avatar = None, bio = None, email = None):
        self.id = id
        self.name = name
        self.avatar = avatar
        self.bio = bio
        self.email = email

class Github_Callback(Resource):
    @marshal_with(user_fields)
    def get(self):
        # 拿到github返回的code
        parser.add_argument('code', type = str, location = 'args')
        args = parser.parse_args()
        arg_code = args['code']
        # 带着code去请求POST https://github.com/login/oauth/access_token，使用requests库
        ###################################### 需要设置成私密文件，不能上传至git
        requests_date = {
            'client_id': current_app.config['GITHUB_OAUTH']['client_id'], 
            'client_secret': current_app.config['GITHUB_OAUTH']['client_secret'], 
            'code': arg_code
        }
        r = requests.post('https://github.com/login/oauth/access_token', data = requests_date)
        if r.status_code == 200:
            # 拿到github返回的结果，重新拼接成另一个请求，再次请求github
            info = requests.get('https://api.github.com/user?' + r.text)
            if info.status_code == 200:
                # github接口返回的是json格式
                info_dict = json.loads(info.text)
                # 调用中间件
                return QueryUser(
                    id = 1, 
                    name = info_dict['login'], 
                    avatar = info_dict['avatar_url'], 
                    bio = info_dict['bio'], 
                    email = info_dict['email']
                )

            else:
                return info.text, 400
        else:
            return r.text, 400

class Login_With_Github(Resource):
    def get(self):
        return make_response(render_template('login_github.html'))

api.add_resource(Login_With_Github, '/github')
api.add_resource(Github_Callback, '/github/callback')