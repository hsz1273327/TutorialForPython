
# 在Ipython Notebook中的代码调试与优化

jupyter 是科学计算工具,那代码的调优就是它的一个重点了,python本身的运算能力其实很令人着急的,但通过分析计算瓶颈和用numpy,cython等工具优化代码,python也可以拥有非常高的运算效率(其实是C的功劳)

本文的先验知识有:

+ [代码调试](/工具链篇/调试工具.html)
+ [性能调优](/工具链篇/性能调优工具/html)
+ [使用Cython为python加速](/嵌入与扩展篇/使用Cython优化python程序的性能)
+ [使用numba为python加速](/嵌入与扩展篇/用numba为python写高性能C扩展.html)

## 调试代码

+ ### 异常抛出精简

python报异常从来都是一大段,很难看也很难看懂,可以使用`%xmode Plain`和`%xmode Verbose`来在精简模式和运来模式间切换


```python
def f1(a,b):
    return a/b
def f2(x):
    a = x
    b = x-1
    return f1(a,b)
```


```python
%xmode Plain
```

    Exception reporting mode: Plain



```python
f2(1)
```


    Traceback (most recent call last):


      File "<ipython-input-3-d9076a5554c7>", line 1, in <module>
        f2(1)


      File "<ipython-input-1-d7ac5604b6da>", line 6, in f2
        return f1(a,b)


      File "<ipython-input-1-d7ac5604b6da>", line 2, in f1
        return a/b


    ZeroDivisionError: division by zero




```python
%xmode Verbose
```

    Exception reporting mode: Verbose



```python
f2(1)
```


    ---------------------------------------------------------------------------

    ZeroDivisionError                         Traceback (most recent call last)

    <ipython-input-5-d9076a5554c7> in <module>()
    ----> 1 f2(1)
            global f2 = <function f2 at 0x106a34bf8>


    <ipython-input-1-d7ac5604b6da> in f2(x=1)
          4     a = x
          5     b = x-1
    ----> 6     return f1(a,b)
            global f1 = <function f1 at 0x106a34840>
            a = 1
            b = 0


    <ipython-input-1-d7ac5604b6da> in f1(a=1, b=0)
          1 def f1(a,b):
    ----> 2     return a/b
            a = 1
            b = 0
          3 def f2(x):
          4     a = x
          5     b = x-1


    ZeroDivisionError: division by zero


+ ### `%debug`用户调试错误

使用`%debug`会在报错时进去调试模式,在调试模式中我们可以
+ 输入变量名来获取变量的情况,
+ 输入up来进入上一层查看
+ 要退出输入quit即可

+ ### 运行时间检查
计算机再怎么算的慢也是比人快的多的,人的直觉并不能很好的感知到一个程序运行的快不快慢不慢,这种时候就要用时间检查工具.
ipython中常用的就是`%timeit <func>`命令了


```python
%timeit sum(map(lambda x:x**2,range(10000000)))
```

    6.57 s ± 214 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


或者查看具体时间在哪里损耗的`%time`


```python
%time sum(map(lambda x:x**2,range(10000000)))
```

    CPU times: user 6.15 s, sys: 61.9 ms, total: 6.21 s
    Wall time: 6.41 s





    333333283333335000000



+ ### `%%prun`/`%prun`命令调用`profile`模块，对单元中的代码进行宏观上的性能剖析

`%prun`将会产生一个有序表格来展示在该语句中所调用的每个内部函数调用的次数，每次调用的时间与该函数累计运行的时间。


```python
%%prun
def fib(n):
    if n<2:
        return n
    return fib(n-1)+fib(n-2)
fib(20)
```

     

+ ### 使用`line_profiler`,对代码做逐行性能分析

在ipython中使用line_profiler可以使用他们的ipython魔法命令`%lprun`,要使用这个魔法命令需要先加载

`%lprun`可以带上参数 `-f` 指定需要检查的方法


```python
%load_ext line_profiler
```


```python
%lprun -s -f fib fib(20)
```

+ ### 使用memory_profiler,对代码做内存分析

与line_profiler类似,memory_profiler也有对ipython的支持,使用方式也类似,他的魔法命令是`%menit`和`%mprun`

+ ### 粗粒度内存检查

关于内存的使用,在数据量小的时候看不出来但一旦数据量大了就会很棘手,ipython中查看内存使用的魔法命令是`%menit`


```python
%load_ext memory_profiler
```


```python
%memit sum(map(lambda x:x**2,range(10000000)))
```

    peak memory: 41.92 MiB, increment: 0.10 MiB


+ ### 细粒度内存检查

`%mprun`只能检查引用进来的模块的内存性能,因此需要先将代码写到文件重作为模块引入

`%mprun`可以带上参数 `-f` 指定需要检查的方法



```python
import myfib
```


```python
%mprun -f myfib.fib myfib.fib(20)
```

    


## `*`使用C语言扩展做代码优化

对于提高python运行速度,我们常用C语言来加速,对于用C语言构建核心运算模块,Cython是numpy,scipy的发展方向.一般用Cython我们都是拿他写模块,写好后要编译安装,而ipython notebook对Cython有相当好的支持

我们可以用`%load_ext Cython`来直接编译运行Cython写出来的程序


```python
%load_ext Cython
```

我们以斐波那契数列来举例,看看用在ipython中python的速度可以有多快

### 用Cython优化性能

+ 原版python


```python
def fib(n):
    if n<2:
        return n
    return fib(n-1)+fib(n-2)
```


```python
fib(20)
```




    6765




```python
%timeit fib(20)
```

    5.04 ms ± 94.6 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


+ 直接用cython加速


```cython
%%cython

def fib_cython(n):
    if n<2:
        return n
    return fib_cython(n-1)+fib_cython(n-2)
```


```python
fib_cython(20)
```




    6765




```python
%timeit fib_cython(20)
```

    1.66 ms ± 164 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


时间上和原版俩差了3倍的速度

+ 使用静态编译


```cython
%%cython
cpdef long fib_cython_type(long n):
    if n<2:
        return n
    return fib_cython_type(n-1)+fib_cython_type(n-2)
```


```python
fib_cython_type(20)
```




    6765




```python
%timeit fib_cython_type(20)
```

    56.7 µs ± 1.8 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)


速度直线上升,快了100倍不止!

+ 使用缓存计算(递归改迭代)


```python
from functools import lru_cache as cache
```


```python
@cache(maxsize=None)
def fib_cache(n):
    if n<2:
        return n
    return fib_cache(n-1)+fib_cache(n-2)
```


```python
%timeit fib_cache(20)
```

    181 ns ± 5.27 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)


或者简单的使用变量


```python
def fib_seq(n):
    if n < 2:
        return n
    a,b = 1,0
    for i in range(n-1):
        a,b = a+b,a
    return a
```


```python
fib_seq(20)
```




    6765




```python
%timeit fib_seq(20)
```

    2.4 µs ± 116 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)


原版的Python对迭代的优化还是相当可以的利用两个变量存储过程量,可以大大减少运算量

+ **使用缓存并且使用Cython加速**


```cython
%%cython
from functools import lru_cache as cache
@cache(maxsize=None)
def fib_cache_cython(n):
    if n<2:
        return n
    return fib_cache_cython(n-1)+fib_cache_cython(n-2)
```


```python
%timeit fib_cache_cython(20)
```

    218 ns ± 13 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)



```cython
%%cython
def fib_seq_cython(n):
    if n < 2:
        return n
    a,b = 1,0
    for i in range(n-1):
        a,b = a+b,a
    return a 
```


```python
fib_seq_cython(20)
```




    6765




```python
%timeit fib_seq_cython(20)
```

    1.07 µs ± 25.8 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)


惊了...只有1微秒左右!

+ 再静态化


```cython
%%cython
cpdef long fib_seq_cython_type(long n):
    if n < 2:
        return n
    cdef long a,b
    a,b = 1,0
    for i in range(n-1):
        a,b = a+b,a
    return a
```


```python
fib_seq_cython_type(20)
```




    6765




```python
%timeit fib_seq_cython_type(20)
```

    113 ns ± 1.31 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)


又快了4倍

### 使用numba加速


```python
from numba import jit
```


```python
@jit
def fib_seq_numba(n):
    if n < 2:
        return n
    a,b = 1,0
    for i in range(n-1):
        a,b = a+b,a
    return a 
```


```python
fib_seq_numba(20)
```




    6765




```python
%timeit fib_seq_numba(20)
```

    293 ns ± 5.73 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)


略不如Cython的最终版本
