import asyncio
from aiozmq import rpc

class Handler(rpc.AttrHandler):

    @rpc.method
    def remote(self, arg1, arg2):
        return arg1 + arg2

@asyncio.coroutine
def go():
    server =  yield from rpc.serve_rpc(Handler(),
                                       bind='tcp://127.0.0.1:5555')

    client = yield from rpc.connect_rpc(connect='tcp://127.0.0.1:5555')

    ret = yield from client.call.remote(1, 2)
    print(ret)
    asyncio.sleep(1)
    assert ret == 3

asyncio.get_event_loop().run_until_complete(go())
