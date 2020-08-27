import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import random
from database import orm
database_orm = orm.initialize_orm()
database_session = database_orm['session']
database_mail_code = database_orm['mail_code']

class Random_Code():
    def __init__(self, count):
        if isinstance(count, int) and 0 < count < 20 and str.isdigit(str(count)):
            self.random_number_list = (str(random.randint(0, 9)) for _ in range(count))
            self.result = ''.join(self.random_number_list)
        else:
            raise ValueError('必须是大于0小于20的正整数')

    def __str__(self):
        return self.result

    def translate(self, *arg):
        return self.result

# new_code = database_mail_code(mail_code = Random_code(4))
# database_session.add(new_code)
# database_session.commit()
# database_session.close()

temp = ['\\0', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\t', '\\n', '\x0b', '\x0c', '\\r', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\\Z', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', ' ', '!', '\\"', '#', '$', '%', '&', "\\'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\x7f']
a = Random_Code(4)
print(a)
print(a.translate(temp))