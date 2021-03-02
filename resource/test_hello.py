from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from database import database_tables, database_factory
from database.ensure_database_integrity import ensure_database_tables

app = Blueprint('hello', __name__, url_prefix = '/hello')

api = Api(app)
parser = reqparse.RequestParser()

# 拿到session
database_session = database_factory.session
# 拿到表类
database_test = database_tables.Test

class Hello(Resource):
    def get(self):
        return {'result': 'hello world'}

class Test(Resource):
    # 引入装饰器，确保存在Test表
    @ensure_database_tables('Test')
    def get(self):
        parser.add_argument('content', type = str, location = 'args')
        args = parser.parse_args()
        arg_res = args['content']
        new_test = database_test(
            content = arg_res
        )
        database_session.add(new_test)
        try:
            database_session.commit()
            database_session.close()
            return '记录成功'
        except Exception as e:
            database_session.rollback()
            database_session.close()
            return str(e), 500


api.add_resource(Hello, '/')
api.add_resource(Test, '/test')