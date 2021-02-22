from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

# 创建一个基类，所有映射数据表的类都继承自该基类
Base = declarative_base()

# User表
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String(20), nullable = False)
    email = Column(String(20), nullable = True)
    password = Column(String(20), nullable = False)
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