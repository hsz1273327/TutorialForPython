import asyncio
from signal import (
    SIGTERM, SIGINT,
    signal as signal_func,
    Signals
)

class Signal:
    stopped = False

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

#loop = asyncio.get_event_loop()
loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)
# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 3000)
server = loop.run_until_complete(coro)
signal=Signal()
register_sys_signals=True
# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
if register_sys_signals:
    for _signal in (SIGINT, SIGTERM):
        try:
            loop.add_signal_handler(_signal, loop.stop)
        except NotImplementedError:
            print('Sanic tried to use loop.add_signal_handler but it is'
                     ' not implemented on this platform.')

try:
    loop.run_forever()
finally:
    server.close()
    loop.run_until_complete(server.wait_closed())
    signal.stopped = True
    loop.close()


# Close the server
