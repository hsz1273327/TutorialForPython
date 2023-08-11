# 通过WebSocket接口读写数据

我们实现收到10条信息后发送一个close事件让服务端关闭这个连接.

## 异步客户端

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


## 同步客户端

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

