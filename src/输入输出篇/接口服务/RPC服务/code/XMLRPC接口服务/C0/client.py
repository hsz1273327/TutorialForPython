import xmlrpc.client

HOST = "localhost"
PORT = 5000

with xmlrpc.client.ServerProxy(f"http://{HOST}:{PORT}/XMLRPC") as proxy:
    result = proxy.md5_func("这是一个测试")

print(result)