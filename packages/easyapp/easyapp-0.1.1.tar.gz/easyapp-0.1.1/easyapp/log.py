import http
import logging
import urllib
from copy import copy


logger = logging.getLogger()


class AccessFormatter(logging.Formatter):
    def get_client_addr(self, scope):
        client = scope.get("client")
        if not client:
            return ""
        return "%s:%d" % (client[0], client[1])

    def get_path(self, scope):
        return urllib.parse.quote(scope.get("root_path", "") + scope["path"])

    def get_full_path(self, scope):
        path = scope.get("root_path", "") + scope["path"]
        query_string = scope.get("query_string", b"").decode("ascii")
        if query_string:
            return urllib.parse.quote(path) + "?" + query_string
        return urllib.parse.quote(path)

    def get_status_code(self, record):
        status_code = record.__dict__["status_code"]
        try:
            status_phrase = http.HTTPStatus(status_code).phrase
        except ValueError:
            status_phrase = ""
        status_and_phrase = "%s %s" % (status_code, status_phrase)

        return status_and_phrase

    def formatMessage(self, record):
        recordcopy = copy(record)
        scope = recordcopy.__dict__["scope"]
        method = scope["method"]
        path = self.get_path(scope)
        full_path = self.get_full_path(scope)
        client_addr = self.get_client_addr(scope)
        status_code = self.get_status_code(recordcopy)
        http_version = scope["http_version"]
        request_line = "%s %s HTTP/%s" % (method, full_path, http_version)
        recordcopy.__dict__.update(
            {
                "method": method,
                "path": path,
                "full_path": full_path,
                "client_addr": client_addr,
                "request_line": request_line,
                "status_code": status_code,
                "http_version": http_version,
                # "query_string": query_string
            }
        )
        return super().formatMessage(recordcopy)


LOGCONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_stream": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelname)s %(message)s",
            "use_colors": None,
        },
        "default_file": {
            "()": "logging.Formatter",
            "fmt": "%(levelname)s %(message)s",
        },

        "access_stream": {
            "()": "uvicorn.logging.AccessFormatter",
            # "()": "logging.Formatter",
            "fmt": '%(levelname)s %(client_addr)s - "%(request_line)s" %(status_code)s  %(asctime)s',  # noqa: E501
        },
        "access_file": {
            "()": "easyapp.log.AccessFormatter",
            "fmt": '%(levelname)s  %(asctime)s  %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
        },
    },
    "handlers": {
        "default": {  # 控制台输出，默认的，变颜色的
            "formatter": "default_stream",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {  # http接口访问，控制台输出，变颜色的
            "formatter": "access_stream",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "default_file": {  # 日志文件输出，默认的，没有颜色
            # https://docs.python.org/zh-cn/3/library/logging.handlers.html#timedrotatingfilehandler
            "formatter": "default_file",
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'd',
            'interval': 1,
            'backupCount': 0,
            "filename": "./log/log.log",
            "delay": True,
            'encoding': 'utf-8'
        },
        "access_file": {  # http接口访问，日志文件台输出，无颜色的，自定义的handler
            # https://docs.python.org/zh-cn/3/library/logging.handlers.html#timedrotatingfilehandler
            "formatter": "access_file",
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'd',
            'interval': 1,
            'backupCount': 0,
            # "filename": "./log/log",
            "filename": "./log/log.log",
            "delay": True,
            # 'encoding':'utf-8'
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default", "default_file"], "level": "INFO", "propagate": False},
        # "": {"handlers": ["default"], "level": "INFO"},
        "": {"handlers": ["default", "default_file"], "level": "INFO", "propagate": False},
        # "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access", "access_file"], "level": "INFO", "propagate": False},
    },
}
