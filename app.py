from factory import creat_app
from flask_cors import CORS
from factory.config.config import Config

app = creat_app()

# 跨域
CORS(app)

app.run(
    host = Config.HOST_NAME,
    port = Config.PORT_NAME,
    threaded = True # 开多线程，防止加载一个页面时访问多个服务，导致出错
)