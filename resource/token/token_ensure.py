from functools import wraps
from flask_restful import reqparse
from flask import make_response, render_template

parser = reqparse.RequestParser()

# 定义一个判断是否登录的装饰器
def ensure_exist(func):
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