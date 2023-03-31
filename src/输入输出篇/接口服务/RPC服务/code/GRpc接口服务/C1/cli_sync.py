#!/usr/bin/env python
import grpc
from data_pb2_grpc import SquareServiceStub
from data_pb2 import Message
url = "localhost:5000"
conn = grpc.insecure_channel(url)
client = SquareServiceStub(channel=conn)
for i in client.rangeSquare(Message(message=12)):
    print(i.message)