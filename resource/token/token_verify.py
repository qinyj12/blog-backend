from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 这是一个接收token，然后解密的函数
def verify_token(token):
    #参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer('dev')
    try:
        #转换为字典
        data = s.loads(token)
        print('token解析完成，内容是', data)
        return data
    except Exception as e:
        return e
    #拿到转换后的数据，根据模型类去数据库查询用户信息
    # user = User.query.get(data["id"])
    # return user