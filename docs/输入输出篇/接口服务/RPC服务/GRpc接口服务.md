
# GRpc接口服务

GRpc正如其名,是一种RPC.它实际上和RESTful接口在功能上是相近的,本质都是一种请求响应模式的服务.只是作为一个RPC,GRpc一般描述动作而非资源,并且它可以返回的不光是一个数据,而是一组流数据.

GRpc是一种跨语言的Rpc,它建立在http2上使用protobuf作为结构化数据的序列化工具.

它有4种形式:

+ 请求-响应
+ 请求-流响应
+ 流请求-响应
+ 流请求-流响应

其基本使用方式是:

1. 服务端与客户端开发者协商创建一个protobuf文件用于定义rpc的形式和方法名以及不同方法传输数据的schema
2. 编译protobuf文件至服务端客户端的实现语言
3. 服务端实现protobuf文件中定义的方法
4. 客户端调用protobuf文件中定义的方法

在python中我们使用[protobuf](https://pypi.org/project/protobuf/)和[grpcio](https://pypi.org/project/grpcio/)来编译protobuf文件.

## 请求-响应

这个例子[C0](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/RPC%E6%9C%8D%E5%8A%A1/code/GRpc%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/C0)我们来实现一个简单的服务--输入一个数,输出这个数的平方

### 创建一个protobuf文件

创建protobuf文件的语法可以看[protobuf的语法指南](https://developers.google.com/protocol-buffers/docs/proto3)

我们将函数命名为Square,每次传传入的数据是一个double型的数,传回的也是一个double型的数.

```proto
syntax = "proto3";
package squarerpc_service;

service SquareService {
    rpc square (Message) returns (Message){}
}

message Message {
    double message = 1;
}
```

### 将这个proto文件编译为python模块

要将proto文件编译为python模块我们需要工具[protoc](https://github.com/protocolbuffers/protobuf/releases)和[grpcio-tools](https://pypi.org/project/grpcio-tools/)

安装好这两个后我们可以使用如下命令将目标protobuf文件编译为

```shell
python -m grpc_tools.protoc -I=$proto_dir \
--python_out=$target_dir \
--grpc_python_out=$target_dir \
$proto_file
```

### 服务端实现定义的方法

python的grpc服务端是使用线程实现的,这也就意味着它无法承受高并发.但这通常不是rpc关注的问题,rpc一般都是要通过起多个实例做负载均衡的,同时这也要求了我们的rpc要做到无状态.

+ server.py

```python
#!/usr/bin/env python
import time
from concurrent import futures
import grpc
from data_pb2_grpc import SquareServiceServicer, add_SquareServiceServicer_to_server
from data_pb2 import Message

HOST = "0.0.0.0"
PORT = 5000
ONE_DAY_IN_SECONDS = 60 * 60 * 24

class SquareServic(SquareServiceServicer):
    def square(self, request, context):
        return Message(message=request.message**2)

def main():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SquareServiceServicer_to_server(SquareServic(), grpcServer)
    print(f'"msg":"grpc start @ grpc://{HOST}:{PORT}"')
    grpcServer.add_insecure_port(f"{HOST}:{PORT}")
    grpcServer.start()
    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)
    except Exception as e:
        grpcServer.stop(0)
        raise

if __name__ == "__main__":
    main()
```

grpc服务端写法步骤:

1. 继承我们定义的`service`名字加`Servicer`的抽象类,并实现其中的方法,姑且叫他`RPC`类
2. 使用`grpc.server(executor[,maximum_concurrent_rpcs])`创建一个服务器,executor必须使用标准库的`futures.ThreadPoolExecutor`,通过它来确定最大使用多少个worker.`maximum_concurrent_rpcs`则是用于设置最大同时处理多少个请求,当请求超过`maximum_concurrent_rpcs`的数值,name后来的请求就会被拒绝
3. 使用`add_[我们定义的service名字]Servicer_to_server(RPC类的实例,grpcServer)`
4. `grpcServer.add_insecure_port(f"{HOST}:{PORT}")`绑定ip和端口
5. `grpcServer.start()`启动服务,需要注意的是`grpcServer.start()`是启动新线程实现的,需要阻塞主线程以防止退出,因此需要有一个死循环在主线程.

#### 借助多进程提高cpu利用率

python写rpc往往是处理计算密集型任务,但GIL让rpc无法高效的利用cpu.我们来重新实现下上面的服务,让计算的部分由多进程实现

```python
Executor = futures.ProcessPoolExecutor(max_workers=3)

class SquareServic(SquareServiceServicer):
    def square(self, request, context):
        f = Executor.submit(square,request.message)
        futures.as_completed(f)
        result = f.result()
        return Message(message=result)

...

def main():
    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)
        Executor.shutdown()
    except Exception as e:
        grpcServer.stop(0)
        Executor.shutdown()
        raise
```

### 客户端实现方式

python作为客户端同样比较常见.毕竟更多的时候我们是要调用别人写的服务

客户端需要做的是

1. 连接上服务器
2. 构造一个Stub的实例
3. 调用stub实例上的对应方法并获得结果

#### 同步客户端

官方默认使用的是同步写法,比较直观

+ cli_sync.py

```python
#!/usr/bin/env python
import grpc
from data_pb2_grpc import SquareServiceStub
from data_pb2 import Message
url = "localhost:5000"
channel = grpc.insecure_channel(url)
client = SquareServiceStub(channel=channel)
result = client.square(Message(message=12.3))
print(result)
```

#### 异步客户端

grpc的客户端有两种请求有`.future()`方法可以返回`grpc.Future`,它的接口和`asyncio.Future`十分类似,但却不满足`awaitable`协议.感谢[aiogrpc](https://github.com/hubo1016/aiogrpc)为我们做了一个包装器,用它我们就可以使用协程语法了

+ cli_async.py

```python
#!/usr/bin/env python
import asyncio
from aiogrpc import insecure_channel
from data_pb2_grpc import SquareServiceStub
from data_pb2 import Message

url = "localhost:5000"

async def query():
    async with insecure_channel(url) as conn:
        client = SquareServiceStub(channel=conn)
        result = await client.square(Message(message=12.3))
        print(result)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(query())


if __name__ == "__main__":
    main()

```

### 添加ssl支持

由于python常用于做原型开发,所以很多时候它需要独立完成部署而不能借助其他工具,那ssl支持就是一个必须要考虑的问题了

grpc原生支持ssl只需要:

+ 服务端修改

    ```python
    grpcServer.add_insecure_port
    ```

    改为

    ```python
    with open('crt/example.key', 'rb') as f:
        private_key = f.read()
    with open('crt/example.crt', 'rb') as f:
        certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials(
        ((private_key, certificate_chain,),))
    grpcServer.add_secure_port(f"{HOST}:{PORT}", server_credentials)
    ```

+ 客户端修改

    ```python
    conn = grpc.insecure_channel(url)
    ```

    改为

    ```python
    with open('crt/example.crt', 'rb') as f:
        trusted_certs = f.read()
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel(url, credentials)
    ```


## 请求-流响应

这种需求比较常见,有点类似python中的range函数,它生成的是一个流而非一个数组,它会一次一条的按顺序将数据发送回请求的客户端.

这个例子[C1](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/RPC%E6%9C%8D%E5%8A%A1/code/GRpc%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/C1)实现了给出一个正整数,它会返回从0开始到它为止的每个整数的平方.

### 修改protobuf文件

```proto
service SquareService {
    rpc rangeSquare (Message) returns (stream Message){}
}
```

### 修改服务端实现

服务一端的流是一年`yield`关键字推送

```python
...
class SquareServic(SquareServiceServicer):
    def rangeSquare(self, request, context):
        print(request.message)
        for i in range(int(request.message+1)):
            yield Message(message=i**2)
```

### 修改客户端实现

我们在客户端可以直接用for循环读取返回的流

#### 同步客户端

```python
...
for i in client.rangeSquare(Message(message=12)):
    print(i.message)
```

#### 异步客户端

```python
...
async def query():
    async with insecure_channel(url) as conn:
        client = SquareServiceStub(channel=conn)
        async for response in client.rangeSquare(Message(message=12)):
            print(response.message)
...
```


## 流请求-响应

这种需求不是很多见,可能用的比较多的是收集一串数据后统一进行处理吧,流只是可以确保是同一个客户端发过来的而已.

这个例子[C2](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/RPC%E6%9C%8D%E5%8A%A1/code/GRpc%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/C2)实现了传过来一串数,之后返回他们的平方和

### 修改protobuf文件

```proto
service SquareService {
    rpc sumSquare (stream Message) returns (Message){}
}
```

### 修改服务端实现

以流为请求的服务端第二个参数为一个`iterator`,因此我们可以使用for循环来获取其中的内容

```python
...
class SquareServic(SquareServiceServicer):
    def sumSquare(self, request_iterator, context):
        result = 0
        for i in request_iterator:
            result += i.message**2
        return Message(message=result)
```

### 修改客户端实现

我们在客户端可以直接用for循环读取返回的流

#### 同步客户端

同步客户端通过将一个`iterator`作为参数来调用以流为请求的服务端

```python
...
result = client.sumSquare(Message(message=i) for i in range(12))
```

#### 异步客户端

异步客户端则接收一个异步iterator作为参数,我们可以使用`aitertools`来生成或者处理异步迭代器,如果请求流比较复杂,我们也可以创建一个异步生成器,异步语法可以看[我的这篇文章](https://tutorialforpython.github.io/%E8%AF%AD%E6%B3%95%E7%AF%87/%E6%B5%81%E7%A8%8B%E6%8E%A7%E5%88%B6/%E9%98%BB%E5%A1%9E%E5%BC%82%E6%AD%A5%E4%B8%8E%E5%8D%8F%E7%A8%8B.html#%E5%BC%82%E6%AD%A5%E8%BF%AD%E4%BB%A3%E5%99%A8%E5%92%8Casync-for)

```python
from aitertools import AsyncIterWrapper
...
response = await client.sumSquare(AsyncIterWrapper(Message(message=i) for i in range(12)))
...
```



## 流请求-流响应

将上面两种方式结合起来,就是我们的第四种方式,请求为一个流,响应也是流.这两个流可以是相互交叉的也可以是请求完后再返回一个流.他们在写pb文件时是相同的写法

```proto
service SquareService {
    rpc streamrangeSquare (stream Message) returns (stream Message){}
}
```


### 请求流完成后返回流


这个例子[C3](https://github.com/TutorialForPython/python-server/tree/master/code/GRpc%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/C3)实现了传过来一串数,之后以流的形式返回这组数每个的平方.

#### 修改服务端实现

服务端获得的请求是一个`iterator`,而返回的流则是通过yield语法推出的.

```python
...
class SquareServic(SquareServiceServicer):
    def streamrangeSquare(self, request_iterator, context):
        result = []
        for i in request_iterator:
            result.append(i.message**2)
        for j in result:
            yield Message(message=j)
```

#### 修改同步客户端

同步客户端请求的参数是一个`iterator`,返回的也是一个`iterator`

```python
...
for result in client.streamrangeSquare(Message(message=i) for i in range(12)):
    print(result)
```

#### 修改异步客户端

异步客户端请求的参数是一个`async iterator`,返回的也是一个`async iterator`

```python
async with insecure_channel(url) as conn:
    client = SquareServiceStub(channel=conn)
    async for response in client.streamrangeSquare(AsyncIterWrapper(Message(message=i) for i in range(12))):
        print(response.message)
...
```

### 请求流中返回流

这个例子[C4](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/RPC%E6%9C%8D%E5%8A%A1/code/GRpc%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/C4)实现了传过来一串数,过程中每传来一个数就返回它的平方

#### 修改服务端实现

这种其实只需要修改服务端即可,在每获得一个数据后就yield出去结果就行了

```python
...
class SquareServic(SquareServiceServicer):
    def streamrangeSquare(self, request_iterator, context):
        for i in request_iterator:
            yield Message(message=i.message**2)
```


## 总结

python的GRpc接口充分利用了python语法中的iterator协议,因此无论是服务端客户端都可以写出相当简短的服务.调用起来也最像本地的模块.
