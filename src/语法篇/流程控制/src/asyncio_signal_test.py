import signal
import asyncio
signal.alarm(4)
loop = asyncio.get_event_loop()

loop.add_signal_handler(signal.SIGALRM,lambda : print("闹铃响了"))
async def main():
    while True:
        await asyncio.sleep(1)

loop.run_until_complete(main())