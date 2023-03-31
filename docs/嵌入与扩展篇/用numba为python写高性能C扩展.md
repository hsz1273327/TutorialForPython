
# `*`用numba为python写高性能C扩展

[numba](http://numba.pydata.org/numba-doc/dev/index.html)是利用llvm加速python的技术,虽然现在还在开发中,但已经基本可用了

numba有代码预热,如果迭代太少反而会减低效率


```python
from numba import jit,int64,int32,float32,float64
```

## 基本用法:装饰符`@jit`


### 使用装饰符`@jit`可以延迟编译并进行优化


```python
def f_org(x, y):
    # A somewhat trivial example
    return x + y
```


```python
from numba import jit

@jit
def f(x, y):
    # A somewhat trivial example
    return x + y
```


```python
f(1,2)
```




    3




```python
f(1j, 2)
```




    (2+1j)



### 使用`@jit`标注类型快速编译


```python
@jit(int32(int32, int32))
def fint(x, y):
    # A somewhat trivial example
    return x + y
```


```python
fint(1,2)
```




    3




```python
fint(1j,2)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-8-59f8fbbf0505> in <module>()
    ----> 1 fint(1j,2)
    

    ~/anaconda3/lib/python3.6/site-packages/numba/dispatcher.py in _explain_matching_error(self, *args, **kws)
        397         msg = ("No matching definition for argument type(s) %s"
        398                % ', '.join(map(str, args)))
    --> 399         raise TypeError(msg)
        400 
        401     def _search_new_conversions(self, *args, **kws):


    TypeError: No matching definition for argument type(s) complex128, int64


numba必须为用到的所有函数加上`@jit`,否则会拖慢运算


```python
import math
@jit
def square(x):
    return x ** 2

@jit
def hypot(x, y):
    return math.sqrt(square(x) + square(y))
```


```python
hypot(1,2)
```




    2.23606797749979



我们来看看加速的效果怎么样


```python
import time
from numpy import random
from numba import double
from numba.decorators import jit as jit

def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result

jitsum2d = jit(sum2d)
csum2d = jitsum2d.compile(double(double[:,::1]))

arr = random.randn(100, 100)

start = time.time()
res = sum2d(arr)
duration = time.time() - start
print("Result from python is %s in %s (msec)" % (res, duration*1000))

csum2d(arr)       # warm up

start = time.time()
res = csum2d(arr)
duration2 = time.time() - start
print("Result from compiled is %s in %s (msec)" % (res, duration2*1000))

print("Speed up is %s" % (duration / duration2))
```

    Result from python is -68.045336031 in 2.89607048035 (msec)
    Result from compiled is -68.045336031 in 0.118970870972 (msec)
    Speed up is 24.3426853707


## 使用`@generated_jit()`编译时控制特殊化选项

虽然jit()装饰器在许多情况下是有用的，有时你想编写一个具有不同实现取决于其输入类型的函数。 generated_jit（）装饰器允许用户在编译时控制特殊化的选择，同时充满保留JIT函数的运行时执行速度。

假设你想编写一个函数，该函数根据某些约定返回一个给定值是否是一个"丢失"值。为了举例，让我们采用以下定义：
+ 对于浮点参数，缺少的值是NaN
+ Numpy datetime64和timedelta64参数，缺少的值是NaT
+ 其他类型没有缺少值的概念。

编译时逻辑很容易使用generated_jit()装饰器实现：


```python
import numpy as np

from numba import generated_jit, types

@generated_jit(nopython=True)
def is_missing(x):
    """
    Return True if the value is missing, False otherwise.
    """
    if isinstance(x, types.Float):
        return lambda x: np.isnan(x)
    elif isinstance(x, (types.NPDatetime, types.NPTimedelta)):
        # The corresponding Not-a-Time value
        missing = x('NaT')
        return lambda x: x == missing
    else:
        return lambda x: False
```

这里有几点要注意：
+ 装饰函数使用参数的Numba类型调用，而不是它们的值。
+ 装饰函数实际上不计算结果，它返回一个可调用的实现给定类型的函数的实际定义。
+ 可以在编译时预先计算一些数据（上面缺少的变量），以便在编译的实现中重用它们。
+ 函数定义使用与修饰函数中的参数相同的名称，这是必需的，以确保通过名称传递参数按预期工作。

## 编译可选项

除了基本用法,`@jit()`和`@generated_jit()`还可以带上一些参数

+ nopython

这个关键字表示编译时不使用python的对象,这是一种不太安全的编译方式,容易报错



```python
@jit(nopython=True)
def f_nopython(x, y):
    return x + y
```


```python
f_nopython(1,2)
```




    3



+ nogil

我们知道python受gil限制,使用这个参数可以突破限制,但用了这个就相当于也用了`nopython=True`,但要注意解决线程冲突等问题.


```python
@jit(nogil=True)
def f(x, y):
    return x + y
```


```python
import threading
from timeit import repeat

import numpy as np
from numba import jit

nthreads = 4
size = 1e6

def func_np(a, b):
    """
    Control function using Numpy.
    """
    return np.exp(2.1 * a + 3.2 * b)

@jit('void(double[:], double[:], double[:])', nopython=True, nogil=True)
def inner_func_nb(result, a, b):
    """
    Function under test.
    """
    for i in range(len(result)):
        result[i] = math.exp(2.1 * a[i] + 3.2 * b[i])

def timefunc(correct, s, func, *args, **kwargs):
    """
    Benchmark *func* and print out its runtime.
    """
    print(s.ljust(20))
    # Make sure the function is compiled before we start the benchmark
    res = func(*args, **kwargs)
    if correct is not None:
        assert np.allclose(res, correct), (res, correct)
    # time it
    print('{:>5.0f} ms'.format(min(repeat(lambda: func(*args, **kwargs),
                                          number=5, repeat=2)) * 1000))
    return res

def make_singlethread(inner_func):
    """
    Run the given function inside a single thread.
    """
    def func(*args):
        length = len(args[0])
        result = np.empty(length, dtype=np.float64)
        inner_func(result, *args)
        return result
    return func

def make_multithread(inner_func, numthreads):
    """
    Run the given function inside *numthreads* threads, splitting its
    arguments into equal-sized chunks.
    """
    def func_mt(*args):
        length = len(args[0])
        result = np.empty(length, dtype=np.float64)
        args = (result,) + args
        chunklen = (length + numthreads - 1) // numthreads
        # Create argument tuples for each input chunk
        chunks = [[arg[i * chunklen:(i + 1) * chunklen] for arg in args]
                  for i in range(numthreads)]
        # Spawn one thread per chunk
        threads = [threading.Thread(target=inner_func, args=chunk)
                   for chunk in chunks]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return result
    return func_mt


func_nb = make_singlethread(inner_func_nb)
func_nb_mt = make_multithread(inner_func_nb, nthreads)

a = np.random.rand(size)
b = np.random.rand(size)

correct = timefunc(None, "numpy (1 thread)", func_np, a, b)
timefunc(correct, "numba (1 thread)", func_nb, a, b)
timefunc(correct, "numba (%d threads)" % nthreads, func_nb_mt, a, b)
```

    /Users/huangsizhe/LIB/CONDA/anaconda/envs/py2/lib/python2.7/site-packages/ipykernel/__main__.py:76: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future
    /Users/huangsizhe/LIB/CONDA/anaconda/envs/py2/lib/python2.7/site-packages/ipykernel/__main__.py:77: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future


    numpy (1 thread)    
      118 ms
    numba (1 thread)    
       83 ms
    numba (4 threads)   
       46 ms





    array([ 90.34046635,   1.79903916,  33.98849279, ...,   9.11325173,
            21.48394079,  11.4777402 ])



+ cache

我们也可以使用缓存来提高运行效率


```python
@jit(cache=True)
def f_cache(x, y):
    return x + y
```


```python
f_cache(1,2)
```




    3



## 使用`@jitclass`编译python的类

这个装饰器比较新,目前容易出错.但用法应该不会有大变化,class可以静态编译的话还是相当可以


```python
import numpy as np
from numba import jitclass          # import the decorator
from numba import int32, float32    # import the types

spec = [
    ('value', int32),               # a simple scalar field
    ('array', float32[:]),          # an array field
]

@jitclass(spec)
class Bag(object):
    def __init__(self, value):
        self.value = value
        self.array = np.zeros(value, dtype=np.float32)

    @property
    def size(self):
        return self.array.size

    def increment(self, val):
        for i in range(self.size):
            self.array[i] = val
        return self.array
```


```python
mybag = Bag(21)
print('isinstance(mybag, Bag)', isinstance(mybag, Bag))
print('mybag.value', mybag.value)
print('mybag.array', mybag.array)
print('mybag.size', mybag.size)
print('mybag.increment(3)', mybag.increment(3))
print('mybag.increment(6)', mybag.increment(6))
```

    ('isinstance(mybag, Bag)', True)
    ('mybag.value', 21)
    ('mybag.array', array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.], dtype=float32))
    ('mybag.size', 21)
    ('mybag.increment(3)', array([ 3.,  3.,  3.,  3.,  3.,  3.,  3.,  3.,  3.,  3.,  3.,  3.,  3.,
            3.,  3.,  3.,  3.,  3.,  3.,  3.,  3.], dtype=float32))
    ('mybag.increment(6)', array([ 6.,  6.,  6.,  6.,  6.,  6.,  6.,  6.,  6.,  6.,  6.,  6.,  6.,
            6.,  6.,  6.,  6.,  6.,  6.,  6.,  6.], dtype=float32))


### 限制
+ 一个jitclass类对象在numba编译函数中被当作一个函数（构造函数）。
+ isinstance()只在解释器中工作。但在解释器中操作jitclass实例尚未优化。
+ jitclasses目前仅在CPU上可用。

## 使用`@vectorize`和`@guvectorize`构建numpy的universal function

vectorize(向量化计算)是指是一种特殊的并行计算的方式，相比于一般程序在同一时间只执行一个操作的方式，它可以在同一时间执行多次操作，通常是对不同的数据执行同样的一个或一批指令，或者说把指令应用于一个数组/向量。
python的numpy包以向量化作为其计算的基本特点.而`@vectorize`就是将函数作为向量化工具的装饰器

目前,`vectorize`装饰器支持编译后被下面的目标使用:

Target	|Description
---|---
cpu|Single-threaded CPU
parallel|Multi-core CPU
cuda|CUDA GPU

### vectorize()

我们可以这样定义一个操作


```python
from numba import vectorize, float64

@vectorize([float64(float64, float64)])
def f_u(x, y):
    return x + y
```

但这样就限制了通共性,我们可以这样写提高他的通用性


```python
@vectorize([int32(int32, int32),
            int64(int64, int64),
            float32(float32, float32),
            float64(float64, float64)])
def f_u(x, y):
    return x + y
```


```python
a = np.arange(6)
f_u(a, a)
```




    array([ 0,  2,  4,  6,  8, 10])




```python
a = np.linspace(0, 1, 6)
f_u(a, a)
```




    array([ 0. ,  0.4,  0.8,  1.2,  1.6,  2. ])




```python
a = np.linspace(0, 1+1j, 6)
```


```python
f_u(a, a)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-28-d8a6bc9e068a> in <module>()
    ----> 1 f_u(a, a)
    

    TypeError: ufunc 'f_u' not supported for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''



```python
a = np.arange(12).reshape(3, 4)
```


```python
a
```




    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]])




```python
f_u.reduce(a, axis=0)
```




    array([12, 15, 18, 21])




```python
f_u.reduce(a, axis=1)
```




    array([ 6, 22, 38])




```python
f_u.accumulate(a)
```




    array([[ 0,  1,  2,  3],
           [ 4,  6,  8, 10],
           [12, 15, 18, 21]])




```python
f_u.accumulate(a, axis=1)
```




    array([[ 0,  1,  3,  6],
           [ 4,  9, 15, 22],
           [ 8, 17, 27, 38]])



### guvectorize()
`vectorize()`允许你编写一次在一个元素上工作的ufuncs
而`guvectorize()`装饰器将这个概念进一步提升一步，允许你编写ufuncs来处理输入为任意数量的元素的数组，并返回不同尺寸的阵列。典型的例子是运行中值或卷积滤波器。与`vectorize()`函数相反，`guvectorize()`函数不返回它们的结果值：它们将它作为数组参数，它必须由函数填充。这是因为数组实际上是由NumPy的dispa分配的


```python
from numba import vectorize,guvectorize
@guvectorize([(int64[:], int64[:], int64[:])], '(n),()->(n)')
def g(x, y, res):
    for i in range(x.shape[0]):
        res[i] = x[i] + y[0]
```


```python
a = np.arange(5)

print(g(a, 2))

```

    [2 3 4 5 6]



```python
b = np.arange(6).reshape(2, 3)
print(g(b, 10))
print(g(b, np.array([10, 20])))
```

    [[10 11 12]
     [13 14 15]]
    [[10 11 12]
     [23 24 25]]

