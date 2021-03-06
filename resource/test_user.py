#导入依赖包
from flask import Blueprint, render_template, make_response
from flask_restful import Api, Resource, reqparse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from functools import wraps

def create_token(parse):
    #第一个参数是内部的私钥，这里写在公用的配置信息里了，如果只是测试可以写死
    #第二个参数是有效期(秒)
    s = Serializer('dev', expires_in = 60)
    #接收用户id转换与编码
    token = s.dumps({"id":parse}).decode("ascii")
    return token

def verify_token(token):
    #参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer('dev')
    try:
        #转换为字典
        data = s.loads(token)
        return data
    except Exception as e:
        return e
    #拿到转换后的数据，根据模型类去数据库查询用户信息
    # user = User.query.get(data["id"])
    # return user

app = Blueprint('user', __name__, url_prefix = '/user')
api = Api(app)
parser = reqparse.RequestParser()

# 定义一个判断是否登录的装饰器
def ensure_token(func):
    @wraps(func)
    def inner(self):
        # 判断cookie中有没有保存token
        parser.add_argument('Token', type = str, location = 'cookies')
        args = parser.parse_args()
        # 如果保存了token
        if args['Token']:
            return func(self)
        # 如果没有保存token，即尚未登录
        else:
            # 因为是通过flask_restful的api返回的，所以返回的是json字符串，要用make_response格式化一下
            return make_response(render_template('login.html'))
    return inner

class User(Resource):
    def post(self):
        # 从'form'中拿到提交的数据
        parser.add_argument('username', type = str, location = 'form')
        args = parser.parse_args()
        arg_username = args['username']

        # 生成token
        user_token = create_token(arg_username)
        # 把token放在返回头里
        return '已登录： %s' % arg_username, 200, {'Set-Cookie':'Token=' + user_token + ';Max-Age=' + str(10)}

        ######## 需要先验证提交的数据，通过后作为token放在返回头里

    # 快使用装饰器，嚯嚯哈嘿
    @ensure_token
    def get(self):
        parser.add_argument('Token', type = str, location = 'cookies')
        args = parser.parse_args()
        arg_token = args['Token']
        username = verify_token(arg_token)
        return username

api.add_resource(User, '/')