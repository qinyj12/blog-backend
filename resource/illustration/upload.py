from flask import app, Blueprint, current_app
from flask_restful import Api, Resource, reqparse, request
from werkzeug.datastructures import FileStorage
import pathlib
import time
import os
from factory.config.config import Config

app = Blueprint('illustration', __name__, url_prefix = '/illustration')
api = Api(app)
parser = reqparse.RequestParser()

class Upload(Resource):
    def post(self):
        parser.add_argument('illustration', type = FileStorage, location = ['files'])
        args = parser.parse_args()
        arg_illustration = args['illustration']
        # 调用在工厂函数里定义的flask_uploads实例，保存前端上传的文件
        filename = current_app.illustration_upload.save(arg_illustration)
        # 获取保存后的地址
        file_url = 'http://' + Config.HOST_NAME + ':' + Config.PORT_NAME + '/' + current_app.illustration_upload.path(filename)
        # return {
        #     'code': 20000,
        #     'data': file_url
        # }
        return {
            "msg": "",  
            "code": 0,  
            "data": {  
                "errFiles": [],  
                "succMap": {  
                    "demo.png": file_url,  
                }  
            }  
        }

api.add_resource(Upload, '/upload/')