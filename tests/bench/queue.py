import sys
from  multiprocessing import Process, SimpleQueue
import time


msg_list = []
for i in range(100):
    msg_list.append("result.Test_data")

def worker(q): 
    for _ in range(100000):
        q.get()
 
    sys.exit(1)
 
def main():
    q = SimpleQueue()
    p = Process(target=worker, args=(q,))
    p.start()
    for _ in range(100000):
        q.put(msg_list)
    p.join()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    msg_per_sec = 1000000 / duration
 
    print(f"Duration: {duration}")
    print(f"Messages Per Second: {msg_per_sec}")
