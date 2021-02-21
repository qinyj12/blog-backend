# 做一个装饰器，保证database的表存在
from sqlalchemy_utils import database_exists, create_database
import importlib
from database import database_session.engine as engine
from database import database_tables.Base as Base

# 因为这个装饰器要传参，所以要再做一层。
def ensure_database_integrity(func):
    def wrapper(*args, **kw):
        if database_exists("mysql+pymysql://qinyj12:123456@127.0.0.1:3306/main?charset=utf8"):
            print('database exists')

        else:
            print('database not exists')
            # create_database('sqlite:///database.db', encoding = 'utf-8')
            Base.metadata.create_all(engine)

        # 这里的表名要做成参数，可以传参到装饰器
        if not engine.dialect.has_table(engine, 'test'):
            print('no table')
            # 这里的table是定义表的文件，也可以做成参数动态传参到装饰器
            table_moudles = importlib.import_module('table')
            # 这里的table_moudles.Test是表的类，可以动态传参
            ORMTable = table_moudles.Test
            ORMTable.__table__.create(bind = engine, checkfirst = True)
        else:
            pass
        return func(*args, **kw)
    return wrapper