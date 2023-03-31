import time
import sys
import logging
import sanic.log
import structlog
logging.Formatter.converter = time.gmtime


LOGGING_CONFIG_JSON = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO", "handlers": ["console"]},
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": True,
            "qualname": "sanic.access",
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "error_msg",
            "stream": sys.stderr,
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout,
        },
    },
    formatters={
        "generic": {
            "format": '''%(message)s''',
            "datefmt": "%Y-%m-%dT%H:%M:%S Z",
            "class": "logging.Formatter",
        },
        "error_msg": {
            "format": '''{"time":"%(asctime)s","process":"%(process)d", "level":"%(levelname)s","msg":"%(message)s"}''',
            "datefmt": "%Y-%m-%dT%H:%M:%S Z",
            "class": "logging.Formatter",
        },
        "access": {
            "format": '''{"time":"%(asctime)s","name":"%(name)s", "level":"%(levelname)s","host":"%(host)s","status":"%(status)d","byte":"%(byte)d","request":"%(request)s"}''',
            "datefmt": "%Y-%m-%dT%H:%M:%S Z",
            "class": "logging.Formatter",
        },
    },
)


#logging.config.dictConfig(LOGGING_CONFIG_JSON)
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,  # 判断是否接受某个level的log消息
        structlog.stdlib.add_logger_name,  # 增加字段logger
        structlog.stdlib.add_log_level,  # 增加字段level
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),  # 增加字段timestamp且使用iso格式输出
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,  # 捕获异常的栈信息
        structlog.processors.StackInfoRenderer(),  # 详细栈信息
        structlog.processors.JSONRenderer()  # json格式输出,第一个参数会被放入event字段
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
log = structlog.get_logger("sanic.root")
sanic.log.logger = log