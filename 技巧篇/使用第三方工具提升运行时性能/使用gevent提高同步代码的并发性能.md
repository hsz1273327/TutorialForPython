# 使用gevent提高同步代码的并发性能

如果你的整个程序(包括依赖)的网络,系统信号,多线程等部分都仅使用了标准库,那么你就可以使用[gevent的猴子补丁](https://www.gevent.org/intro.html#monkey-patching)借助greenlet将同步代码隐式的替换为异步操作从而实现提高并发性能的要求.

接口也及其简单--在程序的入口最顶部打上猴子补丁即可
```python
try:
    from gevent import monkey
except Exception:
    print("gevent not installed,not patched")
else:
    monkey.patch_all()
...
```

这个方式有如下注意猴子补丁需要打在最早执行的位置,这样之后导入的标准库中对应的对象就都会被替换为gevent中的异步操作.具体替换的标准库包括:

+ `socket`,可以将同名参数置为`False`来取消补丁,如果希望为除了其中`dns`相关的方法外打补丁,则可以将参数`dns`置为`False`.
+ `ssl`,可以将同名参数置为`False`来取消补丁,替换`ssl.SSLSocket`,仅在给socket打了补丁的情况下会生效.
+ `select`,可以将同名参数置为`False`来取消补丁,如果参数`aggressive`设为`False`则只替换`select.select()`和`select.poll()`,否则还会额外替换`select.epoll()`,
`select.kqueue()`,`select.kevent()`,`select.devpoll()`Ï
+ `signal`,可以将同名参数置为`False`来取消补丁,替换`signal.signal()`
+ `os`,可以将同名参数置为`False`来取消补丁,替换`os.fork()`和`os.waitpid()`.需要先有`signal`打好补丁
+ `subprocess`,可以将同名参数置为`False`来取消补丁替换掉`subprocess.call()`,`subprocess.check_call()`,`subprocess.check_output()`和`subprocess.Popen`
+ `thread`,可以将同名参数置为`False`来取消补丁,用eventlet替换线程,注意同时和`multiprocessing.Queue`或`concurrent.futures.ProcessPoolExecutor`一起使用会造成进程被挂起.
+ `queue`,可以将同名参数置为`False`来取消补丁,替换`queue.SimpleQueue`,仅在python3.7以上的版本会生效
+ `contextvars`,可以将同名参数置为`False`来取消补丁,替换`contextvars`模块中的接口
+ `time`,可以将同名参数置为`False`来取消补丁,`time.sleep`会被替换为异步

与之类似的包[eventlet](https://github.com/eventlet/eventlet)也可以用相似的方法通过猴子补丁达到相似的效果,不同点仅在于gevent的后端是`libev`或`libuv`.而eventlet的后端是异步库`libevent`

## 对psycopg2打补丁

`psycopg2`是连接`postgresql`的python客户端程序,但由于它是完全使用C写的,gevent的猴子补丁无法对其直接生效,要让它也支持异步gevent也支持对其打补丁,当然这需要一些额外的代码


```python
try:
    from gevent import monkey
except Exception:
    print("gevent not installed,not patched")
else:
    monkey.patch_all()
    try:
        from psycopg2 import extensions
    except ModuleNotFoundError as e:
        warnings.warn("not install psycopg2 skip patching")
    else:
        def patch_psycopg2() -> None:
            extensions.set_wait_callback(_psycopg2_gevent_callback)
        def _psycopg2_gevent_callback(conn: Any, timeout: Any = None) -> None:
            while True:
                state = conn.poll()
                if state == extensions.POLL_OK:
                    break
                elif state == extensions.POLL_READ:
                    wait_read(conn.fileno(), timeout=timeout)
                elif state == extensions.POLL_WRITE:
                    wait_write(conn.fileno(), timeout=timeout)
                else:
                    raise ValueError('poll() returned unexpected result')
    
        patch_psycopg2()
        
```

上面的代码可以借助库[psycogreen](https://github.com/psycopg/psycogreen/)来简化代码
                
```python
try:
    from gevent import monkey
except Exception:
    print("gevent not installed,not patched")
else:
    monkey.patch_all()
    try:
        from psycopg2 import extensions
    except ModuleNotFoundError as e:
        warnings.warn("not install psycopg2 skip patching")
    else:
        import psycogreen.gevent
        psycogreen.gevent.patch_psycopg()
```

## 总结

优点:

1. 几乎无侵入,没有学习成本
2. 非常容易分发
3. 对并发性能提升显著


缺点:

1. 适用场景狭窄
2. 仅加速io操作
3. 隐式替换难以debug



适用场景:

gevent打猴子补丁是在python异步语法出现前针对高并发的标准做法,即便到了现在其效果依然拔群,不少老python用户依然拒绝使用异步语法就是因为有gevent可见其江湖地位.但它的适用范围也仅限于io密集型任务.而且由于其原理是将线程改为协程,因此只要打了补丁就相当于废了线程,这样如果程序中有计算密集型的部分就必然会造成堵塞,python 3.12开始已经在逐步取消gil了,在未来的版本中python必将可以使用多线程利用多核,届时使用这种方式这无异于自己放弃对多核的支持.
