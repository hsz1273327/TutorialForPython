import zerorpc

HOST = "127.0.0.1"
PORT = 5000

c = zerorpc.Client()
c.connect(f"tcp://{HOST}:{PORT}")
print(c.md5_func("这是一个测试"))