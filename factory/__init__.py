import os
from flask import Flask
from flask_mail import Mail

def creat_app(spare_config = None):
    # 自定义实例文件夹/resource，此处为绝对路径，可以通过其他参数改为相对路径
    # 和模板文件夹/template，此处为相对路径
    # ################################# static_folder，好像通过这个参数可以让外部访问这个文件夹
    app = Flask(
        __name__, 
        instance_path = '/resource', 
        template_folder = '../template', 
        # 默认的static目录是'/factory/static'，这里改成'/static'
        static_folder = os.path.join(os.getcwd(), 'static')
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
    from resource import test_hello, test_user
    app.register_blueprint(test_hello.app)
    app.register_blueprint(test_user.app)

    from resource.token import update
    app.register_blueprint(update.app)

    from resource.user import oauth, login, name, avatar, phone, role, create
    app.register_blueprint(oauth.app)
    app.register_blueprint(login.app)
    app.register_blueprint(name.app)
    app.register_blueprint(avatar.app)
    app.register_blueprint(phone.app)
    app.register_blueprint(role.app)
    app.register_blueprint(create.app)

    from resource.user import collection as user_collection
    from resource.user import id as user_id
    app.register_blueprint(user_collection.app)
    app.register_blueprint(user_id.app)

    from resource.article import collection as article_collection
    from resource.article import id as article_id
    app.register_blueprint(article_collection.app)
    app.register_blueprint(article_id.app)

    from resource.illustration import upload
    app.register_blueprint(upload.app)

    # 创建一个flask-mail实例
    app.mail_instance = Mail(app)

    # 创建flask-uploads实例
    from flask_uploads import IMAGES, ALL, configure_uploads, UploadSet
    app.illustration_upload = UploadSet('illustration', IMAGES)
    configure_uploads(app, app.illustration_upload)

    return app