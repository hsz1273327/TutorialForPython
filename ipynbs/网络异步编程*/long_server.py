from functools import partial
import asyncio
import random

class LongServer(asyncio.StreamReaderProtocol):
    
    def _calcul(self,data,remote):
        if data> remote:
            self._stream_writer.write(b"y")
        elif data==remote:
            self._stream_writer.write(b"x")
        else:
            self._stream_writer.write(b"z")
    
    
    async def hander(self):
        while True:
            print("wait")
            data = await self._stream_reader.read(1)
            data = int(data)
            print('recv: {}'.format(data))
            remote = random.choice([1,2,3])
            print("remot: {}".format(remote))
            if remote == 3 and data == 1:
                self._stream_writer.write(b"y")
            else:
                self._calcul(data,remote)
            print('send done')
        
    
    def __init__(self,stream_reader, client_connected_cb=None,loop=None):
        self.task = None
        super().__init__(stream_reader, client_connected_cb=client_connected_cb,loop=loop)
        
        
    def connection_made(self, transport):
        super().connection_made(transport)
        self._stream_writer = asyncio.StreamWriter(transport, self,
                                               self._stream_reader,
                                               self._loop)
        self.task = asyncio.ensure_future(self.hander())
        print("set task")
        
        
    def connection_lost(self, exc):
        self.task.cancle()
        self.task = None
        super().connection_lost(exc)
        
if __name__=="__main__":
    loop = asyncio.get_event_loop()
    stream_reader = asyncio.StreamReader(loop=loop)
    # Each client connection will create a new protocol instance
    long_server = partial(LongServer,stream_reader =stream_reader,loop=loop)
    coro = loop.create_server(long_server, '127.0.0.1', 5000)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()      