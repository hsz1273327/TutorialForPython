import asyncio
import signal

def handler(arg):
    print("handler", arg)
    loop.stop()

loop = asyncio.ProactorEventLoop()
loop.add_signal_handler(signal.SIGINT, handler, "abc")
loop.run_forever()
loop.remove_signal_handler(signal.SIGINT)
loop.close()
