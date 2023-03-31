# grpc req_stream-res_stream

这个例子是grpc简单的应用.一个请求流对应一个响应流.请求结束后返回响应流

## 编译proto

```shell
python -m grpc_tools.protoc -I=pbschema --python_out=. --grpc_python_out=. data.proto
```

## 使用

建议在虚拟环境下使用

1. `pip install -r requirements.txt`安装依赖
2. `python server.py`启动服务端
3. `python cli_sync.py`启动同步客户端
4. `python cli_async.py`启动异步客户端