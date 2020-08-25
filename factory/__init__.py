import os
from flask import Flask, url_for

def creat_app(spare_config = None):
    # 自定义实例文件夹/resource，此处为绝对路径，可以通过其他参数改为相对路径
    # 和模板文件夹/template，此处为相对路径
    # ################################# static_folder，好像通过这个参数可以让外部访问这个文件夹
    app = Flask(
        __name__, 
        instance_path = '/resource', 
        template_folder = '../template', 
        # static_folder = '../static', 
        # static_url_path = '/static'
    )

    # 如果creat_app()没有接收到参数，使用默认的config文件
    if spare_config is None:
        from .config import config
        app.config.from_object(config.Config)

    # 否则，使用参数中的config文件
    else:
        app.config.from_pyfile(spare_config)

    # 引入蓝图
    from resource import hello, user
    from resource.login import oauth, login
    app.register_blueprint(hello.app)
    app.register_blueprint(user.app)
    app.register_blueprint(oauth.app)
    app.register_blueprint(login.app)

    return app