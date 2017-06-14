import asyncio
import functools
import signal

def sigint_handler():
    print("got SIGINT: stop")
    loop.stop()

def sigbreak_handler():
    print("got SIGBREAK: stop")
    loop.stop()

loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGINT, sigint_handler)
loop.add_signal_handler(signal.SIGBREAK, sigbreak_handler)
loop.run_forever()
loop.remove_signal_handler(signal.SIGINT)
loop.remove_signal_handler(signal.SIGBREAK)
loop.close()
