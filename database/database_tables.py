from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
# 引入Base基类
from database.database_factory import Base

# User表
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String(20), nullable = False)
    email = Column(String(20), nullable = True)
    password = Column(String(20), nullable = False)
    roles = Column(String(20), nullable = True)
    introduction = Column(String(100), nullable = True)
    avatar = Column(String(100), nullable = True)
    signup_time = Column(DateTime, default = func.now(), nullable = False)

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