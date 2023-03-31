
# 使用Sanic构建异步的RESTful接口服务

[sanic](https://github.com/huge-success/sanic)是一个基于python3.6+新特性协程的异步框架,其接口设计参照了同样受欢迎的[flask](http://flask.pocoo.org/)但它比flask更加轻量,由于协程的作用,其并发性能更强.而且并不需要借助其他http组件就可以单独运行,甚至于它还可以多进程启动.当然相对的它的生态比flask差的多,但作为一个Restful接口服务它已经很够用了,同时他也是目前最成熟的python异步接口的http框架.

## helloworld

我们依然从一个[helloworld](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/Http%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/code/sanic-server/C0)开始.

RESTful接口基于HTTP的METHOD,因此我们也常用`HTTPMethodView`构造基于METHOD的接口

这种应用构造的过程就是:

+ 使用`Sanic()`创建一个应用实例
+ 继承`HTTPMethodView`构造一个对应RESTful概念中RESOURCE的视图类
+ 通过调用视图类的方法`.as_view()`将视图类转化为一个视图对象
+ 调用应用实例的`.add_route(view,url)`方法将视图对象注册到应用实例对应的url下


+ `app.py`

```python
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json as jsonify
from jsonschema import validate

app = Sanic()

User = []

User_Schema = {
    "title": "User",
    "description": "用户",
    "type": "object",
    "properties": {
        "name": {
            "description": "user name",
            "type": "string"
        }, "age": {
            "description": "user age",
            "type": "integer",
            "minimum": 0,
            "maximum": 140,
            "exclusiveMaximum": True
        }
    },
    "required": ["name", "age"]
}


class UserIndexAPI(HTTPMethodView):

    async def get(self, request):
        count = len(User)
        result = {
            "description": "测试api,User总览",
            "user-count": count,
            "links": [
                {
                    "uri": "/user",
                    "method": "POST",
                    "description": "创建一个新用户"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "GET",
                    "description": "用户号为<id>的用户信息"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "PUT",
                    "description": "更新用户号为<id>用户信息"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "DELETE",
                    "description": "删除用户号为<id>用户"
                },
            ]
        }

        return jsonify(result, ensure_ascii=False)

    async def post(self, request):
        insert = request.json

        try:
            validate(instance=insert, schema=User_Schema)
        except Exception as e:
            return jsonify({
                "msg": "参数错误",
                "error": str(e)
            }, ensure_ascii=False, status=401)
        else:
            uid = User.append(insert)
            return jsonify({
                "msg": "插入成功",
                "uid": uid
            }, ensure_ascii=False)


class UserAPI(HTTPMethodView):

    async def get(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                return jsonify(u, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)

    async def put(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                insert = request.json
                u.update(insert)
                return jsonify({
                    "msg": "更新成功"
                }, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)

    async def delete(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                User[uid] = None
                return jsonify({
                    "msg": "删除成功",
                }, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)


user_index_view = UserIndexAPI.as_view()
user_view = UserAPI.as_view()


app.add_route(user_index_view, '/user')
app.add_route(user_view, '/user/<uid:int>')

if __name__ == "__main__":
    app.run(host='localhost', port=5000)
```

为了防止`json`和标准库重名,我们最好将`sanic.response.json`重命名为`jsonify`.为了返回的数据支持utf-8,我们需要为`jsonify`接口传入参数`ensure_ascii=False`.需要注意`jsonify`中可以用`status`字段设置http状态码,这是和flask中不同的地方

这个app可以直接使用命令`python app.py`独立部署.我们可以直接设置参数定义部署时候的服务器信息.主要的参数有:

参数|默认值|说明
---|---|---
`host`|"127.0.0.1"|服务的host
`port`|8000|服务的端口
`debug`| False| debug模式,会降低性能
`ssl` |None|ssl上下文,用于配置https
`sock`|None|可以通过绑定`unix sock`而非host+port来建立连接
`workers`|1|执行服务的进程数
`loop`|None|指定一个asyncio协议的loop对象
`access_log`|True|请求信息记录进log,会显著降低性能





## 为接口写测试

RESTful接口最大的优势是可以方便的写测试,我们使用项目[C1](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/Http%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/code/sanic-server/C1)来演示如何为Sanic写接口测试,sanic的app对象自己提供了一个测试客户端接口,我们可以利用它来实现测试

+ test.py

```python
from app import app
import unittest

class SanicTestCase(unittest.TestCase):

    def setUp(self):
        print("测试开始")
        self.app = app.test_client
    def tearDown(self):
        print("测试结束")

    def test_user(self):
        request, response  = self.app.get('/user')
        assert "user-count" in response.json.keys()
```


## 使用蓝图为接口分组

上面的用户接口相对是比较简单的,如果碰到更多的接口需要组织,或者需要区分版本,或者由的url要复用视图,那这种在app下直接挂载就会失去灵活性,我们希望将视图模块化来解决上面的问题.Sanic也提供了蓝图模式来做这个功能.其基本用法是:

1. 使用Sanic()创建一个应用实例
2. 使用Blueprint()创建蓝图对象并定义蓝图对象的一级url
3. 继承HTTPMethodView构造一个对应RESTful概念中RESOURCE的视图类
4. 通过调用视图类的方法.as_view()将视图类转化为一个视图对象
5. 调用蓝图对象的.add_route(view,url)方法将视图对象注册到蓝图对象对应的二级url下
6. 使用app.blueprint(api_v1, url_prefix='/v1')将蓝图注册到应用实例上


我们将原来的user接口挂载到一级urlv1上,项目在[C2](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/Http%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/code/sanic-server/C2)上

+ `app.py`

```python
...
from sanic import Blueprint


app = Sanic()
api_v1 = Blueprint('v1_blueprint')

...

api_v1.add_route(user_index_view, '/user')
api_v1.add_route(user_view, '/user/<uid:int>')

app.blueprint(api_v1, url_prefix='/v1')

if __name__ == "__main__":
    app.run(host='localhost', port=5000)
```

### 为蓝图分组

我们可以将蓝图注册到组上过程也与注册到app对象上类似,例子为[C3](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/Http%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/code/sanic-server/C3),我们新增一个todo的source:

+ `app.py`

```python
from sanic import Sanic
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json as jsonify
from jsonschema import validate

app = Sanic()
api_user = Blueprint('api_user')

User = []

User_Schema = {
    "title": "User",
    "description": "用户",
    "type": "object",
    "properties": {
        "name": {
            "description": "user name",
            "type": "string"
        }, "age": {
            "description": "user age",
            "type": "integer",
            "minimum": 0,
            "maximum": 140,
            "exclusiveMaximum": True
        }
    },
    "required": ["name", "age"]
}


class UserIndexAPI(HTTPMethodView):

    async def get(self, request):
        count = len(User)
        result = {
            "description": "测试api,User总览",
            "user-count": count,
            "links": [
                {
                    "uri": "/user",
                    "method": "POST",
                    "description": "创建一个新用户"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "GET",
                    "description": "用户号为<id>的用户信息"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "PUT",
                    "description": "更新用户号为<id>用户信息"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "DELETE",
                    "description": "删除用户号为<id>用户"
                },
            ]
        }

        return jsonify(result, ensure_ascii=False)

    async def post(self, request):
        insert = request.json

        try:
            validate(instance=insert, schema=User_Schema)
        except Exception as e:
            return jsonify({
                "msg": "参数错误",
                "error": str(e)
            }, ensure_ascii=False, status=401)
        else:
            uid = User.append(insert)
            return jsonify({
                "msg": "插入成功",
                "uid": uid
            }, ensure_ascii=False)


class UserAPI(HTTPMethodView):

    async def get(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                return jsonify(u, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)

    async def put(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                insert = request.json
                u.update(insert)
                return jsonify({
                    "msg": "更新成功"
                }, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)

    async def delete(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                User[uid] = None
                return jsonify({
                    "msg": "删除成功",
                }, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)


user_index_view = UserIndexAPI.as_view()
user_view = UserAPI.as_view()

api_user.add_route(user_index_view, '/user')
api_user.add_route(user_view, '/user/<uid:int>')


api_todo = Blueprint('api_todo')

Todo = {}

Todo_Schema = {
    "title": "Todo",
    "description": "工作列表",
    "type": "object",
    "properties": {
        "msg": {
            "description": "message",
            "type": "string"
        }, "dead_line": {
            "description": "dead line",
            "type": "str"
        }
    },
    "required": ["msg"]
}


class TodoAPI(HTTPMethodView):

    async def get(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                if Todo.get(uid):
                    return jsonify({"uid": uid, "todo": Todo.get(uid)}, ensure_ascii=False)
                else:
                    return jsonify({
                        "msg": "未找到用户的todo列表",
                    }, ensure_ascii=False, status=404)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)

    async def post(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                insert = request.json
                try:
                    validate(instance=insert, schema=Todo_Schema)
                except Exception as e:
                    return jsonify({
                        "msg": "参数错误",
                        "error": str(e)
                    }, ensure_ascii=False, status=401)
                else:
                    Todo.get(uid).append(insert)
                    return jsonify({
                        "msg": "插入成功"
                    }, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)


todo_view = TodoAPI.as_view()
api_todo.add_route(todo_view, '/todo/<uid:int>')

api_v1 = Blueprint.group(api_user, api_todo)

app.blueprint(api_v1, url_prefix='/v1')

if __name__ == "__main__":
    app.run(host='localhost', port=5000)

```

## 使用钩子控制服务行为


Sanic程序只有3类钩子


+ `Listeners`在整个服务的启动过程和结束过程时生效,使用装饰器`app.listener(listener)`来注册,其装饰的函数必须由参数`app`和`loop`,包括:

    + before_server_start
    + after_server_start
    + before_server_stop
    + after_server_stop

+ `middleware`在每次请求的处理前后生效,需要注意sanic中没有针对Blueprint或者Blueprint group的`middleware`,虽然Blueprint有接口,但是全局的

    + 装饰器`@app.middleware('request')`修饰的函数必须有参数`request`
    + 装饰器`@app.middleware('response')`修饰的函数必须有参数`request`和`response`

+ `Handler Decorators`修饰view的装饰器,只要对需要修饰的view中的方法修饰即可如果是整个view都需要装饰,那么可以在定义的`HTTPMethodView`的子类中申明`decorators = [some_decorator_here]`
    一个典型的装饰器如下:

    ```python
    from functools import wraps
    import time
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            start = time.time()
            response = await f(request, *args, **kwargs)
            end = time.time()
            spend = end-start
            print(f"spend {spend} s")
            return response
        return decorated_function
    ```

我们用例子[C4](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/Http%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/code/sanic-server/C4)来展示下

+ `app.py`

```python
...
from functools import wraps
import time
def print_time():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            start = time.time()
            response = await f(request, *args, **kwargs)
            end = time.time()
            spend = end-start
            print(f"spend {spend} s")
            return response
        return decorated_function
    return decorator

...

class UserIndexAPI(HTTPMethodView):
    @print_time
    async def get(self, request):
        
...

class TodoAPI(HTTPMethodView):
    decorators = [print_time]
    
...
@app.listener("before_server_start")
async def _before_server_start(app,loop):
    print("before_server_start")

@app.listener("after_server_start")
async def _after_server_start(app,loop):
    print("after_server_start")

@app.listener("before_server_stop")
async def _before_server_stop(app,loop):
    print("before_server_stop")

@app.listener("after_server_stop")
async def _after_server_stop(app,loop):
    print("after_server_stop")

@app.middleware('request')
async def print_on_request(request):
	print("I print when a request is received by the server")

@app.middleware('response')
async def print_on_response(request, response):
	print("I print when a response is returned by the server")

...
```

## 修改log

sanic默认的log为`sanic.root`,`sanic.error`和`sanic.access`,输出是扁平的文本,而现在的趋势是使用json格式化log以便于后续分析,为了满足这个需求,我们可以像下面这样设置,代码在[C5](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/Http%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/code/sanic-server/C5)

+ `logger.py`

```python
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
```
上面的代码我们将`sanic.log.logger`替换成了`structlog`的`log`,这样我们的log就是结构化数据了.要使用可以直接使用`sanic.log.logger`


+ `app.py`

```python
...
from logger import LOGGING_CONFIG_JSON
from sanic.log import logger
...

app = Sanic(log_config=LOGGING_CONFIG_JSON)

...
@app.middleware('response')
async def print_on_response(request, response):
	logger.info("I print when a response is returned by the server")
...
```

## 错误处理

另一个常见的需要是错误处理,通常RESTful接口会复用http状态,比如500表示服务器错误,404表示找不到资源.我们使用`app.exception`来定义错误的处理方式[C6](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/Http%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/code/sanic-server/C6)

```python
...
from sanic.exceptions import NotFound
...

@app.exception(NotFound)
async def ignore_404s(request, exception):
    return jsonify({"message": "page not found"}, status=404)


@app.exception(Exception)
async def ignore_500s(request, exception):
    return jsonify({"message": "server error"}, status=500)
...
```
