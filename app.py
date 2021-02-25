from factory import creat_app
from flask_cors import CORS

app = creat_app()

# 跨域
CORS(app)

app.run(
    host = '0.0.0.0',
    port = '5000'
)