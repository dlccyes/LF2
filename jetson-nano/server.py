import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import sdvs_pb2
import sdvs_pb2_grpc

import gstreamer


class SdvsServicer(sdvs_pb2_grpc.SDVSServicer):

    def __init__(self):
        self.gst = gstreamer.Gstreamer()

    def Compute(self, request, context):
        n = request.algo
        res = n

        
        if not self.gst.started:
            self.gst.start()

        self.gst.change_algo(n)

        response = sdvs_pb2.SdvsResponse()
        response.res = res

        return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8080, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = SdvsServicer()
    sdvs_pb2_grpc.add_SDVSServicer_to_server(servicer, server)

    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        server.wait_for_termination()

    except KeyboardInterrupt:
        servicer.gst.change_algo("terminate")
