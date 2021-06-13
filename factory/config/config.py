from factory.config import secret
# 继承secret.py中Secret父类，Secret父类定义了一些密码，不能同步到github上
class Config(secret.Secret):
    # 开启debug模式
    DEBUG = True
    # 非ASCII编码不要转义
    RESTFUL_JSON = {'ensure_ascii': False}
    # 数据库链接
    DATABASE_URL = 'mysql+pymysql://qinyj12:123456@127.0.0.1:3306/main?charset=utf8'
    # flask_uploads的配置
    UPLOADED_ILLUSTRATION_DEST = './static/article/illustration/'
    UPLOADED_COVER_DEST = './static/article/cover/'
    # 自定义host ip地址
    HOST_NAME = '127.0.0.1'
    # 自定义port端口
    PORT_NAME = '5000'
    # 自定义文章保存父目录
    ARTICLE_FILE_DEST = './static/article/md_file/'

