
import asyncio
import aiozmq
import zmq
import time
port = "5556"
addr = "tcp://0.0.0.0:{port}".format(port=port)
#addr = "tcp://0.0.0.0:*"
async def main():
    client = await aiozmq.create_zmq_stream(zmq.PAIR)
    
    await client.transport.connect(addr)
    #await asyncio.sleep(1)
    msg = await  client.read()
    print("Async client read: {msg}".format(msg=msg))
    server.write("client message to server".encode("utf-8").split())
    server.write("client message to server".encode("utf-8").split())
    asyncio.sleep(1)
    client.close()

if __name__=="__main__":
    asyncio.get_event_loop().run_until_complete(main())
