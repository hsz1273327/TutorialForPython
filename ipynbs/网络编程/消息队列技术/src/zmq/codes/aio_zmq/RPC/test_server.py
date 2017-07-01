import asyncio
import aiozmq.rpc
import time


class ServerHandler(aiozmq.rpc.AttrHandler):

    def __init__(self):
        self.N = 0

    @aiozmq.rpc.method
    def remote_func(self, a:int, b:int) -> int:
        print(self.N)
        self.N += 1
        return a + b



loop = asyncio.get_event_loop()
coro = aiozmq.rpc.serve_rpc(ServerHandler(), bind='tcp://127.0.0.1:5555')
server = loop.run_until_complete(coro)
print('Serving on {}'.format('tcp://127.0.0.1:5555'))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
