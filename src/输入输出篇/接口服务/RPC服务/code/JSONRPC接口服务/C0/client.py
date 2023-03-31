import jsonrpclib

HOST = "localhost"
PORT = 5000


url = "http://localhost:5000/JSONRPC"

cli = jsonrpclib.ServerProxy(url)

result = cli.md5_func("这是一个测试")
cli('close')()
print(result)
