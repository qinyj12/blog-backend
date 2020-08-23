from flask import Blueprint, render_template, make_response
from flask_restful import Api, Resource

app = Blueprint('login_with_qq', __name__, url_prefix = '/qqlogin')

api = Api(app)

class Login(Resource):
    def get(self):
        return make_response(render_template('qqlogin.html'))

api.add_resource(Login, '/')