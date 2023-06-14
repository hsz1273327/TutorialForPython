
# Cython的简单介绍

Cython是针对python模块的一个优化工具,它并不使用jit技术,因此它的使用有一定局限性的.


Cython可以做以下的事情:

+ 将python代码翻译为C语言代码,
+ 将python代码编译为python可以直接调用的动态链接库
+ 通过为python代码指定类型静态化模块,生成python可以直接调用的动态链接库
+ 编译python语法的的超集,Cython语法的源文件`.pyx`文件生成python可以直接调用的动态链接库
+ 通过Cython语法的头文件`.pxd`申明C/C++语言的库,再通过Cython语法的源文件`.pyx`文件生成python可以直接调用的动态链接库

需要注意的是cython编译出来的C/C++语句依然需要使用python的动态库`libpython`,因此要手动使用C编译器编译就需要制定这个库的位置.

Cython提供了两个名,命令行工具

+ cython

    将指定的python,cython源文件翻译为C/C++源文件

+ cythonize

    使用标准库的`distutils`调用C/C++编译器编译由cython翻译出来的C/C++源文件.
    
另外cython为`jupyter notebook`提供了专用的魔术命令`%%cython`,使用它可以直接在notebook上执行cython语法的语句.

## Cython的使用方式

Cython需要编译,本质上来说Cython只是把Cython代码编译成C/C++代码而已.

+ 编写符合Cython语法的`.pyx`源文件
+  (可选)用`.pxd`申明`.pyx`源文件或者`c++`源文件的接口,它类似`c++`中的`.h`文件
+ 将源码编译为动态链接库
+ 在其他python包中`import`这个动态链接库进行包装或者调用

## Cython项目的文件组成

Cython解释器可以识别`.py`,`.cpp`,`.c`,`.h`,`.pyx`,`.pxd`,`.pxi`,其中

+ `.py`是python的源码,一般用在纯净模式下
+ `.cpp`,`.c`,`.h`是c/c++的源码和头文件,一般用在包装模式下
+ `.pyx`,`.pxd`,`.pxi`是cython源码和头文件,用在一般模式下.

而cython源文件中

+ `.pyx` 为源码文件

    
+ `pxd`为申明文件

    申明文件可以包含:
    
    + 任何一种C型声明
    + extern C函数或变量声明
    + 模块实现的声明
    + 扩展类型的定义部分
    + 外部函数库的所有声明等
    
    
    申明文件不能包含:
    
    + 任何非外部C变量声明
    + C或Python功能的实现
    + Python类定义和Python可执行语句
    + 任何被定义为公共的声明即申明可以被其他Cython模块访问.这是没有必要的，因为它是自动的.而且公共声明只需要使外部C代码可以访问.
    
+ `.pxi`为包含文件
    任何Cython代码,因为整个文件都是文字嵌入在引入处的位置,类似于c++中`#include`的机制


## hellowold


```python
%%writefile helloworld/helloworld.pyx
# distutils: language=c++
def run():
    print("Hello World")
    return True
```

    Overwriting helloworld/helloworld.pyx


## Cython的编译方式

Cython的编译有两种途径:

+ 使用`setup.py`编译并安装模块
+ 使用`cythonize`工具编译模块

无论是使用哪种方式编译,都是调用标准库`distutils`.而且都需要用到C/C++的编译器,因此一个比较方便的方法是使用`setup.cfg`文件指明模块的编译参数,

```cfg
[build_ext]
inplace=1

[build]
compiler = msvc
```

接下来我们来编译上面的`helloword`例子

### 使用setup.py编译并安装模块

使用setup.py编译模块并安装的步骤如下:

1. 编写`setup.py`安装文件,其中使用`Cython.Build.cythonize`函数构建模块
2. 命令行使用`python setup.py build_ext`来编译源文件生成模块,如果没有写`setup.cfg`,我们可以在后面添加
    + `--inplace`指定编译后的动态链接库在源文件目录;
    + `--compiler`或者`-c`以指定使用的C/C++编译器.比如windows上`msvc`是指的微软的vc编译器,`mingw32`指的是`mingw32`编译器等


```python
%%writefile setup.py
from pathlib import Path
from distutils.core import setup
from Cython.Build import cythonize

dir_path = Path(__file__).absolute().parent


setup(
    ext_modules = cythonize(str(dir_path.joinpath("helloworld.pyx")))
)
```

    Overwriting setup.py



```python
!python setup.py build_ext
```

    Compiling C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython的基本工作流程\helloworld.pyx because it changed.
    [1/1] Cythonizing C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython的基本工作流程\helloworld.pyx
    running build_ext
    building 'helloworld' extension
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\87\Anaconda3\include -IC:\Users\87\Anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /EHsc /TpC:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython的基本工作流程\helloworld.cpp /Fobuild\temp.win-amd64-3.6\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython的基本工作流程\helloworld.obj
    helloworld.cpp
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\87\Anaconda3\libs /LIBPATH:C:\Users\87\Anaconda3\PCbuild\amd64 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB\amd64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x64" /EXPORT:PyInit_helloworld build\temp.win-amd64-3.6\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython的基本工作流程\helloworld.obj /OUT:C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython的基本工作流程\helloworld.cp36-win_amd64.pyd /IMPLIB:build\temp.win-amd64-3.6\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython的基本工作流程\helloworld.cp36-win_amd64.lib
    helloworld.obj : warning LNK4197: export 'PyInit_helloworld' specified multiple times; using first specification
       Creating library build\temp.win-amd64-3.6\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython的基本工作流程\helloworld.cp36-win_amd64.lib and object build\temp.win-amd64-3.6\Release\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\使用Cython优化python程序的性能\Cython的基本工作流程\helloworld.cp36-win_amd64.exp
    Generating code
    Finished generating code



```python
import helloworld
```


```python
helloworld.run()
```

    Hello World





    True



### 使用cythonize工具编译模块

cythonize是cython官方提供的编译工具,用起来和gcc差不太多.但是无法指定使用的C编译器,因此只能先用`setup.cfg`配置好编译器再执行.

常用的参数有:

+ `-3` 指明使用的是python3语法
+ `-i` 指明编译时是inplace的
+ `-a` 输出编译为C后各行对应的代码


```python
!cythonize -i -3 -a helloworld.pyx
```

    running build_ext


## 更加丰富的编译设置

如果你的模块像上面的例子中只有一个源文件.那么`helloworld`中的`setup.py`就已经可以了,但如果不止一个,或者有一些针对编译器的设置,那么如下的写法是更好的选择


```python
%%writefile setup.py

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

extension = Extension(
           "helloworld",
           sources=["helloworld.pyx"],
           #include_dirs=[numpy.get_include()], # 如果用到numpy
           language="c++"
)

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = cythonize(extension),
)

```

    Overwriting setup.py



```python
!python setup.py build_ext --inplace
```

    running build_ext


可选的编译器设置包括:

+ cythonize 用来确定所要编译的内容,它的参数可以有:

`ext_modules = cythonize("src/*.pyx"[, include_path = [...][,compiler_directives={<option>=<value>}]])`

+ `include_path`是编译所需的源文件,这里可以是`.py`文件,`.pyx`文件,`.pxd`文件,`.c`文件,`.h`文件等,也可以是几个扩展类 型`distutils.extension.Extension`的对象,而`Extension`对象又可以这样定义:

```python

 Extension(name, [source...],
        include_dirs = [...],
        libraries = [...],
        library_dirs = [...])
```

+ `compiler_directives`则是编译的选项,有如下关键字:

    + boundscheck (True / False)
    
        如果设置为False，Cython可以自由地假定代码中的索引操作,将不会导致任何IndexErrors被抛出。
        只有当索引可以被确定为非负数（或者wraparound为False），列表，元组和字符串才会受影响。
        通常触发IndexError的条件可能会导致segfault或数据损坏，如果这被设置为False。
        默认值为True。
        
    + wraparound (True / False)
    
        在Python中，数组可以相对于结束索引(负索引)。而在C中是不支持负索引的。
        如果设置为False，Cython既不检查也不正确处理负索引，可能导致段错误或数据损坏。
        默认值为True。
        
    + initializedcheck (True / False)
    
        如果设置为True，Cython会在访问或分配内存视图时检查它是否被初始化。
        将此设置为False将禁用这些检查。
        默认值为True。
        
    + nonecheck (True / False)
    
        如果设置为False，Cython可以自由地假定 对变量类型的本地字段访问为扩展类型,或者 当变量被设为None时,对缓冲区变量的缓冲区访问永远不会发生。否则插入一个检查并引发适当的异常。
        
        由于性能原因，默认情况下关闭。
        默认值为False。
        
    + overflowcheck (True / False)
    
        如果设置为True，当溢出的C整数算术运算上引发了异常时，会执行适度的运行时惩罚,但即便如此还是比python的int运算快很多,默认为False
        
    + overflowcheck.fold (True / False)
    
        如果设置为True，并且overflowcheck为True，则检查嵌套的溢出位,和有副作用的算术表达式,而不是每个步骤都检查。
        依赖于不同的编译器，体系结构和优化设置，这项选项可能有助于提高性能也可能损害性能。
        默认值为True。
        
    + embedsignature (True / False)
    
        如果设置为True，Cython将在所有Python可见函数和类的docstring中嵌入调用签名的文本副本。
        像IPython和epydoc这样的工具可以显示签名，否则编译后就无法检索。
        默认值为False。
        
    + cdivision (True / False)
    
        如果设置为False，Cython将调整余数和商值运算符C类型以匹配Python的int（当操作数具有相反的符号时不同），并且当右操作数为0时产生ZeroDivisionError。这将会有超过35％的性能损失.
        如果设置为True，则不执行任何检查。
        
    + cdivision_warnings (True / False)
    
        如果设置为True，当使用负操作数执行除法时，Cython将发出运行时警告。 默认值为False.
        
    + always_allow_keywords (True / False)
    
        在构造取零或一个参数的函数/方法时，METH_NOARGS和METH_O置空。
        对具有多个参数的特殊方法和函数没有影响。
        METH_NOARGS和METH_O签名提供了更快的调用约定，但不允许使用关键字
        
    + profile (True / False)
    
        为编译成的C代码写上python分析的钩子,默认为False
        
    + linetrace (True / False)
    
        为编译后的C代码写入Python分析器或覆盖报告的跟踪钩子。
        这也会启用profile。
        默认值为False。

    + infer_types (True / False)
    
        推断函数体中未声明类型变量的类型。默认值为None，表示只允许安全（语义上不变的）推断。特别地，推断用于算术表达式中的变量的整数类型被认为是不安全的（由于可能的溢出），并且必须被明确请求。
        
    + language_level (2/3)
    
        全局设置要用于模块编译的Python语言级别。默认为与Python 2兼容。要启用Python 3源代码语义，请在模块开头将其设置为3，或将“-3”命令行选项传递给编译器。请注意，cimport和包含的源文件从正在编译的模块继承此设置，除非他们明确设置自己的语言级别。
        
    + c_string_type (bytes / str / unicode)
    
        从`char *`或`std :: string`全局设置隐式强制的类型
        
    + c_string_encoding (ascii, default, utf-8, etc.)
    
        全局设置在将`char *`或`std：string`隐式强制转化为unicode对象时使用的编码。从unicode对象到C类型的强制只允许设置为ascii或默认，后者意思是在Python 3中是utf-8
        
    + type_version_tag (True / False)
    
        通过设置类型标志Py_TPFLAGS_HAVE_VERSION_TAG，在CPython中启用扩展类型的属性缓存。
        默认值为True，表示为Cython实现的类型启用了缓存。
        在类型需要在内部与其tp_dict进行协调而不关注缓存一致性的罕见情况下禁用它，可以将此选项设置为False。
        
    + unraisable_tracebacks (True / False)
    
        是否在抑制不可取消的异常时打印回溯。
        



## 在Cython源文件中声明编译设置

上面的方法将编译设置都放在`setup.py`中,这样做略繁琐,也无法在源文件中体现.一个更加优雅的方法是使用类似python中声明编码一样,在源文件的初始几行中.这种方式也是现在官方推荐的写法,使用这种方式也可以更加方便的在jupyter notebook中使用C++的一些特性


```python
%load_ext Cython
```


```cython
%%cython
# distutils: language=c++
def f(double x):
    return x**2-x

def integrate_f(double a, double b, int N):
    cdef int i
    cdef double s, dx
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s += f(a+i*dx)
    return s * dx
```

这种方式的`setup.py`文件也更加简单,只需用`cythonize`函数指定所有`.pyx`文件即可

```python
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("*.pyx")
)
```

# 分析 Cython 程序瓶颈

Cython 中类型声明非常重要，但是我们不加类型标注它依然是一个合法的Cython程序,所以自然而然地,我们会担心漏加类型声明.不过好在 Cython 提供了一个很好的工具,可以方便地检查 Cython 程序中哪里可能可以进一步优化.


```python
!cython -a helloworld.pyx
```

之后我们的文件夹下就会看到一个html文件,其中黄色的部分就是与python交互的部分,也就是性能瓶颈
