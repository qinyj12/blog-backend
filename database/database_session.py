from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 创建engine对象，所有对数据库的操作都通过engine对象来进行
engine = create_engine(
    "mysql+pymysql://qinyj12:123456@127.0.0.1:3306/main?charset=utf8",
    # max_overflow=0,   # 超过连接池大小外最多创建的连接
    # pool_size=5,      # 连接池大小
    # pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    # pool_recycle=-1   # 多久之后对线程池中的线程进行一次连接的回收（重置）
)
# 使用sessionmaker来创建session类
DBSession = sessionmaker(engine)
# session是操作数据库的入口，用session来管理程序和数据库之间的会话，实现增删改查
session = DBSession()
