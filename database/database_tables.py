from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
# 引入Base基类
from database.database_factory import Base

# User表
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String(20), nullable = False)
    email = Column(String(20), nullable = True)
    phone = Column(String(20), nullable = True)
    password = Column(String(20), nullable = False)
    avatar = Column(String(100), nullable = True)
    roles = Column(String(20), nullable = True)
    introduction = Column(String(100), nullable = True)
    signup_time = Column(DateTime, default = func.now(), nullable = False)
    relate_article = relationship('Article', backref = 'relate_user', lazy = 'dynamic')

# Article表
class Article(Base):
    __tablename__ = 'Article'
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String(20), nullable = False)
    user_id = Column(Integer, ForeignKey('User.id'))
    create_time = Column(DateTime, default = func.now(), nullable = False)
    cover = Column(String(100), nullable = False)
    state = Column(String(20), nullable = False)
    tag = Column(String(20), nullable = True)

# 邮件验证码表
class Mail_Code(Base):
    __tablename__ = 'Mail_Code'
    id = Column(Integer, primary_key = True, nullable = False)
    mail_code = Column(String(20), nullable = False)
    time = Column(DateTime, default = func.now(), nullable = False)

# 测试表
class Test(Base):
    __tablename__ = 'Test'
    id = Column(Integer, primary_key = True, nullable = False)
    content = Column(String(20), nullable = False)
    time = Column(DateTime, default = func.now(), nullable = False)