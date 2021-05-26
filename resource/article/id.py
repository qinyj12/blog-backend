from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory

app = Blueprint('articleId', __name__, url_prefix = '/article/id')
api = Api(app)
parser = reqparse.RequestParser()

database_session = database_factory.session
database_article = database_tables.Article

# 根据userID获取具体某个article的全部信息
class IdArticleInfo(Resource):
    def __init__(self):
        self.article_info = {
            'id': None,
            'title': '', 
            'user_id': '',
            'create_time': '',
            'cover': '',
            'state': '',
            'tag': ''
        }
    # 根据id查询article信息
    def get(self):
        parser.add_argument('articleid', type = str, location = ['args'])
        args = parser.parse_args()
        arg_id = int(args['articleid'])
        target_article = database_session.query(database_article).filter_by(id = arg_id).scalar()
        # 如果能在数据库找到
        if target_article:
            # 从数据库拿到数据，然后赋值给已定义好的user_info模板
            self.article_info['id'] = target_article.id
            self.article_info['title'] = target_article.title
            self.article_info['user_id'] = target_article.user_id
            self.article_info['cover'] = target_article.cover
            self.article_info['state'] = target_article.state
            self.article_info['tag'] = target_article.tag
            resp = {
                'code': 20000,
                'data': self.article_info
            }
            database_session.close()
            return resp, 200
        else:
            resp = {
                'code': 50000,
                'message': '根据id查找文章出错'
            }
            return resp, 200

api.add_resource(IdArticleInfo, '/')
