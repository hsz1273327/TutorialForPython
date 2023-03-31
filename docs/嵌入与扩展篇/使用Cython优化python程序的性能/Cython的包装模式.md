
# 用Cython包装C++代码

Cython最大的作用其实是作为C/C++代码和python代码的桥梁,比如我们已经有一个C++写的程序了,但我们希望让python可以调用它,传统的做法是使用ctypes或者cffi作为桥,但这种方式需要有相当的C/C++知识.Cython的话基本可以无痛进行C++代码的包装,这是通过使用外部声明来声明库函数和要使用的库中的C函数来实现的.




Cython现在原生的支持大多数的C++语法.
尤其是:
现在可以使用`new`和`del`关键字动态分配C++对象.

+ C++对象可以进行堆栈分配
+ C++类可以使用新的关键字`cppclass`声明
+ 支持模板化类和函数
+ 支持重载函数
+ 支持C++操作符(例如operator +,operator [],...)的重载

我们通过包装一个例子来看看cython是如何包装c/c++代码的

## 封装步骤

封装C/C++的步骤大致有如下几步:

1. 在setup.py脚本中或在源文件中本地指定C ++语言。
2. 使用`cdef extern from 头文件`创建一个或多个`.pxd`文件.在pxd文件中，以`cdef cppclass`来声明类并且声明公共名称(变量,方法和构造函数）
3. 通过`cimport`引入`pxd`文件，进行`pxd`的实现代码，也就是`.pyx`文件。


## 最简单的一个例子

这个例子用来介绍Cython包装C/C++代码的步骤.例子是一个长方形类,C++代码部分如下:


```python
%load_ext Cython
```


```python
%%writefile Rectangle.h

namespace shapes {
    class Rectangle {
    public:
        static int do_something();
        int x0, y0, x1, y1;
        Rectangle();
        Rectangle(int x0, int y0, int x1, int y1);
        ~Rectangle();
        int getArea();
        void getSize(int* width, int* height);
        void move(int dx, int dy);
    };
}
```

    Overwriting Rectangle.h



```python
%%writefile Rectangle.cpp
#include "Rectangle.h"

namespace shapes {

  Rectangle::Rectangle() { }
    int Rectangle::do_something(){
        return 0;
    }

    Rectangle::Rectangle(int X0, int Y0, int X1, int Y1) {
        x0 = X0;
        y0 = Y0;
        x1 = X1;
        y1 = Y1;
    }

    Rectangle::~Rectangle() { }

    int Rectangle::getArea() {
        return (x1 - x0) * (y1 - y0);
    }

    void Rectangle::getSize(int *width, int *height) {
        (*width) = x1 - x0;
        (*height) = y1 - y0;
    }

    void Rectangle::move(int dx, int dy) {
        x0 += dx;
        y0 += dy;
        x1 += dx;
        y1 += dy;
    }

}
```

    Overwriting Rectangle.cpp


## 用于包装的pyx文件

要包装C++文件,我们得先在cython中声明出这个C++的类,在cython中申明C或者C++的内容(接口)需要使用`cdef extern from ....`这种语法(外部声明).

在


```python
%%writefile rect.pyx
#cython: language_level=3
# distutils: language = c++
# distutils: sources = Rectangle.cpp


cdef extern from "Rectangle.h" namespace "shapes":
    cdef cppclass Rectangle:
        Rectangle() except +
        Rectangle(int, int, int, int) except +
        int x0, y0, x1, y1
        int getArea()
        void getSize(int* width, int* height)
        void move(int, int)
        @staticmethod
        int do_something()
cdef class PyRectangle:
    cdef Rectangle c_rect      # hold a C++ instance which we're wrapping
    def __cinit__(self, int x0, int y0, int x1, int y1):
        self.c_rect = Rectangle(x0, y0, x1, y1)
    def get_area(self):
        return self.c_rect.getArea()
    def get_size(self):
        cdef int width, height
        self.c_rect.getSize(&width, &height)
        return width, height
    def move(self, dx, dy):
        self.c_rect.move(dx, dy)
    @staticmethod
    def do_something():
        return Rectangle.do_something()
```

    Overwriting rect.pyx


这样，我们就完成了C++的封装。而且从Python的开发角度来看，这个扩展类型看起来和感觉就像一个本地定义的Rectangle类。
需要注意的是，如果我们需要额外的属性设置方法，可以自己再添加.

## setup.py的写法

我们的setup.py和之前差不多的写法


```python
%%writefile setup.py

from distutils.core import setup
from Cython.Build import cythonize
 
setup(
    name = "rectangleapp",
    ext_modules = cythonize('*.pyx')
)
```

    Overwriting setup.py



```python
!python setup.py build_ext --inplace
```

    Compiling rect.pyx because it changed.
    [1/1] Cythonizing rect.pyx
    running build_ext
    building 'rect' extension
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\87\Anaconda3\include -IC:\Users\87\Anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /EHsc /Tprect.cpp /Fobuild\temp.win-amd64-3.6\Release\rect.obj
    rect.cpp
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\87\Anaconda3\include -IC:\Users\87\Anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /EHsc /TpRectangle.cpp /Fobuild\temp.win-amd64-3.6\Release\Rectangle.obj
    Rectangle.cpp
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\87\Anaconda3\libs /LIBPATH:C:\Users\87\Anaconda3\PCbuild\amd64 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB\amd64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x64" /EXPORT:PyInit_rect build\temp.win-amd64-3.6\Release\rect.obj build\temp.win-amd64-3.6\Release\Rectangle.obj /OUT:C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\python性能优化\Cython的包装模式\rect.cp36-win_amd64.pyd /IMPLIB:build\temp.win-amd64-3.6\Release\rect.cp36-win_amd64.lib
    rect.obj : warning LNK4197: export 'PyInit_rect' specified multiple times; using first specification
       Creating library build\temp.win-amd64-3.6\Release\rect.cp36-win_amd64.lib and object build\temp.win-amd64-3.6\Release\rect.cp36-win_amd64.exp
    Generating code
    Finished generating code



```python
import rect
```


```python
pyRect = rect.PyRectangle(100, 100, 300, 500)
width, height = pyRect.get_size()
print("size: width = %d, height = %d" % (width, height))
```

    size: width = 200, height = 400



```python
pyRect.get_area()
```




    80000




```python
pyRect.do_something()
```




    0



## 外部声明

默认情况下,在模块级声明的C函数和变量对模块是本地的(即它们具有C静态存储类).它们也可以声明为extern，以指定它们在其他位置定义，例如：

```cython
cdef extern int spam_counter
 
cdef extern void order_spam(int tons)
```

Cython包装C/C++就是依赖这种外部申明

## 引用头文件

当你使用一个extern定义时，Cython在生成的C文件中包含一个声明.如果声明与其他C代码将看不到的声明不完全匹配，这可能会导致问题.例如，如果要封装现有的C库，那么生成的C代码必须与库的其余部分具有完全相同的声明.

为了实现这一点，你可以告诉Cython声明将在C头文件中找到，如下所示：

```cython
cdef extern from "spam.h":
 
    int spam_counter
 
    void order_spam(int tons)
```

引用头文件用于引入C/C++中的声明,但我们依然需要手动将其中被声明的内容用cython语法重新写一遍,这样cython才可以识别.

这个`cdef extern`代码块定义了如下三件事情：

+ 它指示Cython为生成的C代码中的命名头文件放置一个#include语句.
+ 它阻止Cython为相关块中的声明生成任何C代码
+ 它处理块中的所有声明，就像它们以cdef extern开头

重要的是要理解Cython本身不读取C头文件，所以你仍然需要提供Cython版本你要使用的声明.然而，Cython声明并不总是必须完全匹配C，在某些情况下，它们不应该或不能。尤其是：

+ 不要使用任何平台特定的C语言扩展，例如`__declspec()`
+ 如果头文件声明一个大结构，并且你只想使用几个成员，你只需要声明你感兴趣的成员.留下余下的没有任何危害，因为C编译器将使用头文件中的完整定义.

    在某些情况下，你可能不需要任何struct的成员，在这种情况下，你可以只传递在struct声明的主体，例如：

    ```cython
    cdef extern from "foo.h":
        struct spam:
            pass
    ```

    注意：你只能在一个cdef extern从块里面这样做;任何其他地方的struct声明必须是非空的。

+ 如果头文件使用`typedef`名称（如word）来引用与平台相关的数值类型的风格，则需要一个相应的`ctypedef`语句，但不需要完全匹配类型,只是使用一些正确的一般类型(int，float等).
    例如：
    ```cython
    ctypedef int word

    ```
    将工作正常无论实际大小的单词是(提供的头文件正确定义它).与Python类型(如果有)之间的转换也将用于此新类型.
    
+ 如果头文件使用宏来定义常量，则将它们转换为正常的外部变量声明。如果它们包含正常的int值，也可以将它们声明为枚举。请注意，Cython认为枚举等同于int，因此不要对非int值执行此操作.

+ 如果头文件使用宏定义了一个函数，那么声明它就像是一个普通的函数，具有适当的参数和结果类型

    如果你想包含一个C头，因为它是另一个头需要的，但不想使用它的任何声明，在extern-from块中放入pass关键字：
    ```cython
    cdef extern from "spam.h":
        pass
    ```
    如果要包括系统标题，请在引号中加上尖括号：
    ```cython
    cdef extern from "<sysheader.h>":
        ...
    ```
    如果你想包含一些外部声明，但不想指定一个头文件（因为它包含了你已经包含的其他头文件），你可以用*代替头文件名：
    ```cython
    cdef extern from *:
        ...
    ```

## 在C/C++中实现

另一种简单的写法是直接使用外部声明声明C/C++实现


```python
%%writefile spam.c

#include <stdio.h>
static int order_spam(int tons)
{
    printf("Ordered %i tons of spam!\n", tons);
    return tons;
}
```

    Overwriting spam.c



```python
%%writefile pyspam.pyx

cdef extern from "spam.c":
    int order_spam(int tons)

cpdef pyorder_spam(int tons):
    return order_spam(tons)
```

    Overwriting pyspam.pyx



```python
%%writefile setup.py

from distutils.core import setup
from Cython.Build import cythonize
 
setup(
    name = "pyspam",
    ext_modules = cythonize('pyspam.pyx')
)
```

    Overwriting setup.py



```python
!python setup.py build_ext --inplace
```

    Compiling pyspam.pyx because it changed.
    [1/1] Cythonizing pyspam.pyx
    running build_ext
    building 'pyspam' extension
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\87\Anaconda3\include -IC:\Users\87\Anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /Tcpyspam.c /Fobuild\temp.win-amd64-3.6\Release\pyspam.obj
    pyspam.c
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\87\Anaconda3\libs /LIBPATH:C:\Users\87\Anaconda3\PCbuild\amd64 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB\amd64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x64" /EXPORT:PyInit_pyspam build\temp.win-amd64-3.6\Release\pyspam.obj /OUT:C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\python性能优化\Cython的包装模式\pyspam.cp36-win_amd64.pyd /IMPLIB:build\temp.win-amd64-3.6\Release\pyspam.cp36-win_amd64.lib
    pyspam.obj : warning LNK4197: export 'PyInit_pyspam' specified multiple times; using first specification
       Creating library build\temp.win-amd64-3.6\Release\pyspam.cp36-win_amd64.lib and object build\temp.win-amd64-3.6\Release\pyspam.cp36-win_amd64.exp
    Generating code
    Finished generating code



```python
import pyspam
```


```python
pyspam.pyorder_spam(1)
```




    1



需要注意的是这种方式函数必须是`static`

## 结构，联合和枚举声明的样式

在C头文件中可以使用两种主要方法来声明结构，联合和枚举：

+ 使用标签名称
+ 使用typedef

基于这些的各种组合也存在一些变化.重要的是使Cython声明与头文件中使用的样式相匹配,以便Cython能够对其生成的代码中的类型发出正确的引用.
为了实现这一点,Cython提供了两种不同的语法来声明结构,联合或枚举类型.上面介绍的样式对应于标签名的使用.要获得另一个样式,您需要在声明前面加上`ctypedef`,如下图所示.
下表显示了可以在头文件中找到的各种可能的样式，以及应该放在`cdef extern from`块中的相应Cython声明。用结构体声明作为例子;这同样适用于联合和枚举声明.

![](source/cythonCextern.png)

## 静态成员方法

如果开头我们定义的C++类Rectangle类具有静态成员,那么如上面的做法..就像python中一样,使用`@staticmethod`装饰器装饰对应的成员方法即可

## 运算符重载

这个例子是一个vector2d,实现了加和乘.



```python
%%writefile vector2d.h

namespace algebra {
    class Vec2d {
    public:
        double x, y;
        Vec2d();
        Vec2d(double x, double y);
        ~Vec2d();
        Vec2d operator+(const Vec2d& b);
        Vec2d operator*(double k);
        
    };
}
```

    Overwriting vector2d.h



```python
%%writefile vector2d.cpp
#include "vector2d.h"

namespace algebra {

    Vec2d::Vec2d() {
        x=0;
        y=0;
    }

    Vec2d::Vec2d(double x, double y) {
        this->x = x;
        this->y = y;
    }

    Vec2d::~Vec2d() { }
    
    Vec2d Vec2d::operator+(const Vec2d& other){

        Vec2d r = Vec2d(this->x+other.x,this->y+other.y);
        return r;
    }
    Vec2d Vec2d::operator*(double k){
        Vec2d r = Vec2d(this->x*k,this->y*k);
        return r;
    }
}
```

    Overwriting vector2d.cpp



```python
%%writefile vec2d_main.cpp
#include "vector2d.h"
#include <iostream>
using algebra::Vec2d;
using std::cout;
using std::endl;
        
int main(){
    Vec2d v1 = Vec2d(2.1,2.2);
    Vec2d v2 = Vec2d(2.3,2.4);
    Vec2d v3 = v1+v2;
    cout << v3.x<<endl;
    cout << v3.y<<endl;
}
```

    Overwriting vec2d_main.cpp



```python
!g++-7 -o a.out vec2d_main.cpp vector2d.cpp 
```


```python
!./a.out
```

    4.4
    4.6



```python
%%writefile vec2d.pyx
#cython: language_level=3
# distutils: language = c++
# distutils: sources = vector2d.cpp


cdef extern from "vector2d.h" namespace "algebra":
    cdef cppclass Vec2d:
        Vec2d() except +
        Vec2d(double, double) except +
        double x, y
        Vec2d operator+(Vec2d)
        Vec2d operator*(float)

cdef class PyVec2d:
    cdef Vec2d c_vec2d      # hold a C++ instance which we're wrapping
    def __cinit__(self, float x, float y):
        self.c_vec2d = Vec2d(x, y)
    @property
    def x(self):
        return self.c_vec2d.x
    @property
    def y(self):
        return self.c_vec2d.y
    
    cpdef add(self,PyVec2d other):
        cdef Vec2d c
        c = self.c_vec2d+other.c_vec2d
        return PyVec2d(c.x,c.y)
    
    cpdef mul(self,float k):
        cdef Vec2d c
        c = self.c_vec2d*k
        return PyVec2d(c.x,c.y)
    
    def __add__(self,PyVec2d other):
        return self.add(other)
    
    def __mul__(self,float k):
        return self.mul(k)
    
```

    Overwriting vec2d.pyx



```python
%%writefile setup.py

from distutils.core import setup
from Cython.Build import cythonize
 
setup(
    name = "vec2dapp",
    ext_modules = cythonize('vec2d.pyx')
)
```

    Overwriting setup.py



```python
!python setup.py build_ext --inplace
```

    Compiling vec2d.pyx because it changed.
    [1/1] Cythonizing vec2d.pyx
    running build_ext
    building 'vec2d' extension
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\87\Anaconda3\include -IC:\Users\87\Anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /EHsc /Tpvec2d.cpp /Fobuild\temp.win-amd64-3.6\Release\vec2d.obj
    vec2d.cpp
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\87\Anaconda3\include -IC:\Users\87\Anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /EHsc /Tpvector2d.cpp /Fobuild\temp.win-amd64-3.6\Release\vector2d.obj
    vector2d.cpp
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\87\Anaconda3\libs /LIBPATH:C:\Users\87\Anaconda3\PCbuild\amd64 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB\amd64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x64" /EXPORT:PyInit_vec2d build\temp.win-amd64-3.6\Release\vec2d.obj build\temp.win-amd64-3.6\Release\vector2d.obj /OUT:C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\python性能优化\Cython的包装模式\vec2d.cp36-win_amd64.pyd /IMPLIB:build\temp.win-amd64-3.6\Release\vec2d.cp36-win_amd64.lib
    vec2d.obj : warning LNK4197: export 'PyInit_vec2d' specified multiple times; using first specification
       Creating library build\temp.win-amd64-3.6\Release\vec2d.cp36-win_amd64.lib and object build\temp.win-amd64-3.6\Release\vec2d.cp36-win_amd64.exp
    Generating code
    Finished generating code



```python
import vec2d
```


```python
v1 = vec2d.PyVec2d(2.1,2.2)
```


```python
v2 = vec2d.PyVec2d(2.3,2.4)
```


```python
(v1+v2).x
```




    4.399999618530273



## 模板

Cython使用括号语法进行模板化。下面是一个包装C ++ Vector的简单示例


```cython
%%cython
#cython: language_level=3
# distutils: language = c++
# import dereference and increment operators
from cython.operator cimport dereference as deref, preincrement as inc
 
cdef extern from "<vector>" namespace "std":
    cdef cppclass vector[T]:
        cppclass iterator:
            T operator*()
            iterator operator++()
            bint operator==(iterator)
            bint operator!=(iterator)
        vector()
        void push_back(T&)
        T& operator[](int)
        T& at(int)
        iterator begin()
        iterator end()
 
cdef vector[int] *v = new vector[int]()
cdef int i
for i in range(10):
    v.push_back(i)
 
cdef vector[int].iterator it = v.begin()
while it != v.end():
    print(deref(it))
    inc(it)
 
del v
```

    0
    1
    2
    3
    4
    5
    6
    7
    8
    9


多个模板参数可以定义为列表，如`[T，U，V]`或`[int，bool，char]`.可以通过写入`[T，U，V = *]`来指示可选的模板参数.

如果Cython需要显式引用不完整模板实例化的默认模板参数的类型,它将编写`MyClass <T，U> :: V`，所以如果类为其模板参数提供了`typedef`，那么最好在这里使用该名称.

模板函数的定义与类模板类似，模板参数列表跟随函数名称：


```cython
%%cython
# cython: language_level=3
# distutils: language = c++
cdef extern from "<algorithm>" namespace "std":
    T max[T](T a, T b)
 
print(max[long](3, 4))
print(max(1.5, 2.5))  # simple template argument deduction
```

    4
    2.5


### 使用默认构造函数简化包装

如果扩展类型使用默认构造函数(不传递任何参数)来实例化包装的C++类，则可以通过将其直接绑定到Python包装器对象的生命周期来简化生命周期处理。取代声明一个指针，我们可以声明一个实例


```cython
%%cython
#cython: language_level=3
# distutils: language = c++
from libcpp.vector cimport vector
cdef class VectorStack:
    cdef vector[int] v
 
    def push(self, x):
        self.v.push_back(x)
 
    def pop(self):
        if self.v.empty():
            raise IndexError()
        x = self.v.back()
        self.v.pop_back()
        return x
```


```python
v = VectorStack()
```


```python
v.push(10)
```


```python
v.push(120)
```


```python
v.pop()
```




    120




```python
v.pop()
```




    10



当Python对象被创建时，Cython将自动生成实例化C ++对象实例的代码，并在Python对象被垃圾回收时将其删除。

### 异常Exception处理


Cython不能抛出C++异常,或者使用try-except语句来捕获它们,但是有可能通过在声明函数时在其后加上`except +`来声明一个函数可能引发C++异常并将其转换为Python异常.例如长方体例子中的
```cython
Rectangle() except +
Rectangle(int, int, int, int) except +
```

这将将try和C++错误翻译成适当的Python异常。根据下表执行翻译（C++标识符中省略了std ::前缀）：


C++异常|	Python异常
---|---
bad_alloc	|MemoryError
bad_cast	|TypeError
bad_typeid	|TypeError
domain_error	|ValueError
invalid_argument	|ValueError
ios_base::failure	|IOError
out_of_range	|IndexError
overflow_error	|OverflowError
range_error	|ArithmeticError
underflow_error|	ArithmeticError
(all others)	|RuntimeError

如果`except +`后面加上指定的python错误类型,则会将捕获到的C++异常转化为指定的python错误

```cython
cdef int bar() except +MemoryError
```

就会指定bar()函数报错后转化为`MemoryError`


同时也可以通过实现一个函数来指定捕获的错误转化为何种python异常

```cython

cdef int raise_py_error()
cdef int something_dangerous() except +raise_py_error
```

如果有不可预知的错误代码引发了一个C++异常，那么`raise_py_error`将被调用，这允许一个人自定义`C++`到Python的错误“translations”.如果`raise_py_error`实际上并不引发一个异常，则会引发一个`RuntimeError`.
