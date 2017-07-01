import asyncio
import aiozmq.rpc

async def go():
    client = await aiozmq.rpc.connect_rpc(
        connect='tcp://127.0.0.1:5555')

    ret = await client.call.remote_func(1, 2)
    assert 3 == ret
    print(ret)
    C = await client.call.remote_func2()
    print(C)

    client.close()

asyncio.get_event_loop().run_until_complete(asyncio.wait([go() for i in range(10)]))
