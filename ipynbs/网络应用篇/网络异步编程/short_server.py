import asyncio
class MyServerProtocol(asyncio.Protocol):
    HANDLERS = {
        "a":lambda x:x**2,
        "b":lambda x:x*x*x,
        "c":lambda x:x*x*x*x,
        "d":lambda x:x,
    }
    
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        
        
    def _decoder(self,data):
        message = data.decode()
        result = self.HANDLERS.get(message[0])(float(message[1:]))
        return result
    
    def _encoder(self,query,num):
        message = query+str(num)
        return message.encode()

    def data_received(self, data):
        result =self._decoder(data)
        self.transport.write(self._encoder("d",result))
        
    def connection_lost(self, exc):
        print('The client closed the connection')

if __name__=="__main__":
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(MyServerProtocol, '127.0.0.1', 5000)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()