
import asyncio
import aiozmq
import zmq

port = "5556"
addr = "tcp://0.0.0.0:{port}".format(port=port)
async def main():
    server = await aiozmq.create_zmq_stream(
        zmq.PAIR,
        bind=addr)
    print(list(server.transport.bindings())[0])
    while True:
        server.write("Server message to client".encode("utf-8").split())
        try:
            data = await server.read()
        except asyncio.CancelledError:
            break
        print("Async server read: {data}".format(data=data))
        asyncio.sleep(1)
    server.close()

if __name__=="__main__":
    print("sever is running on {addr}".format(addr=addr))
    asyncio.get_event_loop().run_until_complete(main())
