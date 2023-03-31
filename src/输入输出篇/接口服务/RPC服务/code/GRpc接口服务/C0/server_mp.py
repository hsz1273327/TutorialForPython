#!/usr/bin/env python
import time
from concurrent import futures
import grpc
from data_pb2_grpc import SquareServiceServicer, add_SquareServiceServicer_to_server
from data_pb2 import Message

Executor = futures.ProcessPoolExecutor(max_workers=3)

HOST = "0.0.0.0"
PORT = 5000
ONE_DAY_IN_SECONDS = 60 * 60 * 24

def square(n:int):
    return n**2


class SquareServic(SquareServiceServicer):
    def square(self, request, context):
        f = Executor.submit(square,request.message)
        futures.as_completed(f)
        result = f.result()
        return Message(message=result)

def main():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SquareServiceServicer_to_server(SquareServic(), grpcServer)
    print(f'"msg":"grpc start @ grpc://{HOST}:{PORT}"')
    grpcServer.add_insecure_port(f"{HOST}:{PORT}")
    grpcServer.start()
    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)
        Executor.shutdown()
    except Exception as e:
        grpcServer.stop(0)
        Executor.shutdown()
        raise

if __name__ == "__main__":
    main()