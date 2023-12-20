# numba与numpy结合使用

在本篇中我们已经简单介绍过numba用于给计算密集型任务加速.作为python数值计算领域的事实标准,numba自然也对numpy有原生支持可以无缝集成.

numpy提供了一种高效的向量化数据结构和对应的高性能计算框架,而numba则可以在底层层面借助numpy的数据结构更高效的加速运算过程

numba对numpy的支持有多种形式:

+ numba理解对numpy的`ufunc`的调用,可以在编译后获得更加高效的等效本地代码以提高性能。
+ numba直接支持numpy数组,并可以有更高的数组访问效率;同时支持多数numpy提供的计算接口,在编译后也可以获得更高效的本地代码
+ numba提供了更加方便高效的用python构造`ufunc`的装饰器,同时提供了对`generalized universal functions`(广义泛函数)的支持,让numpy有了更好的扩展性

本文将介绍这两者如何结合使用.

## numba支持的numpy中的ufunc

numba有两个编译模式--`object mode`和`nopython mode`,官方推荐都使用`nopython mode`编译.这两个模式对numpy中ufunc的支持并不完全一致,下面是对应表

> 计算符号

UFUNC|object mode|nopython mode
---|---|---
`add`|Yes|Yes
`subtract`|Yes|Yes
`multiply`|Yes|Yes
`divide`|Yes|Yes
`logaddexp`|Yes|Yes
`logaddexp2`|Yes|Yes
`true_divide`|Yes|Yes
`floor_divide`|Yes|Yes
`negative`|Yes|Yes
`power`|Yes|Yes
`float_power`|Yes|Yes
`remainder`|Yes|Yes
`mod`|Yes|Yes
`fmod`|Yes|Yes
`divmod (timedelta上不支持)`|Yes|Yes
`abs`|Yes|Yes
`absolute`|Yes|Yes
`fabs`|Yes|Yes
`rint`|Yes|Yes
`sign`|Yes|Yes
`conj`|Yes|Yes
`exp`|Yes|Yes
`exp2`|Yes|Yes
`log`|Yes|Yes
`log2`|Yes|Yes
`log10`|Yes|Yes
`expm1`|Yes|Yes
`log1p`|Yes|Yes
`sqrt`|Yes|Yes
`square`|Yes|Yes
`cbrt`|Yes|Yes
`reciprocal`|Yes|Yes
`conjugate`|Yes|Yes
`gcd`|Yes|Yes
`lcm`|Yes|Yes

> 三角函数

UFUNC|object mode|nopython mode
---|---|---
`sin`|Yes|Yes
`cos`|Yes|Yes
`tan`|Yes|Yes
`arcsin`|Yes|Yes
`arccos`|Yes|Yes
`arctan`|Yes|Yes
`arctan2`|Yes|Yes
`hypot`|Yes|Yes
`sinh`|Yes|Yes
`cosh`|Yes|Yes
`tanh`|Yes|Yes
`arcsinh`|Yes|Yes
`arccosh`|Yes|Yes
`arctanh`|Yes|Yes
`deg2rad`|Yes|Yes
`rad2deg`|Yes|Yes
`degrees`|Yes|Yes
`radians`|Yes|Yes


> bit位计算

UFUNC|object mode|nopython mode
---|---|---
`bitwise_and`|Yes|Yes
`bitwise_or`|Yes|Yes
`bitwise_xor`|Yes|Yes
`bitwise_not`|Yes|Yes
`invert`|Yes|Yes
`left_shift`|Yes|Yes
`right_shift`|Yes|Yes


> 比较计算

UFUNC|object mode|nopython mode
---|---|---
`greater`|Yes|Yes
`greater_equal`|Yes|Yes
`less`|Yes|Yes
`less_equal`|Yes|Yes
`not_equal`|Yes|Yes
`equal`|Yes|Yes
`logical_and`|Yes|Yes
`logical_or`|Yes|Yes
`logical_xor`|Yes|Yes
`logical_not`|Yes|Yes
`maximum`|Yes|Yes
`minimum`|Yes|Yes
`fmax`|Yes|Yes
`fmin`|Yes|Yes


> 浮点数计算

UFUNC|object mode|nopython mode
---|---|---
`isfinite`|Yes|Yes
`isinf`|Yes|Yes
`isnan`|Yes|Yes
`signbit`|Yes|Yes
`copysign`|Yes|Yes
`nextafter`|Yes|Yes
`modf`|Yes|No
`ldexp`|Yes|Yes
`frexp`|Yes|No
`floor`|Yes|Yes
`ceil`|Yes|Yes
`trunc`|Yes|Yes
`spacing`|Yes|Yes


> 时间计算

UFUNC|object mode|nopython mode
---|---|---
`isnat`|Yes|Yes

## numba编译numpy的限制

numba对numpy原生支持,但也不是完全支持,在`@jit`装饰的函数中也仅是支持numpy的一部分特性.

numba支持大部分numpy原生的数据类型,仅不支持的常量类型包括

1. python对象(`object`)
2. 半精度和扩展精度的浮点数和复数类型(`float16`,`float128`,`complex256`)
3. 嵌套结构体


numba支持[大多数numpy运算符](https://numba.readthedocs.io/en/stable/reference/numpysupported.html#calculation)和[大多数numpy的dnarray的方法](https://numba.readthedocs.io/en/stable/reference/numpysupported.html#other-methods)

在算法方面numba也支持[大多数numpy中内置的算法](https://numba.readthedocs.io/en/stable/reference/numpysupported.html#functions).同时支持numpy中的如下几个模块

+ [random](https://numba.readthedocs.io/en/stable/reference/numpysupported.html#random),用于随机和分布
+ [stride-tricks](https://numba.readthedocs.io/en/stable/reference/numpysupported.html#stride-tricks),用于切分数组构造窗口

## 使用numba快速定义numpy的univeral function

numba提供了两个装饰器用于构造ufunc

+ 装饰器`@vectorize`用于将一个python函数包装为`univeral function`(泛函).它装饰的函数用于处理标量,即在广播中每个标量都会被计算的部分.调用泛函的数组总是返回和参数一样维度的数组.
+ 装饰器`@guvectorize`,用于将一个python函数包装为`generalized universal functions`(广义泛函数).它装饰的函数用于处理高维数组和标量,调用广义泛函的数组通常输入和输出的维度是不同的


### 装饰器`@vectorize`

`@vectorize`支持的参数按顺序包括:

+ `signatures=[]`:指定泛函的函数签名
+ `identity=None`:指定用于某些操作的中性元素,可选的有`0`,`1`,`None`,`"reorderable"`(可重新排序),默认为`None`,中性元素是在对数组元素执行一些操作时用于初始化结果的特殊值.例如对于加法操作中性元素是`0`,因为任何数加`0`都等于它本身;对于乘法操作中性元素是`1`,因为任何数乘以`1`都等于它本身.如果不额外指定,numba会根据调用情况自行分配
+ `nopython=True`,强制使用`nopython`模式执行,当使用`nopython`模式时numba会将被装饰的函数进行编译,这样它就可以完全在没有Python解释器的情况下运行,也就可以有更好的运行性能;但如果设置`nopython=False`时numba也会优先使用`nopython`模式,当无法使用时才会回退到`object`模式.在`object`模式下numba将识别可以编译的循环,并将其编译成在机器代码中运行的函数然后在解释器中运行其余代码.
+ `target='cpu'`,指定编译后被哪个平台使用,支持`cpu`--单线程CPU计算;`parallel`--多线程CPU计算;`cuda`--有cuda的GPU计算
+ `forceobj=False`,强制使用`object`模式运行.
+ `cache=False`,是否缓存编译,注意`target='cuda'`无法缓存
+ `locals={}`,指定函数的本地变量的类型,类似指定函数签名,也是起到静态化提高运行效率的作用


```python
import numpy as np
from numba import vectorize,float32, float64, int32,int64

@vectorize([float64(float64, float64)], identity=0)
def ucustom_sum(x, y):
    return x + y

result = ucustom_sum(np.array([1.0, 2.1, 3.2, 4.3]), np.array([5.4, 6.5, 7.6, 8.7]))
result
```




    array([ 6.4,  8.6, 10.8, 13. ])



#### 多签名泛函

python函数本身提供动态类型支持,比如上面的例子如果我们希望参数和返回值也可以是int类型这样就可以使用`@vectorize`的多签名声明.

写法很简单,之前的签名参数位置放的就是一个签名的列表,多签名声明就是扩展这个列表,把你觉得需要的签名都加上



```python
@vectorize([int32(int32, int32),
            int64(int64, int64),
            float32(float32, float32),
            float64(float64, float64)],
           identity=0)
def ucustom_sum(x, y):
    return x + y

result = ucustom_sum(np.array([1, 2, 3, 4]), np.array([5, 6, 7, 8]))
result
```




    array([ 6,  8, 10, 12])



#### 动态签名泛函

如果不输入签名,那么`@vectorize`也可以生效,它会在每次调用的时候现编译自动分析输入的类型和输出的代码推断签名.那自然的代价也是这种动态的编译带来的性能损失了.


```python
@vectorize
def ucustom_sum(x, y):
    return x + y

result = ucustom_sum(np.array([1, 2, 3, 4]), np.array([5, 6, 7, 8]))
result
```




    array([ 6,  8, 10, 12])



### 装饰器`@guvectorize`

装饰器`@guvectorize`用于定义`generalized universal functions`(广义泛函数).

很多时候操作不仅需要在标量上的函数上循环,还需要在向量(或数组)上的函数中循环.这个概念是在`universal function`即泛函上的推广,因此称为`generalized universal functions`(广义泛函数)简称`gufunc`.

在常规`ufunc`中初等函数仅限于逐元素运算,而`gufunc`则支持逐"子数组"运算的"子阵列".典型的例子是中值计算或卷积滤波器.与`vectorize()`函数相反,`guvectorize()`函数不返回它们的结果值,它们将它作为数组参数，它必须由函数填充。这是因为数组实际上是由NumPy的dispa分配的

`@guvectorize`的参数按顺序为:

+ `signatures`,广义泛函的签名,需要注意`@guvectorize`装饰的函数返回值一定为`void`,调用时返回的结果则放在签名参数的最后一位
+ `layout`,广义泛函的核心布局,`layout`这个参数的类型是str,形式如`(m,n),(n,p)->(m,p)`用于描述调用时输入参数shape和输出参数shape间的关系,`->`前面的是调用时参数描述,后面则是返回值描述.常量的核心形状描述为`()`,1维向量描述为`(n)`,2维维`(m,n)`依次类推.
+ `identity=None`
+ `nopython=True`
+ `target='cpu'`
+ `forceobj=False`
+ `cache=False`
+ `locals={}`


#### 返回向量

下面这个例子我们定义一个将一个输入向量每个元素加个常量值获得一个新输出向量的例子


```python
from numba import guvectorize,int64

@guvectorize([(int64[:], int64, int64[:])], '(n),()->(n)')
def g(x, y, res):
    for i in range(x.shape[0]):
        res[i] = x[i] + y
```


```python
g(np.arange(5), 2)
```




    array([2, 3, 4, 5, 6])



#### 返回常量

我们的返回值声明必须是一个向量,但如果将核心中返回值部分声明为一个常量,我们可以在函数实现的最后将结果未知的第一位设置成返回值


```python
@guvectorize([(int64[:], int64, int64[:])], '(n),()->()')
def g(x, y, res):
    acc = 0
    for i in range(x.shape[0]):
        acc += x[i] + y
    res[0] = acc
```


```python
g(np.arange(5), 2)
```




    20


