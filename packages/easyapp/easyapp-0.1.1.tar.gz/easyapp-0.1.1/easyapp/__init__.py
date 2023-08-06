from .db import Db
from .log import logger
from config.application import settings
# import config.application_model
from .result import MyResponse, MyResponseError, ResultError, MyException
from .tools import IdWorker

settings=settings

# 初始化数据库默认链接
Db.dbconfig_default = dict(settings.DB_OPTION)

db = Db()  # 默认链接配置的Db实例
Db = Db  # 自己初始化链接的类对象

logger = logger

MyResponseError: MyResponseError = MyResponseError
ResultError: ResultError = ResultError
MyResponse: MyResponse = MyResponse
MyException: MyException = MyException
get_id = IdWorker(1,1,1).get_id
