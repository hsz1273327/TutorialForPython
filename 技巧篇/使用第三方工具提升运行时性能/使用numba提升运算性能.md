# 使用numba提升运算性能

[numba](http://numba.pydata.org/)是专门利用llvm的jit技术加速python的技术,底层还是C.它并不具备扩展python功能的作用,但可以非常简单的加速python代码的执行.需要注意numba有代码预热,如果迭代太少反而会减低效率.


```python
from numba import jit,int64,int32,float32,float64
```

## 基本用法

numba的基本用法就是利用python的装饰器装饰函数或类,在执行时就会根据不同的装饰器起到不同的作用.

在提升python运算性能方面大致可以分为3种装饰器

+ `@jit`(包括`@njit`,`@generated_jit()`等),装饰一个要提速的函数
+ `@jitclass`,装饰一个要提速的类

同时numba支持`parallel`和`fastmath`选项可以进一步用真多线程并行计算以及针对数学运算的专用库进行提速

### 装饰器`@jit`

装饰符`@jit`可以针对一个函数进行延迟编译并进行优化.它可以是一个不带参数的装饰器也可以是带参数的装饰器,其支持的参数按顺序包括:

+ `signature=None`,指定函数签名,当指定了函数签名后numba可以根据指定的签名更好的静态化,从而提高运行效率
+ `nopython=False`,强制使用`nopython`模式执行,当使用`nopython`模式时numba会将被装饰的函数进行编译,这样它就可以完全在没有Python解释器的情况下运行,也就可以有更好的运行性能;但如果设置`nopython=False`时numba也会优先使用`nopython`模式,当无法使用时才会回退到`object`模式.在`object`模式下numba将识别可以编译的循环,并将其编译成在机器代码中运行的函数然后在解释器中运行其余代码.
+ `nogil=False`, 使函数不受gil限制,这只会在`nopython`模式下执行时生效
+ `cache=False`, 指定是否使用编译缓存,当启用时函数的编译结果会留下缓存.当被调用时有缓存时则会加载缓存而不是重新编译.缓存默认保存在包含源文件的目录的`__pycache__`子目录中,但如果没有对这个目录的写权限则会回退保存到平台的当前用户的缓存目录中(例如Unix平台上的`$HOME/.cache/numbera`).并不是所有的函数都可以缓存,因为有些函数不能始终保存到磁盘上.当函数无法缓存时numba会发出警告.
+ `forceobj=False`, 强制使用`object`模式运行.
+ `parallel=False`, 指定是否并行计算,这边的并行化主要针对numpy优化
+ `error_model='python'`, 指定除0错误的行为模式,可选的有`numpy`和`python`
+ `fastmath=False`,指定是否使用`fastmath`针对数值计算做额外优化
+ `locals={}`, 指定函数的本地变量的类型,类似指定函数签名,也是起到静态化提高运行效率的作用
+ `boundscheck=False`,函数不做边界检查

装饰器`@jit`有几个扩展,他们是:

+ `@njit`,`@jit(nopython=True)`的缩写,numba官方推荐更多的使用`nopython`模式,因此我们通常也更常用它.它的其他参数和`@jit`一致
+ `@generated_jit`,允许动态生成编译结果的`@jit`,用在函数的输入类型不固定时

最简单的用法就是直接使用`@jit`装饰你需要加速的函数,比如一个函数:

```python
def f_org(x, y):
    # A somewhat trivial example
    return x + y
```


```python
from numba import njit

@njit
def f(x, y):
    # A somewhat trivial example
    return x + y
```


```python
f(1, 2)
```




    3




```python
f(1j, 2)
```




    (2+1j)



#### 体验加速

我们来看看加速的效果怎么样


```python
import time
from numpy import random
from numba import double
from numba import njit as jit

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

    Result from python is -120.81653580794645 in 1.600027084350586 (msec)
    Result from compiled is -120.81653580794645 in 0.046253204345703125 (msec)
    Speed up is 34.59278350515464


上面这个例子中,相同的函数,使用numba加速可以快近35倍.

#### 使用`@jit`标注类型快速编译

通过指定函数的签名类型以及本地变量类型可以帮助numba更好的编译,从而提高效率.

numba提供了如下变量名用于指定类型,基础类型包括:

类型名|简写|说明
---|---|---
`boolean`|`b1`| 布尔类型
`uint8`,`byte`|`u1`|8位长度的无标记字节
`uint16`|`u2`|16位长度无标记整型
`uint32`|`u4`|32位长度无标记整型
`uint64`|`u8`|64位长度无标记整型
`int8`,`char`|`i1`|8位长度的有标记字节
`int16`|`i2`|16位长度有标记整型
`int32`|`i4`|32位长度有标记整型
`int64`|`i8`|64位长度有标记整型
`intc`|---|C语言中int长度的整型
`uintc`|---|C语言中int长度的无标记整型
`intp`|---|指针长度整型
`uintp`|---|指针长度无标记整型
`ssize_t`|---|C语言中的`ssize_t`
`size_t`|---|C语言中的`size_t`
`float32`|`f4`|单精度浮点数
`float64`,`double`|`f8`|双精度浮点数
`complex64`|`c8`|单精度复数
`complex128`|`c16`|双精度复数

numba同样支持数组,其写法就是在基础类型后面加`[:]`,`[]`中的内容可以是如下形式,基本就是通用的连续内存表示形式:

+ `int32[:]`表示int32类型的1维数组
+ `int32[:,:]`表示int32类型的2维数组

可以用`::1`来表示内存连续性,规则也是和其他地方一致的

此外还有特殊类型`void`用于标注函数无返回,以及修饰函数`optional(基础类型)`用于标注变量可以为空


标注函数签名使用参数`signature`,其形式为`返回值类型(参数1类型,参数2类型,...)`可以是函数形式也可以是字符串形式

```python
from numba import njit,int32

@njit(int32(int32, int32))
def fint(x, y):
    # A somewhat trivial example
    return x + y
```

等价于

```python
from numba import njit

@njit(signature = "int32(int32, int32)")
def fint(x, y):
    # A somewhat trivial example
    return x + y
```

#### `@jit`装饰函数的调用

在`@jit`装饰器外部调用`@jit`装饰的函数和调用普通函数是一样的,上面已有演示.

但如果调用行为在`@jit`装饰器装饰的函数内部则需要注意,被调用的函数也必须被`@jit`所装饰,否则会拖慢运算.


```python
import math
@njit
def square(x):
    return x ** 2

@njit
def hypot(x, y):
    return math.sqrt(square(x) + square(y))
```


```python
hypot(1,2)
```




    2.23606797749979



#### 突破gil限制

我们知道python受gil限制,使用`nogil`这个参数可以突破限制,但要注意解决线程冲突,资源争抢等问题,因此一旦开启,其包装的函数就需要谨慎编写了.

下面这个例子我们进行一个矩阵计算,将两个同维的矩阵每一位分别乘以一个倍数后相加再平方.


```python
import math
import threading
from timeit import repeat

import numpy as np
from numba import njit

nthreads = 4
size = int(1e6)

def func_np(a, b):
    """numpy计算的函数."""
    return np.exp(2.1 * a + 3.2 * b)

@njit('void(double[:], double[:], double[:])',nogil=True)
def inner_func_nb(result, a, b):
    """待测试的函数."""
    for i in range(len(result)):
        result[i] = math.exp(2.1 * a[i] + 3.2 * b[i])

def timefunc(correct, s, func, *args, **kwargs):
    """计时程序,用于做Benchmark."""
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
    """单线程计算."""
    def func(*args):
        length = len(args[0])
        result = np.empty(length, dtype=np.float64)
        inner_func(result, *args)
        return result
    return func

def make_multithread(inner_func, numthreads):
    """多线程计算."""
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

    numpy (1 thread)    
       66 ms
    numba (1 thread)    
       42 ms
    numba (4 threads)   
       15 ms





    array([ 7.62183712, 42.92231867,  1.63570813, ...,  6.25215369,
           11.4994343 ,  3.65032141])



可以看到性能的提升相当明显

#### 使用`@generated_jit()`编译时控制特殊化选项

`@jit`通常已经够用了,但如果你想编写一个实现由输入参数类型决定的函数时`@jit`并不能有效的加速,这时候就可以使用`@generated_jit`了.`@generated_jit`装饰器允许用户在编译时控制特殊化的选择,同时充分保留jit函数的运行时执行速度.

其可以填入的参数多数和`@jit`相同,按顺序如下:

+ `nopython=False`
+ `nogil=False`
+ `cache=False`
+ `forceobj=False`
+ `locals={}`


下面这个例子中,我们根据参数的类型来用不同的方式判断输入参数是否是一个"缺失值".我们采用以下定义:

+ 对于浮点参数,缺失值是`NaN`
+ Numpy的`datetime64`和`timedelta64`类型参数,缺失值是`NaT`
+ 其他类型没有缺失值的概念。


```python
import numpy as np

from numba import generated_jit, types

@generated_jit(nopython=True)
def is_missing(x):
    """判断x是否为缺失值."""
    if isinstance(x, types.Float):
        return lambda x: np.isnan(x)
    elif isinstance(x, (types.NPDatetime, types.NPTimedelta)):
        # The corresponding Not-a-Time value
        missing = x('NaT')
        return lambda x: x == missing
    else:
        return lambda x: False
```

    /Users/mac/micromamba/envs/py3.10/lib/python3.10/site-packages/numba/core/decorators.py:262: NumbaDeprecationWarning: [1mnumba.generated_jit is deprecated. Please see the documentation at: https://numba.readthedocs.io/en/stable/reference/deprecation.html#deprecation-of-generated-jit for more information and advice on a suitable replacement.[0m
      warnings.warn(msg, NumbaDeprecationWarning)



```python
is_missing(12)
```




    False




```python
is_missing(np.NaN)
```




    True



这里有几点要注意:

+ 装饰函数实际上不计算结果,它**返回一个可调用的实现给定类型的函数**的实际定义.
+ 返回的函数的形参名称需要与`@generated_jit`装饰的函数的**形参名字相同**,以确保通过名称传递参数按预期工作.
+ 装饰函数使用参数的Numba类型调用而不是它们的值.
+ 可以在编译时预先计算一些数据(上面缺少的变量),以便在编译的实现中重用它们.


### 使用`@jitclass`编译python的类

Numba支持通过`@jitclass`装饰器装饰一个类,使其中的字段被转存到堆内可以跳过python解释器被`nopython`模式的函数访问,同时使其绑定的方法都被编译成`nopython`模式的函数.


`@jitclass`装饰的类属性需要声明类型,我们可以直接使用python的typehints语法声明也可以通过`@jitclass`的参数`spec`申明,当参数`spec`中有对对应字段的申明时numba使用参数`spec`中的声明,否则使用typehints语法声明自动推导的结果.typehints声明并不需要指定numba中的类型,和正常python类型标注一样就可以,numba会自己做推导.需要注意如果有字段是numpy的数组,这个用typehints目前无法准确声明,因此这种类型的字段必须在参数`spec`中声明.

`@jitclass`装饰的类必须至少有个自定义的`__init__`方法用于给定义的字段提供默认值


```python
import numpy as np
from numba.experimental import jitclass          # import the decorator
from numba import int32, float32    # import the types

spec = [   
    ('array', float32[:]),          # an array field
]

@jitclass(spec)
class Bag(object):
    value: int
    array: list[float]
    def __init__(self, value: int):
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

    isinstance(mybag, Bag) True
    mybag.value 21
    mybag.array [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
    mybag.size 21
    mybag.increment(3) [3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3. 3.]
    mybag.increment(6) [6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6. 6.]


`@jitclass`的使用有如下注意点:

+ `@jitclass`装饰的类对象被视为numba编译函数中的函数(构造函数)

+ `isinstance()`只在python解释器中起作用

+ 在解释器中操作`@jitclass`装饰的类的实例实例时尚未优化

+ 对`@jitclass`的支持仅在CPU上可用


## numba装饰器中函数的使用限制

被numba装饰器装饰的函数其中的代码并非支持全部python语法,下面是使用限制

### 完全支持的python语法

1. 条件语法: `if .. elif .. else`

2. 循环语法:`while`,`for .. in`,`break`,`continue`

3. 生成器语法: `yield`

4. 断言语法: `assert`

### 部分支持的语法

+ 异常语法: `try .. except ... else ... finally `, `raise`,限制是只能捕获异常基类`Exception`和它的子类,同时会屏蔽`KeyboardInterrupt`,`SystemExit`这两个由系统信号引起的异常.

+ 上下文管理器: `with`,仅支持`numba.objmode()`这一种上下文管理器

+ 函数动态参数: 支持`*args`,但对应的`args`类型为tuple,不支持`**kwargs`

+ 高级函数: 支持函数作为参数,但不支持函数作为返回值

+ 内部函数: 仅支持非递归的内部函数

+ 递归调用: 支持大多数递归调用模式,唯一的限制是递归被调用者必须有一个返回时不递归的控制流路径

+ 标准容器: 都支持,包括`str`类型也支持大多数内置方法,但`tuple`无法使用`tuple(x)`的形式构造;`list`,`set`和`dict`必须严格同构,且类型需要预先已经被编译.且只有符合这些要求的容器可以使用解析语法.

### 不支持的语法

+ 异步语法: `async with`,`async for`,`async def`,`await`

+ 类定义: `class`(我们应该在外部使用`@jitclass`定义用到的类)

+ 生成器委托语法: `yield from`

+ 其他较新的语法糖如模式匹配等

### 与python行为不一致的地方


### 支持的内置函数

仅支持如下内置函数(不算内置类型的构造函数)

内置函数|限制
---|---
`abs()`|---
`chr()`|---
`divmod()`|---
`enumerate()`|---
`filter()`|---
`getattr()`|属性必须为字符串且返回值不能为函数
`hasattr()`|---
`hash()`|---
`iter()`|仅支持单参数版本
`isinstance()`|---
`len()`|---
`min()`|---
`map()`|---
`max()`|---
`next()`|仅支持单参数版本
`ord()`|---
`print()`|仅支持单参数版本
`range()`|不能将其作为参数传递
`repr()`|---
`round()`|---
`sorted()`|不支持`key`参数
`sum()`|---
`type()`|仅支持部分类型,仅支持单参数版本
`zip()`|---

### 支持的标准库

支持的标准库如下:

标准库|限制
---|---
`array`|不支持类型代码`u`
`cmath`|支持[部分函数](https://numba.readthedocs.io/en/stable/reference/pysupported.html#cmath)
`collections`|不支持`collections.namedtuple()`
`ctypes`|支持[以特定类型作为参数和返回值的接口](https://numba.readthedocs.io/en/stable/reference/pysupported.html#ctypes)
`enum`|支持`enum.Enum`和`enum.IntEnum`的子类
`math`|支持[部分函数](https://numba.readthedocs.io/en/stable/reference/pysupported.html#math)
`operator`|支持[部分函数](https://numba.readthedocs.io/en/stable/reference/pysupported.html#operator)
`functools`|仅支持`functools.reduce()`且必须填入参数`initializer`
`random`|仅支持[部分函数](https://numba.readthedocs.io/en/stable/reference/pysupported.html#random),更多的时候推荐使用numpy的随机功能
`heapq`|支持[部分函数](https://numba.readthedocs.io/en/stable/reference/pysupported.html#heapq)


## 总结

可以看出numba是为高性能计算设计的python性能提升工具,主要针对计算密集型任务,数值计算为主.在满足它要求的情况下确实可以大幅提高python程序的执行效率.但使用限制还是比较多的,编码时要是有不少要注意的方面.
