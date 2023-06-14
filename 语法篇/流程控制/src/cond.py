import time
import multiprocessing
def consumer(cond):
    t = multiprocessing.current_process()
    with cond:
        cond.wait()  # wait()方法创建了一个名为waiter的锁，
        #并且设置锁的状态为locked。这个waiter锁用于线程间的通讯
        print('{}: Resource is available to consumer'.format(t.name))
def producer(cond):
    t = multiprocessing.current_process()
    with cond:
        print('{}: Making resource available'.format(t.name))
        cond.notify_all()  # 释放waiter锁，唤醒消费者
        
if __name__=='__main__':
    condition = multiprocessing.Condition()
    c1 = multiprocessing.Process(name='c1', target=consumer, args=(condition,))
    c2 = multiprocessing.Process(name='c2', target=consumer, args=(condition,))
    p = multiprocessing.Process(name='p', target=producer, args=(condition,))
    c1.start()
    time.sleep(1)
    c2.start()
    time.sleep(1)
    p.start()