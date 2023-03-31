#!/usr/bin/env python
import time
from concurrent import futures
import grpc
from data_pb2_grpc import SquareServiceServicer, add_SquareServiceServicer_to_server
from data_pb2 import Message


HOST = "0.0.0.0"
PORT = 5000
ONE_DAY_IN_SECONDS = 60 * 60 * 24

class SquareServic(SquareServiceServicer):
    def square(self, request, context):
        return Message(message=request.message**2)



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
    except Exception as e:
        grpcServer.stop(0)
        raise

if __name__ == "__main__":
    main()