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


# import sys
# sys.path.append('c:/Users/Lenovo/Desktop/blog-backend/')

# from database import database_tables, database_factory
# # 拿到session
# database_session = database_factory.session
# # 拿到表类
# database_user = database_tables.User

# target_user = database_session.query(database_user).filter_by(id = 0).scalar()

# print(list(map(lambda x: x.id, target_user.relate_article)))

# database_session.close()

demo = [('a',1),('b',2)]

demo2 = list({'tag': i[0], 'num': i[1]} for i in demo)

print(demo2)
