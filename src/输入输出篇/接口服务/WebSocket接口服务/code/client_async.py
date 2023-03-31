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
                #break
            else:
                count += 1
            print(message)


asyncio.get_event_loop().run_until_complete(hello())