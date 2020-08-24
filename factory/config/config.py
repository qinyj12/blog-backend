from factory.config import secret
# 继承secret.py中Secret父类，Secret父类定义了一些密码，不能同步到github上
class Config(secret.Secret):
    # 开启debug模式
    DEBUG = True
    # 非ASCII编码不要转义
    RESTFUL_JSON = {'ensure_ascii': False}