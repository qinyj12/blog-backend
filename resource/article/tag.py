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
        # 要统计tag频次，就要有一个统计上限
        parser.add_argument('max_num', type = int, location = ['args'])
        args = parser.parse_args()
        args_tags_max_num = args['max_num']
        # tag统计频次
        count_result = database_session.query(database_article.tag, func.count(database_article.tag)).group_by(database_article.tag).all()
        print(count_result)
        # 因为统计到的成果是这样的[('a',1),('b',2)]，所以要转换一下
        count_result_in_list = list({'tag': i[0], 'num': i[1]} for i in count_result)
        # 然后根据前端的传值，拿到max_num以内的统计结果
        # 当然要先close链接
        database_session.close()
        return {
            'code': 20000,
            'data': count_result_in_list[0 : args_tags_max_num]
        }

api.add_resource(Tag, '/')