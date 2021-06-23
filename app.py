from factory import creat_app
from flask_cors import CORS
from factory.config.config import Config

app = creat_app()

# 跨域
CORS(app)

app.run(
    host = Config.HOST_NAME,
    port = Config.PORT_NAME,
    threaded = True # 开多线程
)