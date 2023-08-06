# from uvicorn.config import LOGGING_CONFIG
import logging
import traceback
import os

from config.openapi import DOC_CONFIG
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request

from . import MyException, MyResponseError, ResultError, get_id
from .log import LOGCONFIG, logger
from .main_init import get_routers_custom, init_openapi_doc

logging.config.dictConfig(LOGCONFIG)

app = FastAPI()
app.log_config=LOGCONFIG
# app.default_response_class = MyResponse

# 开始初始化项目定制的路由
app.include_router(get_routers_custom())

# 初始化log目录
if not os.path.exists('./log'):
    os.makedirs('./log')  

# 初始化文档doc参数属性
init_openapi_doc(app, DOC_CONFIG)


@app.get("/favicon.ico")
async def demo():
    return ''

# 预留，验证身份使用


@app.middleware("http")
async def process_authorization(request: Request, call_next):

    response = await call_next(request)
    return response


@app.exception_handler(Exception)
async def request_validation_exception_handler(request: Request, e: Exception):
    logger.error(
        f"全局异\n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

    result=ResultError(
        code=9000,
        msg='内部错误',
        detail=None,
        errmsg=str(e.args),
        errid=get_id(),
        traceback=traceback.format_exc()
        )
    return MyResponseError(result)

@app.exception_handler(MyException)
async def request_validation_exception_handler(request: Request, e: MyException):
    logger.error(
        f"全局异\n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

    result=ResultError(
        code=e.code,
        msg=e.msg,
        detail=e.detail,
        errmsg=e.errmsg,
        errid=get_id(),
        traceback=traceback.format_exc()
        )
    return MyResponseError(result)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    result=ResultError(code=100)
    # return MyResponseError({"detail": exc.errors(), "body": exc.body})
    return MyResponseError(result)
