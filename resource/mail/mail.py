from flask_mail import Message
from flask import current_app, render_template, copy_current_request_context
import random

# 自定义一个随机整数类，接受一个参数
class Random_Code():
    def __init__(self, count):
        # 0 < 接受的参数 < 20，并且接受的参数必须是整数
        if isinstance(count, int) and 0 < count < 20 and str.isdigit(str(count)):
            # 做一个生成器，共由几位整数字符组成，位数 == count
            self.random_number_generator = (str(random.randint(0, 9)) for _ in range(count))
            self.result = ''.join(self.random_number_generator)
        else:
            # 如果接受的参数不满足条件的话，就raise ValueError
            raise ValueError('必须是大于0小于20的正整数')

    # 用print()调用
    def __repr__(self):
        return self.result

    # sql会调用translate()方法，不然无法录入数据库。第二个参数似乎是字符映射转换表，用sqlalchemy时自带，不用传入
    def translate(self, *arg):
        return self.result

def send_mail(target_mail_address):
    mail = current_app.mail_instance
    msg = Message('hello', sender = '1562555013@qq.com', recipients = [target_mail_address])
    # 快使用我自定义的Random_Code类，生成4位随机字符串，炒鸡好用
    new_code = Random_Code(4)
    msg.html = render_template('mail_code.html', code = new_code)
    # 先尝试发送邮件，如果成功，再把这个随机字符串保存到数据库
    try:
        mail.send(msg)
        return (new_code)
    except:
        return False