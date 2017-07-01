import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
addr = "tcp://0.0.0.0:{port}".format(port=port) 
socket.bind(addr)
print("sever is running on {addr}".format(addr=addr))
while True:
    socket.send(b"Server message to client")
    msg = socket.recv()
    print(msg)
    time.sleep(1)