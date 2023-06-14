import asyncio


async def main():
    count = 0
    loop = asyncio.get_event_loop()
    while True:
        count += 1
        print("ok")
        await asyncio.sleep(1)
        if count == 3:
            context = {
                'message': '错误消息',
                'exception': AttributeError('错误消息')
            }
            loop.call_exception_handler(context)


def AttributeErrorHaddler(loop, context):
    loop.call_exception_handler(context)


loop = asyncio.get_event_loop()
loop.set_exception_handler(lambda loop, context: print(context))
loop.run_until_complete(main())
