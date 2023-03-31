#!/usr/bin/env python
import grpc
from data_pb2_grpc import SquareServiceStub
from data_pb2 import Message
with open('crt/example.crt', 'rb') as f:
    trusted_certs = f.read()

url = "localhost:5000"

credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
channel = grpc.secure_channel(url, credentials)
client = SquareServiceStub(channel=channel)
result = client.square(Message(message=12.3))
print(result)