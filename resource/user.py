#导入依赖包
from flask import request,jsonify,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

User = {'id':1, 'name':'dog'}

def create_token(api_user):
    #第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    #第二个参数是有效期(秒)
    s = Serializer('dev', expires_in = 3)
    #接收用户id转换与编码
    token = s.dumps({"id":api_user}).decode("ascii")
    return token

def verify_token(token):
    print(token)
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

temp = create_token('123')
print(temp)

import time
time.sleep(4)

temp2 = verify_token(temp)
print(temp2)