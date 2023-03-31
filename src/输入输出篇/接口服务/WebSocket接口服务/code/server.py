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
