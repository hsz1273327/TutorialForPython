
# Cython纯净模式

所谓的纯净模式就是cython直接编译`.py`文件的模式.

在某些情况下,希望加速Python代码,而不会失去与Python解释器一起运行的能力.可以使用Cython编译纯Python脚本,但通常只能以20％-50％的速度增长.

为了超越此范围,Cython提供了语言结构,为Python模块添加静态类型和cythonic功能,使其在编译时运行得更快,同时仍然允许它被解释.有两种方案可以实现这一需求:


+ 通过导入cython模块后使用其中的特殊功能和装饰器完成
+ 通过扩展的`.pxd`文件

尽管通常不建议在`.pyx`文件中直接编写Cython代码,但更容易的测试,可以方便的与纯Python开发人员的协作等特点也为其提供了合理性.

在纯净python源文件下，你或多或少受限于在Python中的语法表达,如果希望跳过python语法,只能用具有扩展语言语法的`.pyx`文件完成,因为它依赖于`Cython`编译器的特性.

cython可以使用`cython.compiled`来反射是否运行的是被编译的版本

`.pxd`文件中可以申明使用`C/C++`扩展,因此可以在`.py`文件中根据需要使用`c/c++`的编写的函数.


## 通过cython模块中的特殊功能和装饰器扩展

这种方式相比前面的使用`pxd`申明扩展的方式更加方便,所有这些特殊功能和装饰器都是非侵入式的,加上去掉都不会影响原本`.py`源代码在python解释器中的工作.

### 可用于申明的C类型


cython中常用的C语言类型有:

cython中类型|类型说明
---|---
cython.int| 整形
cython.long|长整形
cython.double|双精度浮点型
cython.char|字符型


其他的包括无符号整形之类的C语言中的基础类型也都有,这边不再复述.

另外一个特殊的类型就是指针,cython中指针类型就是基础类型前面加上`p_`,如整形数指针就是`cython.p_int`


### 常用的声明函数和装饰器有

不同于`.pyx`文件,`.py`文件需要符合python语法,因此很多申明和关键字需要使用函数或者类等对象来代替,纯净模式更多的是静态化参数以此来提高效率.下面是用于申明的函数和装饰器

+ `cython.declare(**kws)`

    用于申明变量
    
+ `cython.struct(**kws)` 

    申明一个结构体
    
+ ` cython.union(**kws)`

    申明一个联合体
    
+ `@cython.locals(**kws)`

    用于声明函数或者方法的参数和内部变量,即便是python方法也可以声明变量类型,这样静态化也可以获得提速
    
+ `@cython.returns([cython_type])`

    用于申明函数或者方法的参数和内部变量
    
+ `@cython.ccall`

    申明可被python解释器调用的cython函数.相当于`.pyx`中的`cpdef`定义的函数或方法
    
+ `@cython.cfunc`

    申明c/c++语言函数,这种函数会跳过运行时直接执行,而且隐藏在python解释器之下,只有模块中才可以调用
    
+ `@cython.inline`

    申明函数为`inline`函数
    
### 常用的特殊函数

处理C语言函数时,我们很有可能需要使用一些关于内存指针的操作,这些操作python自己是没有的,因此Cython也提供一些这种特殊的函数

+ `cython.address(x)`

    获取变量的指针地址

+ `cython.sizeof(x)`

    获取变量的地址空间大小

+ `cython.typedef(x)`

    用于获取一个给定指针名称下的变量类型的类型
    
+ `cython.cast(T,x,typecheck=True)`

    用于将变量指定为某一类型,类似C/C++语言中的`<T>t`.注意这个函数是不安全的,容易内存泄漏.可选参数`typecheck=True`相当于`<T?>t`


### 常用编译指示装饰器

+ `@cython.boundscheck(bool)`

    用于设定是否进行边界检查,默认值为True。
    
    
+ `@cython.wraparound(bool)`

    用于设定是否进行数组负索引检查,默认值为True。
    
    
+ `@cython.initializedcheck(bool)`

    用于设定访问或分配内存视图时是否检查它是否被初始化.默认值为True。
    
    
+ `@cython.overflowcheck`

    如果设置为True，当溢出的C整数算术运算上引发了异常时，会执行适度的运行时惩罚,但即便如此还是比python的int运算快很多,默认为False
    
    
+ `@cython.overflowcheck.fold`

    如果设置为True，并且overflowcheck为True，则检查嵌套的溢出位,和有副作用的算术表达式,而不是每个步骤都检查。 依赖于不同的编译器，体系结构和优化设置，这项选项可能有助于提高性能也可能损害性能。 默认值为True。
    
    
+ `@cython.nonecheck`

    如果设置为False，Cython可以自由地假定 对变量类型的本地字段访问为扩展类型,或者 当变量被设为None时,对缓冲区变量的缓冲区访问永远不会发生。否则插入一个检查并引发适当的异常。
    
这些装饰器可以放在函数上标记好

### 常用的编译器指示注释

编译器可以识别在源文件开始部分的注释为全局的编译器指示,常见的有

+ `#cython: language_level=3`标记编译目标为python3
+ `#cython: boundscheck = False`设置全局不进行边界检查

编译器设置的参数可以在前面的Cython基本流程部分看到


```python
%%writefile B.py
#cython: language_level=3
import cython

if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")
    
@cython.boundscheck(False)
@cython.ccall
@cython.returns(cython.int)
@cython.locals(x=cython.int, y=cython.int,a = cython.int)
def myfunction(x, y=2):
    a = x-y
    return a + x * y

@cython.cfunc
@cython.returns(cython.double)
@cython.locals(a = cython.double)
def _helper(a):
    return a + 1

@cython.cclass
class A:
    cython.declare(a=cython.int, b=cython.int)
    def __init__(self, b=0):
        self.a = 3
        self.b = b
    @cython.ccall
    @cython.locals(x=cython.double)
    def foo(self, x):
        print(x + _helper(1.0))
```

    Overwriting B.py



```python
import B
```

    Just a lowly interpreted script.



```python
B.myfunction(10)
```




    28




```python
a = B.A()
a.foo(2.7)
```

    4.7



```python
%%writefile setup.py

from distutils.core import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize("B.py",language="c++")
)
```

    Overwriting setup.py



```python
!python setup.py build_ext --inplace
```

    Please put "# distutils: language=c++" in your .pyx or .pxd file(s)
    Compiling B.py because it changed.
    [1/1] Cythonizing B.py
    running build_ext
    building 'B' extension
    creating build
    creating build\temp.win-amd64-3.6
    creating build\temp.win-amd64-3.6\Release
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\87\Anaconda3\include -IC:\Users\87\Anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /EHsc /TpB.cpp /Fobuild\temp.win-amd64-3.6\Release\B.obj
    B.cpp
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\87\Anaconda3\libs /LIBPATH:C:\Users\87\Anaconda3\PCbuild\amd64 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB\amd64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x64" /EXPORT:PyInit_B build\temp.win-amd64-3.6\Release\B.obj /OUT:C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\python性能优化\Cython纯净模式\B.cp36-win_amd64.pyd /IMPLIB:build\temp.win-amd64-3.6\Release\B.cp36-win_amd64.lib
    B.obj : warning LNK4197: export 'PyInit_B' specified multiple times; using first specification
       Creating library build\temp.win-amd64-3.6\Release\B.cp36-win_amd64.lib and object build\temp.win-amd64-3.6\Release\B.cp36-win_amd64.exp
    Generating code
    Finished generating code



```python
import B
```

    Yep, I'm compiled.



```python
B.myfunction(10)
```




    28




```python
a = B.A()
a.foo(2.7)
```

    4.7



```python
!cython -a B.py
```

## cython纯净模式福利--类型自动转换

C 类型|从pyhton中获得|返回到python中
---|---|---
[unsigned] char, [unsigned] short, int, long|int|	int
unsigned int, unsigned long, [unsigned] long long|int|int
float, double, long double	|int, float|float
`char*`	|bytes	|bytes
struct, union|--- |dict


除此之外同构定长列表/元组可以与c中数组自动转化

```python
import cython

@cython.locals(counts=cython.int[10], digit=cython.int)
def count_digits(digits):
    """
    >>> digits = '01112222333334445667788899'
    >>> count_digits(map(int, digits))
    [1, 3, 4, 5, 3, 1, 2, 2, 3, 2]
    """
    counts = [0] * 10
    for digit in digits:
        assert 0 <= digit <= 9
        counts[digit] += 1
    return counts
    
```

### 纯python文件扩展的局限性

这种方式的缺点在于:

+ 语法不优雅,堆叠3个装饰器来装饰一个函数看起来很不美观
+ 默认无法使用`type hint`,测试结果看cython解释器无法支持`type hint`,这个特性会在后续的版本中改善

## 使用`.pxd`申明要用的C/C++函数

使用上面这种方式有个很大的缺陷就是无法使用C/C++写好的函数,要让这个可行需要有一个`.pxd`文件用于声明用到的函数,并将其包装为`cpdef`的形式


```python
%%writefile C.py
#cython: language_level=3
import cython

if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")
    from math import sin
    
@cython.boundscheck(False)
@cython.ccall
@cython.returns(cython.int)
@cython.locals(x=cython.int, y=cython.int,a = cython.int)
def myfunction(x, y=2):
    a = x-y
    return a + x * y

@cython.cfunc
@cython.returns(cython.double)
@cython.locals(a = cython.double)
def _helper(a):
    return a + 1

@cython.returns(cython.double)
@cython.locals(x=cython.double)
def echo_sin(x):
    return sin(x)

@cython.cclass
class A:
    cython.declare(a=cython.int, b=cython.int)
    def __init__(self, b=0):
        self.a = 3
        self.b = b
    @cython.ccall
    @cython.locals(x=cython.double)
    def foo(self, x):
        print(x + _helper(1.0))
```

    Overwriting C.py



```python
%%writefile C.pxd
#cython: language_level=3
cdef extern from "math.h":
    cpdef double sin(double x)

```

    Overwriting C.pxd



```python
import C
```

    Just a lowly interpreted script.



```python
%timeit C.echo_sin(3)
```

    The slowest run took 26.72 times longer than the fastest. This could mean that an intermediate result is being cached.
    1000000 loops, best of 3: 249 ns per loop



```python
%%writefile setup.py

from distutils.core import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize("C.py",language="c++")
)
```

    Overwriting setup.py



```python
!python setup.py build_ext --inplace
```

    Please put "# distutils: language=c++" in your .pyx or .pxd file(s)
    Compiling C.py because it changed.
    [1/1] Cythonizing C.py
    running build_ext
    building 'C' extension
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\87\Anaconda3\include -IC:\Users\87\Anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /EHsc /TpC.cpp /Fobuild\temp.win-amd64-3.6\Release\C.obj
    C.cpp
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\87\Anaconda3\libs /LIBPATH:C:\Users\87\Anaconda3\PCbuild\amd64 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB\amd64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x64" /EXPORT:PyInit_C build\temp.win-amd64-3.6\Release\C.obj /OUT:C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\python性能优化\Cython纯净模式\C.cp36-win_amd64.pyd /IMPLIB:build\temp.win-amd64-3.6\Release\C.cp36-win_amd64.lib
    C.obj : warning LNK4197: export 'PyInit_C' specified multiple times; using first specification
       Creating library build\temp.win-amd64-3.6\Release\C.cp36-win_amd64.lib and object build\temp.win-amd64-3.6\Release\C.cp36-win_amd64.exp
    Generating code
    Finished generating code



```python
import C
```

    Yep, I'm compiled.



```python
%timeit C.echo_sin(3)
```

    The slowest run took 51.80 times longer than the fastest. This could mean that an intermediate result is being cached.
    10000000 loops, best of 3: 134 ns per loop


### 将所有申明迁移至`.pxd`文件


像上面这种写法已经引入了一个新的文件,既然如此为什么不把申明用的这些个装饰器都移到`.pxd`文件中增加可读性呢

下面是一个纯python源文件


```python
%%writefile A.py
import cython

if cython.compiled:
    print("Yep, I'm compiled.")
    
else:
    print("Just a lowly interpreted script.")
    from math import sin


def myfunction(x, y=2):
    a = x-y
    return a + x * y

def echo_sin(x):
    return sin(x)
    
def _helper(a):
    return a + 1

class A:
    def __init__(self, b=0):
        self.a = 3
        self.b = b

    def foo(self, x):
        print(x + _helper(1.0))
        
```

    Overwriting A.py



```python
import A
```

    Just a lowly interpreted script.



```python
A.myfunction(10)
```




    28




```python
%timeit A.echo_sin(2.7)
```

    The slowest run took 25.54 times longer than the fastest. This could mean that an intermediate result is being cached.
    1000000 loops, best of 3: 225 ns per loop


使用`.pxd`为其申明


```python
%%writefile A.pxd
#cython: language_level=3
cdef extern from "math.h":
    cpdef double sin(double x)

cpdef int myfunction(int x, int y=*)

cdef double _helper(double a)

cdef class A:
    cdef public int a,b
    cpdef foo(self, double x)
```

    Overwriting A.pxd


那么`Cython`将会将`A.py`编译成如下：

```cython
cdef extern from "math.h":
    cpdef double sin(double x)

cpdef int myfunction(int x, int y=2):
    a = x-y
    return a + x * y
def double echo_sin(double x):
    return sin(x)

cdef double _helper(double a):
    return a + 1

cdef class A:
    cdef public int a,b
    def __init__(self, b=0):
        self.a = 3
        self.b = b

    cpdef foo(self, double x):
        print x + _helper(1.0)
```

注意:

+ 使用`*`通配符可以将Python的参数默认值包装给`.pxd`中的定义，即可以从Python访问

`cpdef int myfunction(int x, int y=*)`

+ 内部函数的C函数签名可以声明为cdef

`cdef double _helper(double a)`

+ cdef class用于申明扩展类型

+ 如果属性有读取/写入Python访问权限，则cdef类属性必须声明为cdef public，cdef readonly为只读Python访问，或者是纯Cdef为内部C级属性

+ cdef class 中方法必须声明为

    + cpdef Python可见方法
    + cdef用于内部C方法


```python
%%writefile setup.py

from distutils.core import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize("A.py",language="c++")
)
```

    Overwriting setup.py



```python
!python setup.py build_ext --inplace
```

    Please put "# distutils: language=c++" in your .pyx or .pxd file(s)
    Compiling A.py because it changed.
    [1/1] Cythonizing A.py
    running build_ext
    building 'A' extension
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\87\Anaconda3\include -IC:\Users\87\Anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /EHsc /TpA.cpp /Fobuild\temp.win-amd64-3.6\Release\A.obj
    A.cpp
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\87\Anaconda3\libs /LIBPATH:C:\Users\87\Anaconda3\PCbuild\amd64 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB\amd64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x64" /EXPORT:PyInit_A build\temp.win-amd64-3.6\Release\A.obj /OUT:C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\python性能优化\Cython纯净模式\A.cp36-win_amd64.pyd /IMPLIB:build\temp.win-amd64-3.6\Release\A.cp36-win_amd64.lib
    A.obj : warning LNK4197: export 'PyInit_A' specified multiple times; using first specification
       Creating library build\temp.win-amd64-3.6\Release\A.cp36-win_amd64.lib and object build\temp.win-amd64-3.6\Release\A.cp36-win_amd64.exp
    Generating code
    Finished generating code



```python
import A
```

    Yep, I'm compiled.



```python
A.myfunction(12)
```




    34




```python
%timeit A.echo_sin(2.7)
```

    The slowest run took 90.59 times longer than the fastest. This could mean that an intermediate result is being cached.
    10000000 loops, best of 3: 120 ns per loop


### 使用`.pxd`申明扩展纯python的局限性

使用`.pxd`扩展`.py`源文件的方式最大的缺点在于可维护性,一旦有改动那么无论`.py`和`.pxd`文件都得改动.而且因为使用`cython`语法定义`.pxd`文件,所以对于不会cython的用户很不友好.

另一局限性在于使用c/c++函数或者标准库时只能在`.pxd`文件下申明,因此必须在`.py`文件中判断是否被编译,而且必须实现一个同名的python对象来为纯python环境提供支持.

## 纯净模式的局限性

无论是否要使用`.pxd`申明文件,纯净模式都无法在实现上使用C++中STL容器和算法,也有很多cython语言特性无法实现.

## 使用typehits申明静态类型

在python3.5发布后,cython社区也提出了使用`type hint`来申明cython纯净模式的提议--
[Python Typing Proposal](https://github.com/cython/cython/wiki/Python-Typing-Proposal).在0.27版本以后,cython已经完全支持这种静态类型申明的方式了.纯净模式代码可以比之前的优雅不少


```python
%%writefile BB.py
#cython: language_level=3
import cython

if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")
    
@cython.boundscheck(False)
@cython.ccall
def myfunction(x:cython.int, y:cython.int=2)->cython.int:
    a:cython.int
    a = x-y
    return a + x * y

@cython.cfunc
def _helper(a:cython.double)->cython.double:
    return a + 1

@cython.cclass
class A:
    a:cython.int
    b:cython.int
    def __init__(self, b=0):
        self.a = 3
        self.b = b
        
    @cython.ccall
    def foo(self, x:cython.double)->cython.double:
        print(x + _helper(1.0))
```

    Overwriting BB.py



```python
import BB
```

    Just a lowly interpreted script.



```python
BB.myfunction(10)
```




    28




```python
a = BB.A()
a.foo(2.7)
```

    4.7



```python
!cythonize -i -3 -a BB.py
```

    Compiling C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\BB.py because it changed.
    [1/1] Cythonizing C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\BB.py
    running build_ext
    building 'BB' extension
    creating C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release
    creating C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users
    creating C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87
    creating C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents
    creating C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub
    creating C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub\my
    creating C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub\my\TutorialForPython
    creating C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs
    creating C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能
    creating C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ic:\users\87\anaconda3\include -Ic:\users\87\anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /TcC:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\BB.c /FoC:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\BB.obj
    BB.c
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:c:\users\87\anaconda3\libs /LIBPATH:c:\users\87\anaconda3\PCbuild\amd64 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB\amd64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x64" /EXPORT:PyInit_BB C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\BB.obj /OUT:C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\BB.cp36-win_amd64.pyd /IMPLIB:C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\BB.cp36-win_amd64.lib
    BB.obj : warning LNK4197: export 'PyInit_BB' specified multiple times; using first specification
       Creating library C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\BB.cp36-win_amd64.lib and object C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\tmpm5d7r9zk\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython纯净模式\BB.cp36-win_amd64.exp
    Generating code
    Finished generating code



```python
import BB
```

    Yep, I'm compiled.



```python
BB.myfunction(10)
```




    28




```python
a = BB.A()
a.foo(2.7)
```

    4.7





    0.0


