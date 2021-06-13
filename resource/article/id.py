from logging import config
from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
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
            'tag': '',
            'file_name': '',
            'content': ''
        }
    # 根据id查询article信息
    def get(self):
        parser.add_argument('article_id', location = ['args'])
        parser.add_argument('if_need_content', location = ['args'])
        args = parser.parse_args()
        try:
            arg_id = int(args['article_id'])
        except:
            return {
                'code': 50000,
                'message': 'id出错'
            }
        arg_if_need_content = args['if_need_content']
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
            self.article_info['file_name'] = target_article.file_name

            # 判断是否需要content
            # 如果不需要content，返回值['content']为空
            if arg_if_need_content != 'true':
               self.article_info['content'] = ''
            # 如果需要content，返回值['content']赋值
            else:
                # 找到这个文章对应的目录（user_id + file.name)
                from factory.config.config import Config
                article_file_path = Config.ARTICLE_FILE_DEST + str(self.article_info['user_id']) + '/' + self.article_info['file_name']
                # 读取文章（md文件）的内容
                with open(article_file_path, 'r', encoding='utf-8') as md_f:
                    self.article_info['content'] = md_f.read()
            
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
