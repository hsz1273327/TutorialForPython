#!/usr/bin/env python
import asyncio
from aiogrpc import insecure_channel
from data_pb2_grpc import SquareServiceStub
from data_pb2 import Message

url = "localhost:5000"

async def query():
    async with insecure_channel(url) as conn:
        client = SquareServiceStub(channel=conn)
        async for response in client.rangeSquare(Message(message=12)):
            print(response.message)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(query())


if __name__ == "__main__":
    main()
