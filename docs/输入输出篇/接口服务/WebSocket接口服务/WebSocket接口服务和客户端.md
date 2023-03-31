
# WebSocket接口服务

当我们希望向客户端推送数据时,websocket接口服务是我们最常用也最合适的应用层协议.当然不是说websocket不能用于请求响应模式的接口服务,只是推送数据更适合它.

python下最合适写Websocket接口服务的是包[websockets](https://github.com/aaugustin/websockets),这是一个基于asyncio的websocket包.

一个典型的[例子](https://github.com/TutorialForPython/python-io/tree/master/%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/WebSocket%E6%8E%A5%E5%8F%A3%E6%9C%8D%E5%8A%A1/code)--我们每秒向客户端推送当前的时间:

+ `server.py`:

```python
import asyncio
import datetime
import json
import websockets
from websockets.exceptions import (
    ConnectionClosedError,
    ConnectionClosedOK,
    ConnectionClosed
)

from logger import log

ROOMS = {
    "/nowtime": set()
}
HOST = 'localhost'
PORT = 5000


async def notify_user(websocket, path, message):
    """广播用户加入了房间"""
    if ROOMS.get(path):
        message = json.dumps({
            "status": 200,
            "event": "notification",
            "data": message
        })
        await websocket.send(message)


async def join_room(websocket, path) -> bool:
    room = ROOMS.get(path)
    if isinstance(room, set):
        room.add(websocket)
        await notify_user(websocket, path, "Welcom")
        return True
    else:
        await notify_user(websocket, path, "Unknown url")
        return False


async def leave_room(websocket, path) -> bool:
    room = ROOMS.get(path)
    if isinstance(room, set):
        if websocket in room:
            room.remove(websocket)
            log.info(f"Leave Room {path}")
            return True
        else:
            log.info(f"user not in Room {path}")
            return False
    else:
        log.info("Unknown url")
        return False


async def send_time(websocket):
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        data = {
            "data": now,
            "event": "nowtime",
            "status": 200
        }
        await websocket.send(json.dumps(data))
        await asyncio.sleep(3)


async def listen_close(websocket, task):
    async for message in websocket:
        if json.loads(message).get("event") == "close":
            log.info("get event close from client")
            break
    try:
        task.cancel()
    except Exception as e:
        log.info(f"set task a exception error {type(e)} {str(e)}")
    else:
        log.info("set task a exception")


async def nowtime(websocket, path):
    loop = asyncio.get_event_loop()
    log.info(path)
    is_in_room = await join_room(websocket, path)
    if is_in_room:
        task = loop.create_task(send_time(websocket))
        task.add_done_callback(lambda x: log.info("done"))
        listener = loop.create_task(listen_close(websocket, task))
        try:
            await task
        except asyncio.CancelledError as ce:
            log.info("client closed connection itself")
            await websocket.send(json.dumps({"message":"bye"}))
        except ConnectionClosedError as close_error:
            log.info("client force closed connection ")
        except ConnectionClosedOK as close_ok:
            log.info("client closed connection")
        except ConnectionClosed as close:
            log.info("client closed connection finally")
        except Exception as e:
            raise e
        finally:
            listener.cancel()
            await leave_room(websocket, path)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(nowtime, HOST, PORT))

log.info(f"server start @ {HOST}:{PORT}")
asyncio.get_event_loop().run_forever()
```


我们通过`websockets.serve(handdler,host,port)`构造项目,handdler是一个有参数`websocket`和`path`的函数,其中`path`是访问服务时指定的uri,`websocket`则是客户端和服务端的连接对象.


websocket无非是两个操作:

+ 监听消息:`async for message in websocket:`

+ 发送消息:`websocket.send(str)`



这个例子中我们使用url来构造room的概念,每个连接可以加入或退出一个room.每个room实际是一个set对象,当建立连接时我们根据url判断加入的room,当客户端退出时我们将这个对象从room中删除.有了这个room来存放连接集合,我们就可以很方便的做广播--遍历room中的连接对象每个都发送相同的消息即可.



## websocket客户端

我们实现收到10条信息后发送一个close事件让服务端关闭这个连接.


### 异步客户端

websockets包同样提供了异步的客户端,:

+ `client_async.py`:

```python
import asyncio
import json
import websockets

async def hello():
    uri = "ws://localhost:5000/nowtime"
    async with websockets.connect(uri) as websocket:
        count = 0
        async for message in websocket:
            if websocket.closed:
                break
            if count == 10:
                await websocket.send(json.dumps({"event":"close"}))
                print("send close")
            else:
                count += 1
            print(message)


asyncio.get_event_loop().run_until_complete(hello())
```
    
websockets包客户端的`websocket`对象和服务端一致.

### 同步客户端

[websocket-client](https://github.com/websocket-client/websocket-client)提供了同步客户端.

+ `client_sync.py`

```python
import json
import websocket

ws = websocket.create_connection("ws://localhost:5000/nowtime")
try:
    count = 0
    for message in ws:
        if not ws.connected:
            break
        if count == 10:
            ws.send(json.dumps({"event":"close"}))
            print("send close")
        else:
            count += 1
        print(message)
except Exception:
    ws.close()
```


```python

```
