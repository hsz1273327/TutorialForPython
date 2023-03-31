import os
from multiprocessing import Process
import random
import time
import signal

def worker(i):
    print(f"worker {i} waiting for SIGCONT")
    signal.sigwait({signal.SIGCONT})
    print(f"end worker process {i}")


workers = {}
for i in range(5):
    p = Process(target=worker, args=(i,))
    p.daemon = True
    p.start()
    workers[p.pid] = p

time.sleep(1)
chose = random.choice(list(workers.keys()))
print(f"send to pid {chose}")
os.kill(chose, signal.SIGCONT)
print("closed")
