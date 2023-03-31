
# XMLRPC接口服务



XMLRPC是python标准库[xmlrpc](https://docs.python.org/zh-cn/3/library/xmlrpc.html)提供的RPC框架,一般我们会根据不同的需求配合使用标准库中的`socketserver.ThreadingMixIn`或者`socketserver.ForkingMixIn`来使用多线程或者多进程(注意只能在支持fork的平台使用)处理请求.注意XMLRPC并不安全,需要防止被人利用[XML漏洞](https://docs.python.org/zh-cn/3/library/xml.html#xml-vulnerabilities)


下面是一个简单的例子,我们把它放在[C0](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/RPC%E6%9C%8D%E5%8A%A1/code/XMLRPC%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/C0)中.这个例子我们计算输入的字符串的md5哈希值


## 最简单的服务端

`logger.py`用于定义结构化log. xmlrpc默认的会使用方法`SimpleXMLRPCRequestHandler.log_error(format, *args)`和`SimpleXMLRPCRequestHandler.log_request(code='-', size="-")`打印请求信息和错误信息到`stderr`,默认的打印方式是`plain text`格式的,这种非结构化的数据往往难以收集分析,我们使用`structlog`将其结构化.

```python
import sys
import logging
import structlog
LOG_LEVEL = logging.INFO
SERVER_NAME = "xmlrpc-server"
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

handler = logging.StreamHandler(sys.stdout)
root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(LOG_LEVEL)  # 设置最低log等级
log = structlog.get_logger(SERVER_NAME)
    ```
        
`server.py`用于实现算法逻辑.

```python
import time
from hashlib import md5
from http import HTTPStatus
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
from logger import log


HOST = "localhost"
PORT = 5000

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/XMLRPC',)
    def log_error(self, format, *args):
        """Log an error.

        This is called when a request cannot be fulfilled.  By
        default it passes the message on to log_message().

        Arguments are the same as for log_message().

        XXX This should go to the separate error log.

        """
        log.error("server error",address=self.address_string(),errormsg=format%args)

    def log_request(self, code='-', size="-"):
        """Log an accepted request.

        This is called by send_response().

        """
        if isinstance(code, HTTPStatus):
            code = code.value
        log.info("request info",address=self.address_string(),requestline=self.requestline, code=str(code), size=str(size))

class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def md5_func(text: str)->str:
    """md5哈希."""
    start = time.time()
    result = md5(text.encode("utf-8")).hexdigest()
    end = time.time()
    log.info("time it",seconds=end-start)
    return result


def main():
    with ThreadingXMLRPCServer((HOST, PORT), requestHandler=RequestHandler, allow_none=True) as server:
        # 注册所有可调用函数的名字到system.listMethods方法
        # 注册可调用函数的docstring到system.methodHelp(func_name)方法
        # 注册可调用函数的签名到system.methodSignature(func_name)方法
        server.register_introspection_functions()

        # 这个函数的作用是可以使客户端同时调用服务端的的多个函数。
        server.register_multicall_functions()

        # 注册一个函数,使它可以被调用,后面的字符串就是被调用的函数名
        server.register_function(md5_func, md5_func.__name__)
        try:
            log.info("server start", msg=f"xmlrpc start @ {HOST}:{PORT}!")
            server.serve_forever()
        except Exception:
            log.info("server error", exc_info=True, stack_info=True)
            raise
        finally:
            log.info("server stoped", msg=f"xmlrpc @ {HOST}:{PORT} stoped!")


if __name__ == "__main__":
    main()
    
```

xmlrpc只要将函数注册到server对象,然后执行`server_forever()`方法即可.

## 最简单的客户端


```python
import xmlrpc.client

HOST = "localhost"
PORT = 5000

with xmlrpc.client.ServerProxy(f"http://{HOST}:{PORT}/XMLRPC") as proxy:
    result = proxy.md5_func("这是一个测试")

print(result)
```


这个例子中我们使用多线程以提高rpc服务的并发性能,但一般来说rpc是计算密集型任务,并发上去并不解决问题,更关键的是将每个核利用起来,我们当然也可以多起实例通多代理做负载均衡,但更简单的方案是利用多核将重计算的部分放在多进行中执行.

## 利用多核

在多进程部分我们讲过如何[使用concurrent.futures进行高层抽象的多进程操作](http://blog.hszofficial.site/TutorialForPython/%E8%AF%AD%E6%B3%95%E7%AF%87/%E6%B5%81%E7%A8%8B%E6%8E%A7%E5%88%B6/%E5%A4%9A%E8%BF%9B%E7%A8%8B.html#%E4%BD%BF%E7%94%A8concurrentfutures%E8%BF%9B%E8%A1%8C%E9%AB%98%E5%B1%82%E6%8A%BD%E8%B1%A1%E7%9A%84%E5%A4%9A%E8%BF%9B%E7%A8%8B%E6%93%8D%E4%BD%9C),这边我们还是使用这种方式,代码[C1](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/RPC%E6%9C%8D%E5%8A%A1/code/XMLRPC%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/C1)展示了如何改造上面的例子

+ server.py

```python
...
from concurrent.futures import ProcessPoolExecutor,wait

...

WORKER = 4

...

# 注意此处修改函数名字
def _md5_func(text: str)->str:
    """md5哈希."""
    start = time.time()
    result = md5(text.encode("utf-8")).hexdigest()
    end = time.time()
    log.info("time it",seconds=end-start)
    return result


def main():
    with ProcessPoolExecutor(WORKER) as executor:
        # 将要执行的业务包装,实际执行交给执行器
        def md5_func(text:str)->str:
            fut = executor.submit(_md5_func, text)
            wait([fut])
            return fut.result()

        with ThreadingXMLRPCServer((HOST, PORT), requestHandler=RequestHandler, allow_none=True) as server:
            # 注册所有可调用函数的名字到system.listMethods方法
            # 注册可调用函数的docstring到system.methodHelp(func_name)方法
            # 注册可调用函数的签名到system.methodSignature(func_name)方法
            server.register_introspection_functions()

            # 这个函数的作用是可以使客户端同时调用服务端的的多个函数。
            server.register_multicall_functions()

            # 注册一个函数,使它可以被调用,后面的字符串就是被调用的函数名
            server.register_function(md5_func, md5_func.__name__)
            try:
                log.info("server start", msg=f"xmlrpc start @ {HOST}:{PORT}!")
                server.serve_forever()
            except Exception:
                log.info("server error", exc_info=True, stack_info=True)
                raise
            finally:
                log.info("server stoped", msg=f"xmlrpc @ {HOST}:{PORT} stoped!")


if __name__ == "__main__":
    main()
    
```
