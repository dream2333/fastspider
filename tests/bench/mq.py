import sys
import zmq
from multiprocessing import Process
import time


def worker():
    context = zmq.Context(1)
    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://127.0.0.1:5557")
 
    while True:
        result = work_receiver.recv_pyobj()
        if result == b'exit':
            print(result)
            sys.exit(1)
 
 
def main():
    p = Process(target=worker, args=())
    p.start()
    context = zmq.Context()
    ventilator_send = context.socket(zmq.PUSH)
    ventilator_send.bind("tcp://127.0.0.1:5557")
    for msg in range(500000):
        ventilator_send.send_pyobj(["result.Test_data"])
    ventilator_send.send_pyobj(b'exit')
    p.join()
 
if __name__ == "__main__":
    start_time = time.monotonic()
    main()
    end_time = time.monotonic()
    duration = end_time - start_time
    print(f"Duration: {duration}")

