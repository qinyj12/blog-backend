# 这个蓝图是用来放文章信息集合的，比如查询符合条件的所有文章信息
from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from database import  database_tables, database_factory

app = Blueprint('articleInfoCollection', __name__, url_prefix = '/article/collection/')
api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.session
# 拿到表类
database_article = database_tables.Article
database_user = database_tables.User

import datetime
import json
# 数据库中的signup_time的类型是datetime，无法转化为json格式，需要自定义转码的方法
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d') # 只取年月日
        else:
            return json.JSONEncoder.default(self, obj)        

# 获取所有文章的list
class AllArticleList(Resource):
    def get(self):
        # 取多少条信息？
        parser.add_argument('range_start', type = str, location = ['args'])
        parser.add_argument('range_end', type = str, location = ['args'])
        args = parser.parse_args()
        range_start = int(args['range_start'])
        range_end = int(args['range_end'])
        article_in_range = list(
            map(
                lambda x: 
                    {
                        'id': x.id,
                        'title': x.title, 
                        'user_id': x.user_id,
                        'user_name': database_session.query(database_user).filter_by(id = x.user_id).scalar().name,
                        'user_avatar': database_session.query(database_user).filter_by(id = x.user_id).scalar().avatar,
                        'create_time': x.create_time,
                        'cover': x.cover,
                        'state': x.state,
                        'tag': x.tag
                    }, 
                database_session.query(database_article).order_by(database_article.id.desc())[range_start: range_end]
            )
        )
        from sqlalchemy.sql import func
        article_total_num = database_session.query(func.count(database_article.id)).scalar()
        resp = {
            'code': 20000,
            'data': {
                'totalNum': article_total_num,
                'articleInRange': json.dumps(article_in_range, cls=DateEncoder) # 使用自定义的json转码方法
            }
        }
        database_session.close()
        return resp, 200

api.add_resource(AllArticleList, '/list/')
