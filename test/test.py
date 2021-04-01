# import threading
# import time

# # def show(arg):
# #     time.sleep(1)
# #     print('thread '+str(arg)+" running....")

# # for i in range(3):
# #     t = threading.Thread(target=show, args=(i,))
# #     t.start()


# def demo():
#     def a(arg):
#         time.sleep(1)
#         print(arg)
    
#     t = threading.Thread(target = a, args = ('haha',))
#     t.start()

#     print('b')

# demo()

from flask_restful import fields

# 先定义一个格式化的数据，用来返回给前端固定格式的token
token_returned = {
    'id': fields.Integer,
    'name': fields.String, 
}

# 这似乎是一个中间件，资源调用这个中间件，然后中间件再去查询fields
class QueryToken(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

demo = ['id', 'name']

res = QueryToken(id = 1, name = 'a')

from json import JSONEncoder, JSONDecoder
class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__    

res1 = MyEncoder().encode(res)

def from_json(json_object):
    return QueryToken(
        json_object['id'], 
        json_object['name']
    )

res2 = JSONDecoder(object_hook = from_json).decode(res1)

print(res2.name)