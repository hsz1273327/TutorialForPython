import time
import multiprocessing 
from random import randint

CONSUMER_COUNT = 4

def consumer(evt):
    TIMEOUT = 3
    t = multiprocessing.current_process()
    evt.wait(TIMEOUT)
    print(f'{t.name}: Resource is available to consumer')
        
def producer(evt):
    t = multiprocessing.current_process()
    print(f'{t.name}: wait 2s')
    time.sleep(2)
    print(f'{t.name}: Making resource available')
    evt.set()  # 设置事件唤醒消费者


if __name__ == '__main__':
    evt = multiprocessing.Event() 
    processes = []
    for i in range(CONSUMER_COUNT):
        t = multiprocessing.Process(name=f"c{i}", target=consumer, args=(evt,))
        t.start()
        processes.append(t)
    p = multiprocessing.Process(name='p', target=producer, args=(evt,))
    p.start()
    processes.append(p)
    for t in processes:
        t.join()
