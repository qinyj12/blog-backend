from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
# 在factory/config/config的Config类中定义database的链接
from factory.config.config import Config

# 创建一个基类，所有映射数据表的类都继承自该基类
Base = declarative_base()

# 创建engine对象，所有对数据库的操作都通过engine对象来进行
engine = create_engine(
    Config.DATABASE_URL,
    pool_pre_ping=True, # 每次从连接池中拿连接的时候，都会向数据库发送一个测试查询语句来判断服务器是否正常运行。当该连接出现 disconnect 的情况时，该连接连同pool中的其它连接都会被回收。
    # max_overflow=0,   # 超过连接池大小外最多创建的连接
    pool_size=5,      # 连接池大小
    # pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=3600   # 多久之后对线程池中的线程进行一次连接的回收
)
# 使用sessionmaker来创建session类，同时用scoped_session来XXX（没搞懂）
DBSession = scoped_session(sessionmaker(engine))
# session是操作数据库的入口，用session来管理程序和数据库之间的会话，实现增删改查
session = DBSession()
