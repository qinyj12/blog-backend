from flask import app, Blueprint, current_app
from flask_restful import Api, Resource, reqparse, request
from database import database_tables, database_factory
from ..token import token_verify
from werkzeug.datastructures import FileStorage
from factory.config.config import Config

app = Blueprint('article', __name__, url_prefix = '/save')
api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.session
# 拿到表类
database_article = database_tables.Article

class ArticleCreator(Resource):
    def __init__(self):
        self.article_info = {
            'title': 'undefined',
            'user_id': 0,
            'cover': 'undefined',
            'state': '草稿',
            'tag': 'undefined'
        }

    # 新增article文章
    def put(self):
        # 拿到前段传来的各种article信息
        parser.add_argument('user_id', location = ['form'])
        parser.add_argument('article_title', location = ['form'])
        parser.add_argument('article_cover', type = FileStorage, location = ['files'])
        parser.add_argument('article_tag', location = ['form'])
        parser.add_argument('article_state', location = ['form'])
        # 不能从前端传送md到后端，而要在后端生成md
        parser.add_argument('article_md', type = FileStorage, location = ['files'])

        args = parser.parse_args()
        self.article_info['title'] = args['article_title']
        self.article_info['user_id'] = args['user_id']
        self.article_info['cover'] = args['article_cover']
        self.article_info['state'] = args['article_state']
        self.article_info['tag'] = args['article_tag']

        arg_article_content = args['article_md']

        database_session.add(
            database_article(
                title = self.article_info['title'] ,
                user_id = self.article_info['user_id'],
                cover = self.article_info['cover'],
                state = self.article_info['state'],
                tag = self.article_info['tag']
            )
        )

        # 调用在工厂函数里定义的flask_uploads实例，保存前端上传的文件
        filename = current_app.illustration_upload.save(arg_article_content)
        # 获取保存后的地址
        file_url = 'http://' + Config.HOST_NAME + ':' + Config.PORT_NAME + '/' + current_app.article_upload.path(filename)

        try:
            database_session.commit()
            database_session.close()
            return {
                'code': 20000,
                'data': {'result': '新增成功', 'article_url': file_url}
            }
        except:
            database_session.rollback()
            database_session.close()
            return {
                'code': 20000,
                'data': {'result': '失败'}
            }

api.add_resource(ArticleCreator, '/')