import threading
import random
import time
import signal

def worker(i):
    print(f"worker {i} waiting for SIGCONT")
    signal.sigwait({signal.SIGCONT})
    print(f"end worker thread {i}")


workers = {}
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    workers[t.ident] = t

time.sleep(1)
chose = random.choice(list(workers.keys()))
print(f"send to tid {chose}")
signal.pthread_kill(chose, signal.SIGCONT)
print("closed")
