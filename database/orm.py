from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def initialize_orm():
    Base = declarative_base()

    # User表
    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key = True, nullable = False)
        name = Column(String(20), nullable = False)
        email = Column(String(20), nullable = True)
        password = Column(String(20), nullable = False)
        signup_time = Column(String(20), nullable = False)

    # 这里要注意路径是datebase/database.db
    # engine = create_engine('sqlite:///database/database.db', connect_args = {'check_same_thread': False})
    engine = create_engine(
        "mysql+pymysql://root:password@127.0.0.1:3306/main?charset=utf8",
        # max_overflow=0,   # 超过连接池大小外最多创建的连接
        # pool_size=5,      # 连接池大小
        # pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        # pool_recycle=-1   # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )

    DBSession = sessionmaker(engine)
    session = DBSession()

    return {'session': session, 'user': User}
    # return Base.metadata.create_all(engine)
