import multiprocessing  
import sys  
  
def worker_with(lock, f, pid):  
    with lock:  
        with open(f,"a+") as fs:
            fs.write(f'Lock acquired via with {pid}\n')
        print(f"Lock acquired via with {pid}")

if __name__ == '__main__':
    f = "source/file.txt"
    with open(f,"w") as fs:
        fs.write("")
    lock = multiprocessing.Lock()  
    processes = []
    for i in range(5):
        t = multiprocessing.Process(target=worker_with, args=(lock, f,i))
        processes.append(t)
    for t in processes:     
        t.start()
    for t in processes:
        t.join()
