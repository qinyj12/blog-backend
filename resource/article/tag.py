from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from database import database_tables, database_factory
from ..token import token_verify
from sqlalchemy import func

app = Blueprint('article_tag', __name__, url_prefix = '/article/tag')
api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.session
# 拿到表类
database_article = database_tables.Article

class Tag(Resource):
    def get(self):
        # 下一步，完善tag统计频次的后盾接口
        a = database_session.query(database_article.tag, func.count(database_article.tag)).group_by(database_article.tag).all()
        return a

api.add_resource(Tag, '/')