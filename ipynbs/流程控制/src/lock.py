import multiprocessing  
import sys  
  
def worker_with(lock, f):  
    with lock:  
        with open(f,"a+") as fs:
            fs.write('Lock acquired via with\n')  

if __name__ == '__main__':
    f = "source/file.txt"  
    lock = multiprocessing.Lock()  
    w = multiprocessing.Process(target=worker_with, args=(lock, f))  
    w.start()  
    w.join()