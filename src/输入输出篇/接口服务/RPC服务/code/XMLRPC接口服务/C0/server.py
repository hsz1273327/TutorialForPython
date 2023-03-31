import time
from hashlib import md5
from http import HTTPStatus
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
from logger import log


HOST = "localhost"
PORT = 5000

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/XMLRPC',)
    def log_error(self, format, *args):
        """Log an error.

        This is called when a request cannot be fulfilled.  By
        default it passes the message on to log_message().

        Arguments are the same as for log_message().

        XXX This should go to the separate error log.

        """
        log.error("server error",address=self.address_string(),errormsg=format%args)

    def log_request(self, code='-', size="-"):
        """Log an accepted request.

        This is called by send_response().

        """
        if isinstance(code, HTTPStatus):
            code = code.value
        log.info("request info",address=self.address_string(),requestline=self.requestline, code=str(code), size=str(size))

class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def md5_func(text: str)->str:
    """md5哈希."""
    start = time.time()
    result = md5(text.encode("utf-8")).hexdigest()
    end = time.time()
    log.info("time it",seconds=end-start)
    return result


def main():
    with ThreadingXMLRPCServer((HOST, PORT), requestHandler=RequestHandler, allow_none=True) as server:
        # 注册所有可调用函数的名字到system.listMethods方法
        # 注册可调用函数的docstring到system.methodHelp(func_name)方法
        # 注册可调用函数的签名到system.methodSignature(func_name)方法
        server.register_introspection_functions()

        # 这个函数的作用是可以使客户端同时调用服务端的的多个函数。
        server.register_multicall_functions()

        # 注册一个函数,使它可以被调用,后面的字符串就是被调用的函数名
        server.register_function(md5_func, md5_func.__name__)
        try:
            log.info("server start", msg=f"xmlrpc start @ {HOST}:{PORT}!")
            server.serve_forever()
        except Exception:
            log.info("server error", exc_info=True, stack_info=True)
            raise
        finally:
            log.info("server stoped", msg=f"xmlrpc @ {HOST}:{PORT} stoped!")


if __name__ == "__main__":
    main()
    