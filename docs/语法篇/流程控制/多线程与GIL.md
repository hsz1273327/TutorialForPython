
# 多线程与GIL

## GIL

CPython解释器本身就不是线程安全的,因此有全局解释器锁(GIL),一次只允许使用一个线程执行 Python 字节码.因此一个 Python 进程通常不能同时使用多个 CPU 核心。

编写 Python 代码时无法控制 GIL;不过,执行耗时的任务时,可以使用一个内置的函数或一个使用 C 语言编写的扩展释放GIL.其实有个使用 C 语言编写的 Python库能管理GIL,自行启动操作系统线程,利用全部可用的 CPU 核心.这样做会极大地增加库代码的复杂度,因此大多数库的作者都不这么做.

然而,标准库中所有执行阻塞型I/O操作的函数,在等待操作系统返回结果时都会释放GIL.这意味着在 Python 语言这个层次上可以使用多线程处理io阻塞问题,而 I/O 密集型 Python 程序能从中受益--一个 Python 线程等待网络响应时,阻塞型 I/O 函数会释放 GIL,再运行一个线程.

### 为什么需要GIL

GIL是必须的,这是Python设计的问题--Python解释器是非线程安全的.这意味着当从线程内尝试安全的访问Python对象的时候将有一个全局的强制锁.在任何时候,仅仅一个单一的线程能够获取Python对象或者C API.每100个字节的Python指令解释器将重新获取锁,这(潜在的)阻塞了I/O操作.因此CPU密集型的代码使用线程库时,不会获得性能的提高.


## 使用concurrent.futures进行高层抽象的多线程操作

concurrent.futures提供两种编程模型:

+ 并行任务模型
    单独任务独立使用自己的过程和数据,多任务独立并行计算

+ MapReduce模型
    为各个线程分发数据执行相同的过程
    

### 并行任务模型

这个模型使用submit提交任务到上下文管理器,之后使用返回对象的result()方法阻塞io等待任务完成


```python
from concurrent.futures import ThreadPoolExecutor,as_completed
from random import randrange
from time import time
```


```python
def arcfour(key, in_bytes, loops=20):
    """rc4算法"""
    kbox = bytearray(256)  # create key box
    for i, car in enumerate(key):  # copy key and vector
        kbox[i] = car
    j = len(key)
    for i in range(j, 256):  # repeat until full
        kbox[i] = kbox[i-j]

    # [1] initialize sbox
    sbox = bytearray(range(256))

    # repeat sbox mixing loop, as recommened in CipherSaber-2
    # http://ciphersaber.gurus.com/faq.html#cs2
    j = 0
    for k in range(loops):
        for i in range(256):
            j = (j + sbox[i] + kbox[i]) % 256
            sbox[i], sbox[j] = sbox[j], sbox[i]

    # main loop
    i = 0
    j = 0
    out_bytes = bytearray()

    for car in in_bytes:
        i = (i + 1) % 256
        # [2] shuffle sbox
        j = (j + sbox[i]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
        # [3] compute t
        t = (sbox[i] + sbox[j]) % 256
        k = sbox[t]
        car = car ^ k
        out_bytes.append(car)

    return out_bytes
```


```python
clear = bytearray(b'1234567890' * 100000)
t0 = time()
cipher = arcfour(b'key', clear)
print('elapsed time: %.2fs' % (time() - t0))
result = arcfour(b'key', cipher)
assert result == clear, '%r != %r' % (result, clear)
print('elapsed time: %.2fs' % (time() - t0))
print('OK')
```

    elapsed time: 0.47s
    elapsed time: 0.95s
    OK



```python
def crypto_process(size, key):
    in_text = bytearray(randrange(256) for i in range(size))
    cypher_text = arcfour(key, in_text)
    out_text = arcfour(key, cypher_text)
    assert in_text == out_text, 'Failed arcfour_test'
    return size
    
def main(workers=None):
    JOBS = 12
    SIZE = 2**18

    KEY = b"'Twas brillig, and the slithy toves\nDid gyre"
    STATUS = '{} workers, elapsed time: {:.2f}s'
    if workers:
        workers = int(workers)
    t0 = time()

    with ThreadPoolExecutor(workers) as executor:
        actual_workers = executor._max_workers
        to_do = []
        for i in range(JOBS, 0, -1):
            size = SIZE + int(SIZE / JOBS * (i - JOBS/2))
            job = executor.submit(crypto_process, size, KEY)
            to_do.append(job)

        for future in as_completed(to_do):
            res = future.result()
            print('{:.1f} KB'.format(res/2**10))

    print(STATUS.format(actual_workers, time() - t0))
```


```python
main(1)
```

    384.0 KB
    362.7 KB
    341.3 KB
    320.0 KB
    298.7 KB
    277.3 KB
    256.0 KB
    234.7 KB
    213.3 KB
    192.0 KB
    170.7 KB
    149.3 KB
    1 workers, elapsed time: 5.74s



```python
main(2)
```

    362.7 KB
    384.0 KB
    320.0 KB
    341.3 KB
    298.7 KB
    277.3 KB
    234.7 KB
    256.0 KB
    192.0 KB
    213.3 KB
    170.7 KB
    149.3 KB
    2 workers, elapsed time: 5.90s



```python
main(4)
```

    341.3 KB
    320.0 KB
    362.7 KB
    384.0 KB
    234.7 KB
    277.3 KB
    256.0 KB
    298.7 KB
    170.7 KB
    149.3 KB
    192.0 KB
    213.3 KB
    4 workers, elapsed time: 6.13s


### MapReduce模型

这种模式可能更加被大家熟悉,同一个流程,将容器中的数据一条一脚放入子进程运算,最终也结果也会被放入容器中.最后可以将收集来的数据在主进程中进行处理


```python
import math
PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]
def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True
```


```python
[is_prime(i) for i in PRIMES]
```




    [True, True, True, True, True, False]




```python
def ProcessPool_prime(PRIMES= PRIMES ,workers=4):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        total = []
        for prime in executor.map(is_prime, PRIMES):
            #print('%d is prime: %s' % (number, prime))
            total.append(prime)
    return total
```


```python
ProcessPool_prime()
```




    [True, True, True, True, True, False]



## 使用线程池进行相对底层的多进程操作

线程池的方式很适合批量创建子线程.线程池模块藏在多进程模块`multiprocessing.pool`下,`ThreadPool`

对ThreadPool对象调用`join()`方法会等待所有子进程执行完毕,调用`join()`之前必须先调用`close()`，调用`close()`之后就不能继续添加新的Process了.


请注意输出的结果,task 0,1,2,3是立刻执行的,而task 4要等待前面某个task完成后才执行,这是因为Pool的默认大小在我的电脑上是4，因此，最多同时执行4个进程.这是Pool有意设计的限制,并不是操作系统的限制.如果改成`p = Pool(5)`就可以同时跑5个进程.


由于Pool的默认大小是CPU的核数,如果你不幸拥有8核CPU,你要提交至少9个子进程才能看到上面的等待效果.


除了使用apply_async方法外,还有apply,map和map_async可以用于线程池的计算,编程模型也是如concurrent.futures一样分为两类

+ 并行任务模型

    + `apply` 单一任务布置
    + `apply_async` 非阻塞单一任务布置
    
+ MapReduce模型

    + `map` 同系统的map方法
    + `map_async` 非阻塞的map

#### apply_async


```python
from multiprocessing.pool import ThreadPool as Pool
import os, time, random

def long_time_task(name):
    print('运行任务 %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('任务 %s 执行了 %0.2f 秒.' % (name, (end - start)))

```


```python
print('父线程 %s.' % os.getpid())
p = Pool(4)
for i in range(5):
    p.apply_async(long_time_task, args=(i,))#创建非阻塞子线程用这个
print('等待所有子线程完成...')
p.close()
p.join()
print('所有子线程完成了.')
```

    父线程 36193.
    等待所有子线程完成...
    运行任务 0 (36193)...运行任务 1 (36193)...运行任务 2 (36193)...运行任务 3 (36193)...
    
    
    
    任务 0 执行了 1.00 秒.
    运行任务 4 (36193)...
    任务 3 执行了 1.13 秒.
    任务 2 执行了 2.02 秒.
    任务 1 执行了 2.81 秒.
    任务 4 执行了 1.93 秒.
    所有子线程完成了.


#### map_async


```python
from multiprocessing.pool import ThreadPool as Pool
from time import sleep

def f(x):
    return x*x

# start 4 worker processes
pool = Pool(processes=4)
print("map: ",pool.map(f, range(10)))
print("imap:")
for i in pool.imap_unordered(f, range(10)):
    print(i)

# evaluate "f(10)" asynchronously
res = pool.apply_async(f, [10])
print("apply:",res.get(timeout=1))             # prints "100"

# make worker sleep for 10 secs
res = pool.apply_async(sleep, [10])
print(res.get(timeout=1))             # raises multiprocessing.TimeoutError

```

    map:  [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    imap:
    0
    1
    4
    9
    16
    25
    36
    49
    64
    81
    apply: 100



    ---------------------------------------------------------------------------

    TimeoutError                              Traceback (most recent call last)

    <ipython-input-15-2fd51c1360c1> in <module>()
         18 # make worker sleep for 10 secs
         19 res = pool.apply_async(sleep, [10])
    ---> 20 print(res.get(timeout=1))             # raises multiprocessing.TimeoutError
    

    ~/anaconda3/lib/python3.6/multiprocessing/pool.py in get(self, timeout)
        638         self.wait(timeout)
        639         if not self.ready():
    --> 640             raise TimeoutError
        641         if self._success:
        642             return self._value


    TimeoutError: 


获取进程池中的运算结果


```python
from multiprocessing.pool import ThreadPool as Pool
import time

def func(msg):
    print("msg:", msg)
    time.sleep(1)
    print("end")
    return "done " + msg


pool = Pool(processes=4)
result = []
for i in range(3):
    msg = "hello %d" %(i)
    result.append(pool.apply_async(func, (msg, )))
pool.close()
pool.join()
for res in result:
    print(":::", res.get())
print("Sub-process(es) done.")
```

    msg: hello 0
    msg: hello 1
    msg: hello 2
    end
    end
    end
    ::: done hello 0
    ::: done hello 1
    ::: done hello 2
    Sub-process(es) done.


## 更底层的多线程编程

`threading`模块提供了一个高层的API来提供线程的并发性.这些线程并发运行并共享内存.多线程看着多么美好的,但因为数据安全的问题被加了锁.所以永远是单核运行,不细说了看个简单的用法吧

下面来看threading模块的具体用法:


```python
import threading
import time

def worker(i):
    print(i)
    time.sleep(1)
    print("AWAKE")

for i in range(5):
    t = threading.Thread(target=worker,args=(i,))
    t.start()
print("closed")
```

    01
    
    2
    3
    4closed
    
    AWAKEAWAKE
    
    AWAKEAWAKEAWAKE
    
    


对比下不用多线程:


```python
def worker(i):
    print(i)
    import time
    time.sleep(1)
    print("AWAKE")

for i in range(5):
    worker(i)

```

    0
    AWAKE
    1
    AWAKE
    2
    AWAKE
    3
    AWAKE
    4
    AWAKE


### 一个相对复杂的例子


```python
from threading import Thread
import os
#子线程要执行的代码
def run_proc(name):
    for i in range(3):
        print(u'子线程 %s (%s)...' % (name, os.getpid()))
    print(u'子线程结束.')

print(u'父线程 {}.'.format(os.getpid()))
p = Thread(target=run_proc, args=('test',))
print(u'子线程要开始啦.')
p.start()
for i in range(3):
    print(u'父线程{pid}进行中...'.format(pid = os.getpid()))
p.join()
print(u"父线程结束啦")
```

    父线程 36193.
    子线程要开始啦.
    子线程 test (36193)...
    子线程 test (36193)...父线程36193进行中...
    父线程36193进行中...
    父线程36193进行中...
    
    子线程 test (36193)...
    子线程结束.
    父线程结束啦


### 使用Thread作为父类自定义子线程

Thread的子类需要重写run方法


```python
from threading import Thread

from queue import Queue

class Processor(Thread):

    def __init__(self, queue, idx):
        super(Processor, self).__init__()
        self.queue = queue
        self.idx = idx

    def return_name(self):
        ## NOTE: self.name is an attribute of multiprocessing.Process
        return "Thread idx=%s is called '%s'" % (self.idx, self.name)

    def run(self):
        self.queue.put(self.return_name())
        
processes = list()
q = Queue()
for i in range(0,5):
    p=Processor(queue=q, idx=i)
    processes.append(p)
    p.start()
for proc in processes:
    proc.join()
    ## NOTE: You cannot depend on the results to queue / dequeue in the
    ## same order
    print("RESULT: {}".format(q.get()))
```

    RESULT: Thread idx=0 is called 'Thread-31'
    RESULT: Thread idx=1 is called 'Thread-32'
    RESULT: Thread idx=2 is called 'Thread-33'
    RESULT: Thread idx=3 is called 'Thread-34'
    RESULT: Thread idx=4 is called 'Thread-35'


创建子线程时,只需要传入一个执行函数和函数的参数,创建一个Thread实例,用`start()`方法启动,这样创建进程比`fork()`简单.

`join()`方法可以等待子线程结束后再继续往下运行,通常用于线程间的同步.

可以看到我们的父线程进行完了子线程才进行.其实当执行start方法的时候我们就已经把线程创建好并给他任务了.虽然线程启动了,但我们并不能知道它啥时候运算完成.这时候用join方法来确认是否执行完了(通过阻塞主线程),也就是起个等待结果的作用.

## 使用队列管理线程

线程安全是多线程编程中最不容易的事儿,线程间同步,互斥数据共享一直是要考虑的问题,而最常见的就是用队列实现管理线程了.

### 生产者消费者模型
队列最常见的用处就是在生产者消费者模式中作为数据缓冲区.以下就是一个生产者消费者模式的例子


```python
import queue as Queue
import threading
import random
```


```python
class Producer(threading.Thread):
    """生产者"""
    def __init__(self,q,con,name):
        super(Producer,self).__init__()
        self.q = q
        self.name = name
        self.con = con
        print("生产者{self.name}产生了".format(self=self))

    def run(self):
        count = 3 #只生产满3轮,要不然就会无限循环出不去了
        while count>0:
            #global writelock
            self.con.acquire()
            if self.q.full():
                print("队列满了,生产者等待")
                count-=1
                self.con.wait()

            else:
                value = random.randint(0,10)
                print("{self.name}把值{self.name}:{value}放入了队列".format(self=self,value=value))
                self.q.put("{self.name}:{value}".format(self=self,value=value))
            self.con.notify()
        self.con.release()
```


```python
class Consumer(threading.Thread):
    """消费者"""
    def __init__(self,q,con,name):
        super(Consumer,self).__init__()
        self.q = q
        self.name = name
        self.con = con
        print("消费者{self.name}产生了".format(self=self))

    def run(self):
        while True:
            #global writelock
            self.con.acquire()
            if self.q.empty():

                print("队列空了,消费者等待")
                self.con.wait()
            else:
                value = self.q.get()

                print("{self.name}从队列中获取了{self.name}:{value}".format(self=self,
                                                                         value=value))
                self.con.notify()
            self.con.release()
```


```python
q = Queue.Queue(10)
con = threading.Condition()
p1 = Producer(q,con,"P1")
p1.start()
p2 = Producer(q,con,"P2")
p2.start()
c1 = Consumer(q,con,"C1")
c1.start()
```

    生产者P1产生了
    P1把值P1:10放入了队列生产者P2产生了
    
    P1把值P1:10放入了队列
    P1把值P1:2放入了队列
    P1把值P1:10放入了队列
    P1把值P1:1放入了队列
    消费者C1产生了
    P1把值P1:6放入了队列
    P1把值P1:9放入了队列
    P1把值P1:3放入了队列
    P1把值P1:4放入了队列
    P1把值P1:4放入了队列
    队列满了,生产者等待
    队列满了,生产者等待
    C1从队列中获取了C1:P1:10
    C1从队列中获取了C1:P1:10
    C1从队列中获取了C1:P1:2
    C1从队列中获取了C1:P1:10
    C1从队列中获取了C1:P1:1
    C1从队列中获取了C1:P1:6
    C1从队列中获取了C1:P1:9
    C1从队列中获取了C1:P1:3
    C1从队列中获取了C1:P1:4
    C1从队列中获取了C1:P1:4
    队列空了,消费者等待
    P1把值P1:7放入了队列
    P1把值P1:8放入了队列
    P1把值P1:9放入了队列
    P1把值P1:10放入了队列
    P1把值P1:1放入了队列
    P1把值P1:7放入了队列
    P1把值P1:9放入了队列
    P1把值P1:10放入了队列
    P1把值P1:4放入了队列
    P1把值P1:1放入了队列
    队列满了,生产者等待
    队列满了,生产者等待
    C1从队列中获取了C1:P1:7
    C1从队列中获取了C1:P1:8
    C1从队列中获取了C1:P1:9
    C1从队列中获取了C1:P1:10
    C1从队列中获取了C1:P1:1
    P2把值P2:10放入了队列
    P2把值P2:1放入了队列
    P2把值P2:10放入了队列
    P2把值P2:1放入了队列
    P2把值P2:4放入了队列
    队列满了,生产者等待
    队列满了,生产者等待
    C1从队列中获取了C1:P1:7
    C1从队列中获取了C1:P1:9
    C1从队列中获取了C1:P1:10


## queue模块说明

队列类型 

+ `queue.Queue(maxsize)`先进先出队列,maxsize是队列长度,其值为非正数时是无限循环队列

+ `queue.LifoQueue(maxsize)` 后进先出队列,也就是栈
+ `queue.PriorityQueue(maxsize)` 优先级队列


支持方法

+ `qsize()` 返回近似队列大小,,用近似二字因为当该值大于0时不能保证并发执行的时候get(),put()方法不被阻塞
+ `empty()` 判断是否为空,空返回True否则返回False
+ `full()` 当设定了队列大小的时候,如果队列满了则返回True,否则False
+ `put(item[,block[,timeout]])` 向队列添加元素
    + 当block设置为False时队列满则抛出异常
    + 当block为True,timeout为None时则会等待直到有空位
    + 当block为True,timeout不为None时则根据设定的时间判断是否等待,超时了就抛出错误
+ `put_nowait(item)` 相当于put(item,False)
+ `get([,block[,timeout])` 从队列中取出元素,
    + 当block设置为False时队列空则抛出异常
    + 当block为True,timeout为None时则会等待直到有+元素
    + 当block为True,timeout不为None时则根据设定的时间判断是否等待,超时了就抛出错误
+ `get_nowait()` 等价于get(False)
+ `task_done()` 发送信号表明入列任务已经完成,常在消费者线程里使用
+ `join()` 阻塞直到队列中所有元素处理完

Queue是线程安全的,而且支持in操作,因此用它的时候不用考虑锁的问题

## 使用Unix信号

标准库`signal`提供了操作Unix信号的方法.需要注意signal模块主要是针对Unix平台(linux,osx).Windows上的Python不能发挥signal模块的功能.

常见的信号可以查看本章的结语部分.

Python信号处理程序总是在主线程中执行.这意味着信号不能用作线程间通信的手段.同时也只允许主线程设置新的信号处理程序.

### 常用信号处理函数

+ 设置发送SIGALRM信号的定时器

`signal.alarm(time)`可以设置一个发送`SIGALRM`信号的定时器,在time秒后就会发送这个信号量到进程,在不做处理的情况下进程会退出


+ 使用`signal.pasue`阻塞函数

`signal.pasue`会让主线程暂停以等待信号,接收到信号后使进程停止

+ `signal.signal(sig,handler)`用于注册收到信号后的处理函数

注意handler函数有两个参数--信号number和帧对象


下面这个例子我们演示了监听信号的过程,无论是等待10s还是使用`ctrl+C`都可以中断阻塞使程序结束.


```python
%%writefile src/signal_pasue.py
import signal
signal.signal(signal.SIGALRM,lambda sig,frame:print("闹钟!"))
signal.signal(signal.SIGINT,lambda sig,frame:print("ctrl+C!"))
signal.alarm(10)
print("开始等待信号")
signal.pause()
print("等待结束")

```

    Overwriting src/signal_pasue.py


### 多线程中使用信号


+ `signal.sigwait(sigset)`用于在子线程中等待`sigset`中定义的多个信号之一,一旦受到信号就取消阻塞向下走
+ `signal.pthread_kill(thread_id, signal.SIGCONT)`用于在主线程中发送消息到子线程.thread_id可以通过运行中的子线程的`ident`属性获得.

下面的例子演示了主线程向子线程发送信号的过程


```python
%%writefile src/signal_multithread.py
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

```

    Overwriting src/signal_multithread.py


## 线程变协程

在Python3.4之前python没有原生的协程那个时候有一个神级的协程库[gevent](http://www.gevent.org/contents.html)它可以通过[monkey patch](http://blog.hszofficial.site/TutorialForPython/%E8%AF%AD%E6%B3%95%E7%AF%87/%E5%85%83%E7%BC%96%E7%A8%8B/%E7%8C%B4%E5%AD%90%E8%A1%A5%E4%B8%81%E5%92%8C%E7%83%AD%E6%9B%B4%E6%96%B0.html)将标准库替换从而实现线程变协程,替换的库在[这个文档中](http://www.gevent.org/api/gevent.monkey.html#gevent.monkey.patch_all)有汇总.gevent至今依然被广泛使用,也是最推荐的协程使用方式之一.


```python
%%writefile src/gvt_test.py
from gevent import monkey; monkey.patch_all()
import threading
import queue
import socket
print(socket.socket)

class Processor(threading.Thread):

    def __init__(self, queue, idx):
        super(Processor, self).__init__()
        self.queue = queue
        self.idx = idx

    def return_name(self):
        ## NOTE: self.name is an attribute of multiprocessing.Process
        return "Thread idx=%s is called '%s'" % (self.idx, self.name)

    def run(self):
        self.queue.put(self.return_name())
        
processes = list()
q = queue.Queue()
for i in range(0,5):
    p=Processor(queue=q, idx=i)
    processes.append(p)
    p.start()
for proc in processes:
    proc.join()
    ## NOTE: You cannot depend on the results to queue / dequeue in the
    ## same order
    print("RESULT: {}".format(q.get()))
```

    Overwriting src/gvt_test.py



```python
!python src/gvt_test.py
```

    <class 'gevent._socket3.socket'>
    RESULT: Thread idx=0 is called 'Thread-1'
    RESULT: Thread idx=1 is called 'Thread-2'
    RESULT: Thread idx=2 is called 'Thread-3'
    RESULT: Thread idx=3 is called 'Thread-4'
    RESULT: Thread idx=4 is called 'Thread-5'

