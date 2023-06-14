import sys
import zmq
from multiprocessing import Process
import time

msg_list = []
for i in range(10000):
    msg_list.append("result.Test_data")

def worker():
    context = zmq.Context()
    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://127.0.0.1:5557")
 
    for _ in range(10000):
        work_receiver.recv_pyobj()
 
def main():
    p = Process(target=worker, args=())
    p.start()
    context = zmq.Context()
    ventilator_send = context.socket(zmq.PUSH)
    ventilator_send.bind("tcp://127.0.0.1:5557")
    for _ in range(10000):
        ventilator_send.send_pyobj(msg_list)
    p.join()
 
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    msg_per_sec = 1000000 / duration
 
    print(f"Duration: {duration}")
    print(f"Messages Per Second: {msg_per_sec}")
