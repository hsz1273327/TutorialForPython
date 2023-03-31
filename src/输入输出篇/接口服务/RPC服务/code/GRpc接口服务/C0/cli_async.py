#!/usr/bin/env python
import asyncio
from aiogrpc import insecure_channel
from data_pb2_grpc import SquareServiceStub
from data_pb2 import Message

url = "localhost:5000"

async def query():
    async with insecure_channel(url) as conn:
        client = SquareServiceStub(channel=conn)
        result = await client.square(Message(message=12.3))
        print(result)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(query())


if __name__ == "__main__":
    main()
