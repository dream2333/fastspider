import sys
from  multiprocessing import Process, Pipe
import time



msg_list = []
for i in range(100):
    msg_list.append("result.Test_data")

def worker(receiver): 
    for _ in range(10000):
        receiver.recv()
 
    sys.exit(1)
 
def main():
    receiver, sender = Pipe(duplex=False)
    p = Process(target=worker, args=(receiver,))
    p.start()
    for _ in range(10000):
        sender.send(msg_list)
    sender.close()
    p.join()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    msg_per_sec = 1000000 / duration
 
    print(f"Duration: {duration}")
    print(f"Messages Per Second: {msg_per_sec}")
