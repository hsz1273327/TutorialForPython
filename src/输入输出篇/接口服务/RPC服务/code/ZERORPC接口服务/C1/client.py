import zerorpc

HOST = "127.0.0.1"
PORT = 5000

c = zerorpc.Client()
c.connect(f"tcp://{HOST}:{PORT}")
for item in c.streaming_md5(["测试1","测试2","测试3"]):
    print(item)