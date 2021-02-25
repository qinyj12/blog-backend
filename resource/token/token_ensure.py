from flask_restful import reqparse
from flask import make_response, render_template

parser = reqparse.RequestParser()

# 定义一个判断是否登录的装饰器
def ensure_exist_target_token(target_token):
    def wrapper_fir(func):
        def wrapper_sec(*args, **kw):
            print('使用装饰器，判断前端是否存在cookies')
            # 判断cookie中有没有保存名为target_token的token
            parser.add_argument(target_token, type = str, location = 'cookies')
            args = parser.parse_args()
            print(args)
            # 如果保存了token
            if args[target_token]:
                print('存在cookies')
                return func(*args, **kw)
            # 如果没有保存token
            else:
                print('no cookie')
                return '没有发现token', 400
                # 因为是通过flask_restful的api返回的，所以返回的是json字符串，要用make_response格式化一下
                # return make_response(render_template('login.html'))
            return func(*args, **kw)
        return wrapper_sec
    return wrapper_fir