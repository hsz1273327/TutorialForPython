import time
from multiprocessing import Process
from random import randint
from multiprocessing import Queue

q = Queue(10)

def double(n):
    return n * 2
def producer():
    count = 0
    while True:
        if count > 5:
            break
        pri = randint(0, 100)
        print('put :{}'.format(pri))
        q.put((pri, double, pri))  # (priority, func, args)
        count += 1
def consumer():
    while True:
        if q.empty():
            break
        pri, task, arg = q.get()
        print('[PRI:{}] {} * 2 = {}'.format(pri, arg, task(arg)))
        q.task_done()
        time.sleep(0.1)
        
if __name__=='__main__':
    t = Process(target=producer)
    t.start()
    time.sleep(1)
    t = Process(target=consumer)
    t.start()