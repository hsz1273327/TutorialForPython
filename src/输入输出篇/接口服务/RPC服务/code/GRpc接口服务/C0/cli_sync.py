#!/usr/bin/env python
import grpc
from data_pb2_grpc import SquareServiceStub
from data_pb2 import Message
url = "localhost:5000"
conn = grpc.insecure_channel(url)
client = SquareServiceStub(channel=conn)
result = client.square(Message(message=12.3))
print(result)