
# ZERORPC接口服务

[zerorpc](https://github.com/0rpc/zerorpc-python)是python下一个相当好用的rpc框架,它利用zeromq的req/req模式通信,利用msgpack做序列化.

相较于xmlrpc和jsonrpc它支持返回流,表达能力更丰富,而相较于grpc,它写法更加简单,毕竟不需要先定义数据的结构.基本上zerorpc算是python下体验最好的rpc框架了.

## 简单的请求应答

我们使用例子[C0](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/RPC%E6%9C%8D%E5%8A%A1/code/ZERORPC%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/C0)演示zerorpc最常用的使用方式.这个例子和前面的一样,是一个求字符串md5的hash值的服务.

### 服务端


+ logger.py

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

+ server.py

```python
import time
from hashlib import md5
from concurrent.futures import ProcessPoolExecutor, wait
import zerorpc
from logger import log
HOST = "0.0.0.0"
PORT = 5000
WORKER = 4


def _md5_func(text: str) -> str:
    """md5哈希."""
    start = time.time()
    result = md5(text.encode("utf-8")).hexdigest()
    end = time.time()
    log.info("time it", seconds=end - start)
    return result


def main():
    with ProcessPoolExecutor(WORKER) as executor:
        class HelloRPC:
            def md5_func(self, text: str) -> str:
                fut = executor.submit(_md5_func, text)
                wait([fut])
                return fut.result()

        s = zerorpc.Server(HelloRPC())
        s.bind(f"tcp://{HOST}:{PORT}")
        s.run()


if __name__ == "__main__":
    main()
    
```


需要注意的是zerorpc的host不能是`localhost`,通常我们使用`0.0.0.0`

### 客户端


```python
import zerorpc

HOST = "127.0.0.1"
PORT = 5000

c = zerorpc.Client()
c.connect(f"tcp://{HOST}:{PORT}")
print(c.md5_func("这是一个测试"))
```

同样的,zerorpc的host不能是`localhost`,我们得使用`127.0.0.1`

## 响应流

我们用例子[C1](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/RPC%E6%9C%8D%E5%8A%A1/code/ZERORPC%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/C1)来展示,这次我们输入的是字符串列表,返回的则是每个字符串的md5值


+ server.py


```python
...

class HelloRPC:

    def _stream_md5(self, texts: List[str]) -> Iterator[str]:
        for text in texts:
            fut = executor.submit(_md5_func, text)
            wait([fut])
            yield fut.result()

    @zerorpc.stream
    def streaming_md5(self, texts: List[str]) -> Iterator[str]:
        return self._stream_md5(texts)
```

返回流只需要将函数打上`zerorpc.stream`装饰器,并且返回一个迭代器即可.

+ client.py

```python
import zerorpc

HOST = "127.0.0.1"
PORT = 5000

c = zerorpc.Client()
c.connect(f"tcp://{HOST}:{PORT}")
for item in c.streaming_md5(["测试1","测试2","测试3"]):
    print(item)
```

调用方式也简单,
