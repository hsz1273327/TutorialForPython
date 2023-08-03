import time
import multiprocessing

CONSUMER_COUNT = 4

def consumer(cond):
    t = multiprocessing.current_process()
    with cond:
        cond.wait()  # wait()方法创建了一个名为waiter的锁，
        #并且设置锁的状态为locked。这个waiter锁用于线程间的通讯
        print(f'{t.name}: Resource is available to consumer')
def producer(cond):
    t = multiprocessing.current_process()
    for i in range(CONSUMER_COUNT):
        # 一次唤醒一个消费者
        print(f'{t.name}: wait 2s')
        time.sleep(2)
        with cond:
            print(f'{t.name}: Making resource available')
            cond.notify()  # 释放waiter锁，唤醒消费者
        
if __name__=='__main__':
    condition = multiprocessing.Condition()
    processes = []
    for i in range(CONSUMER_COUNT):
        c = multiprocessing.Process(name=f'c{i}', target=consumer, args=(condition,))
        c.start()
        processes.append(c)

    p = multiprocessing.Process(name='p', target=producer, args=(condition,))
    p.start()
    processes.append(p)
    for t in processes:
        t.join()
