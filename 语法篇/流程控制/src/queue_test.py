import time
from multiprocessing import Process, JoinableQueue
from random import randint

q = JoinableQueue(10)

def double(n):
    return n * 2

def producer(q):
    print("producer started")
    count = 0
    while True:
        if count > 5:
            break
        pri = randint(0, 100)
        print(f'put :{pri}')
        q.put((pri, double, pri))  # (priority, func, args)
        count += 1
        
def consumer(q):
    print("consumer started")
    while True:
        if q.empty():

            break
        pri, task, arg = q.get()
        print(f'[PRI:{pri}] {arg} * 2 = {task(arg)}')
        q.task_done()
        time.sleep(0.1)
        
if __name__=='__main__':
    processes = []
    p = Process(target=producer,args=(q,))
    p.start()
    processes.append(p)
    time.sleep(1)
    c = Process(target=consumer,args=(q,))
    c.start()
    processes.append(c)
    for t in processes:
        t.join()
