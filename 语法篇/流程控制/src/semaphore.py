from multiprocessing import Process, Semaphore

def foo(tid,sema):
    import time
    from random import random
    with sema:
        print('{} acquire sema'.format(tid))
        wt = random() * 2
        time.sleep(wt)
    print('{} release sema'.format(tid))
    
if __name__ == "__main__":
    sema = Semaphore(3)
    processes = []
    for i in range(5):
        t = Process(target=foo, args=(i,sema))
        processes.append(t)

    for t in processes:     
        t.start()
    for t in processes:
        t.join()