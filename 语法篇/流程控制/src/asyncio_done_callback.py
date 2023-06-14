import asyncio
import random
loop = asyncio.get_event_loop()


async def never_end():
    while True:
        await asyncio.sleep(1)
        if random.random() >0.8:
            raise AssertionError("意外退出")
async def main():
    task = asyncio.create_task(never_end())
    task.add_done_callback(lambda x: print(f"task done with exception {x.exception()}"))
    while True:
        await asyncio.sleep(1)

loop.run_until_complete(main())
