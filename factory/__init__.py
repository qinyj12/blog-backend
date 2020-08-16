import os
from flask import Flask

def creat_app(spare_config = None):
    # 自定义实例文件夹/app
    app = Flask(__name__, instance_path = '/resource')

    # 如果creat_app()没有接收到参数，使用默认的config文件
    if spare_config is None:
        from .config import config
        app.config.from_object(config.Config)

    # 否则，使用参数中的config文件
    else:
        app.config.from_pyfile(spare_config)

    # 引入蓝图
    from resource import hello
    app.register_blueprint(hello.app)

    return app