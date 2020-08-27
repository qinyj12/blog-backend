from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = '1562555013@qq.com'
app.config['MAIL_PASSWORD'] = 'agruhtsnobwlhbab'
app.config['MAIL_DEFAULT_SENDER'] = '1562555013@qq.com'

mail = Mail(app)

@app.route('/')
def index():
    msg = Message("Hello",
                  sender="1562555013@qq.com",
                  recipients=["1562555013@qq.com"])
    msg.body = "testing"
    mail.send(msg)

@app.route('/hello')
def hello():
    return 'hello'

if __name__ == '__main__':
    app.run()