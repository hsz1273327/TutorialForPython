"""项目的log配置."""
import sys
import time
import logging
import structlog
from flask import request
from flask.logging import default_handler
import werkzeug._internal as _internal
logging.Formatter.converter = time.gmtime
class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.request = '{0} {1}'.format(request.method, request.url)
        record.host = request.host
        return super().format(record)
access_formatter=RequestFormatter(** {
    "fmt": '''{"timestamp":"%(asctime)s","logger":"app.access", "level":"%(levelname)s","host":"%(host)s","request":"%(request)s",%(message)s}''',
    "datefmt": "%Y-%m-%dT%H:%M:%S Z"
})

werkzeug_formatter = logging.Formatter(**{
    "fmt": '''{"timestamp":"%(asctime)s","logger":"werkzeug.server", "level":"%(levelname)s","msg":"%(message)s"}''',
    "datefmt": "%Y-%m-%dT%H:%M:%S Z"
})
def init_app(app,flask_log_level=logging.INFO,werkzeug_log_level=logging.INFO):
    default_handler.setFormatter(access_formatter)

    handler = logging.StreamHandler(sys.stdout)
    flask_app_logger = logging.getLogger("flask.app")
    flask_app_logger.addHandler(handler)
    flask_app_logger.setLevel(flask_log_level)  # 设置最低log等级
    werkzeug_handler = logging.StreamHandler()
    werkzeug_handler.setFormatter(werkzeug_formatter)
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.handlers = []
    werkzeug_logger.addHandler(werkzeug_handler)
    werkzeug_logger.setLevel(werkzeug_log_level)  # 设置最低log等级
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
    log = structlog.get_logger("flask.app")
    app.logger = log
    return app