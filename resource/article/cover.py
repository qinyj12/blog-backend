from flask import app, Blueprint, current_app
from flask_restful import Api, Resource, reqparse
from database import database_tables, database_factory
from ..token import token_verify
from werkzeug.datastructures import FileStorage
from factory.config.config import Config

app = Blueprint('cover', __name__, url_prefix = '/cover')
api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.DBSession()
# 拿到表类
database_article = database_tables.Article

class Cover(Resource):
    # 上传文章封面，当新建文章时调用
    def put(self):
        # 从files中拿到前端上传的cover
        parser.add_argument('img', type = FileStorage, location = ['files'])
        args = parser.parse_args()
        arg_cover = args['img']
        # 调用在工厂函数里定义的flask_uploads实例，保存前端上传的文件
        from api import create_time_stamp
        filename = current_app.cover_upload.save(arg_cover, name = create_time_stamp.now() + '.')
        # 获取保存后的地址
        file_url = 'http://' + Config.HOST_NAME + ':' + Config.PORT_NAME + '/' + current_app.cover_upload.path(filename)
        return {
            'code': 20000,
            'data': file_url
        }

    # 上传文章封面，当修改文章时调用
    def post(self):
        # 拿到前端上传的cover，和article_id
        parser.add_argument('img', type = FileStorage, location = ['files'])
        parser.add_argument('id', location = ['form'])
        args = parser.parse_args()
        arg_cover = args['img']
        arg_article_id = args['id']
        # 先找到对应的文章
        target_article = database_session.query(database_article).filter_by(id = arg_article_id).scalar()
        # 如果找得到
        if target_article:
            # 调用在工厂函数里定义的flask_uploads实例，保存前端上传的文件
            from api import create_time_stamp
            filename = current_app.cover_upload.save(arg_cover, name = create_time_stamp.now() + '.png')
            # 获取保存后的地址
            file_url = 'http://' + Config.HOST_NAME + ':' + Config.PORT_NAME + '/' + current_app.cover_upload.path(filename)
            # 修改数据库
            target_article.cover = file_url
            database_session.commit()
            database_session.close()

        # 如果找不到
        else:
            database_session.close()
            return {'code': 50008, 'message': 'article不存在'}

api.add_resource(Cover, '/')