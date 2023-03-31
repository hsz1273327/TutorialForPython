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
