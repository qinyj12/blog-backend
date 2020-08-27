from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def create_token(parse):
    #第一个参数是内部的私钥，这里写在公用的配置信息里了，如果只是测试可以写死
    #第二个参数是有效期(秒)
    s = Serializer('dev', expires_in = 60 * 60 * 24)
    #接收用户id转换与编码
    token = s.dumps({"username": parse}).decode("ascii")
    return token