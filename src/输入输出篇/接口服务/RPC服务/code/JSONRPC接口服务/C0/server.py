import time
from hashlib import md5
from http import HTTPStatus
from jsonrpclib.SimpleJSONRPCServer import PooledJSONRPCServer
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCRequestHandler
from jsonrpclib.threadpool import ThreadPool
from logger import log

HOST = "localhost"
PORT = 5000


class RequestHandler(SimpleJSONRPCRequestHandler):
    rpc_paths = ('/JSONRPC',)

    def log_error(self, format, *args):
        """Log an error.

        This is called when a request cannot be fulfilled.  By
        default it passes the message on to log_message().

        Arguments are the same as for log_message().

        XXX This should go to the separate error log.

        """
        log.error("server error", address=self.address_string(), errormsg=format % args)

    def log_request(self, code='-', size="-"):
        """Log an accepted request.

        This is called by send_response().

        """
        if isinstance(code, HTTPStatus):
            code = code.value
        log.info("request info", address=self.address_string(), requestline=self.requestline, code=str(code), size=str(size))


def md5_func(text: str) -> str:
    """md5哈希."""
    start = time.time()
    result = md5(text.encode("utf-8")).hexdigest()
    end = time.time()
    log.info("time it", seconds=end - start)
    return result


def main():
    nofif_pool = ThreadPool(max_threads=10, min_threads=0)
    request_pool = ThreadPool(max_threads=50, min_threads=10)
    with PooledJSONRPCServer((HOST, PORT), thread_pool=request_pool, requestHandler=RequestHandler) as server:
        # 注册所有可调用函数的名字到system.listMethods方法
        # 注册可调用函数的docstring到system.methodHelp(func_name)方法
        # 注册可调用函数的签名到system.methodSignature(func_name)方法
        server.register_introspection_functions()
        server.set_notification_pool(nofif_pool)

        # 这个函数的作用是可以使客户端同时调用服务端的的多个函数。
        server.register_multicall_functions()
        server.register_function(md5_func, md5_func.__name__)
        try:
            nofif_pool.start()
            request_pool.start()
            log.info("server start", msg=f"jsonrpc start @ {HOST}:{PORT}!")
            server.serve_forever()
        except Exception:
            raise
        finally:
            request_pool.stop()
            nofif_pool.stop()
            server.set_notification_pool(None)
            log.info("server stoped", msg=f"jsonrpc @ {HOST}:{PORT} stoped!")


if __name__ == "__main__":
    main()
