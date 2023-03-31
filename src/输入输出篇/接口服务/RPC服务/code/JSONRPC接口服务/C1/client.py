import jsonrpclib

HOST = "localhost"
PORT = 5000


url = "http://localhost:5000/JSONRPC"

with jsonrpclib.ServerProxy(url) as cli:
     result = cli.md5_func("这是一个测试")
print(result)