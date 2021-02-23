# 做一个装饰器，保证database的表存在
from sqlalchemy_utils import database_exists, create_database
from .database_factory import engine
from .database_tables import Base
from . import database_tables

# 因为这个装饰器要传参，所以要再做一层。
def ensure_database_tables(*target_tables):
    def wrapper_fir(func):
        def wrapper_sec(*args, **kw):
            # 如果这个数据库存在，那什么也不用做
            if database_exists(engine.url):
                pass
            
            # 如果这个数据库不存在，则创建这个数据库
            else:
                print('database not exists')
                # create_database('sqlite:///database.db', encoding = 'utf-8')
                Base.metadata.create_all(engine)
                print('database created')

            # 装饰器接受很多个参数，这些参数是表类的名称，遍历，判断是否存在这些表
            for __target_table in target_tables:
                # 如果表类不存在
                if not engine.dialect.has_table(engine, __target_table):
                    print(__target_table, 'not exists')
                    # 去定义表类的模块里拿到这个表的信息，比如database_tables.User
                    # 因为target_table参数是字符串，所以要用eval来转换，比如'database_tables.User' => database_table.User
                    ORMTable = eval('database_tables.' + __target_table)
                    # 然后创建表
                    ORMTable.__table__.create(bind = engine, checkfirst = True)
                    print(__target_table, 'created')
                # 如果表类已存在，跳过。并执行下一个遍历
                else:
                    pass
            return func(*args, **kw)
        return wrapper_sec
    return wrapper_fir