import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
import sdvs_pb2
import sdvs_pb2_grpc

from scanner import read_scanner

def main(args):
    host = f"{args['ip']}:{args['port']}"
    print(host)
    with grpc.insecure_channel(host) as channel:
        stub = sdvs_pb2_grpc.SDVSStub(channel)

        request = sdvs_pb2.SdvsRequest()
        request.algo = args['algo']

        response = stub.Compute(request)
        print(response.res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8080)
    args = vars(parser.parse_args())
    
    args["algo"] = "start"
    main(args)

    while(True):
        try:
            print("Scan your student ID card.\n")
            student_id = read_scanner()

            args["algo"] = student_id
            main(args)

        except KeyboardInterrupt:
            args["algo"] = "terminate"
            main(args)
            break      
