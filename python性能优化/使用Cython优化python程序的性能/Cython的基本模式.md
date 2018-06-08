
# 使用`.pyx`改写python程序

在纯净模式中,我的代码实现手段很有限:

1. 只能直接使用python模块和对象
2. 无法使用c++的容器和算法
3. 无法使用cimport


```python
%load_ext Cython
```


```cython
%%cython
# distutils: language=c++

from libcpp.vector cimport vector
from libcpp.string cimport string
#from libc.stdio cimport printf

cpdef print_vect(string content):
    cdef vector[int] vect
    cdef int i
    for i in range(10):
        vect.push_back(i)
    for i in vect:
        #printf("%d",vect[i])
        print(vect[i])
    for i in content:
        #printf("%d",vect[i])
        print(i)
```


```python
print_vect("黑龙江".encode())
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
    -23
    -69
    -111
    -23
    -66
    -103
    -26
    -79
    -97


# Cython语法

Cython是python的超集,所以python解释器无法解释cython代码,必须编译才可以.


## 静态化参数

Cython是一个Python编译器。这意味着它可以编译普通的Python代码，而不会有任何改变（除了一些尚未支持的语言功能之外，还有一些明显的例外）.然而，对于性能关键代码，添加静态类型声明通常是有帮助的，因为它们将允许Cython退出Python代码的动态特性，并生成更简单更快的C代码.但是，必须注意的是，类型声明会使源代码更加冗长，因而可读性更低.因此，不要在没有正当理由的情况下使用它们，例如基准测试证明他们在性能关键部分真正使代码更快速地使用它们是不鼓励的.通常在正确的地方有几种类型可以走很长的路.所有C类型都可用于类型声明:整数和浮点类型，复数，结构体，联合和指针类型. Cython可以在分配类型之间自动正确地进行转换.这也包括Python的任意大小的整数类型，其中转换为C类型的值溢出会在运行时引发Python `OverflowError`.(但是，在进行算术时，不会检查是否溢出).在这种情况下，生成的C代码将正确安全地处理C类型的依赖于平台的大小.

### 在python函数中使用c语言的类型指明翻译为C语言后的参数类型

由于这些参数被传递到Python声明的函数中，它们会转换为指定的C类型值.但这只适用于数字和字符串类型


```cython
%%cython

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


```python
f(1.2)
```




    0.24



## C级别申明

作为一种动态语言，Python鼓励了一种根据方法和属性考虑类和对象的编程风格，而不仅仅局限于类层次结构中.这可以使Python成为一种非常轻松和舒适的语言，用于快速开发，但有一个代价 -- 管理数据类型的"繁文缛节"被转储到翻译器上.在运行时，解释器在搜索命名空间，获取属性和解析参数和关键字元组方面做了大量工作。与"早期绑定"语言（如C++）相比，这种运行时"后期绑定"是Python相对较慢的主要原因.然而使用Cython可以通过使用"早期绑定"编程技术获得显着的加速.

### `cdef`语句用于创建C级声明

+ 申明变量

```cython
cdef int i, j, k
cdef float f, g[42], *h
```

+ 申明结构体

```cython
cdef struct Grail:
    int age
    float volume
```

+ 申明联合体

```cython
cdef union Food:
    char *spam
    float *eggs
```

+ 申明枚举

```cython
cdef enum CheeseType:
    cheddar, edam,
    camembert
```

+ 申明函数

```cython
cdef int eggs(unsigned long l, float f):
```

`cdef`关键字指定早期绑定,默认是私有的,只有在申明时指定public才会暴露

## 类型转换

在cython中使用`<xxx>yyy`操作符来进行类型转换,其使用方式与C中类似.

```cython
cdef char *p, float *q
p = <char*>q

```

值得注意的是cython中python的`bool`类型会转化为`bint`,而python中的自定义类的实例则对应的`object`

### 类型检测

和C中类似,类型转换时使用`<xxx?>yyy`会先进行检测

## 字符串

C级别无论是字符数组还是c++的string,都只接收python的bytes作为转换来源.返回的也只会转换为bytes.因此需要注意.

## 函数,方法申明

Cython中有三种类型的函数声明.

### Python的可调用对象(def)

这种类型的函数特点:

+ 使用`def`申明
+ 可以被Python解释器调用
+ 可以被Python对象调用
+ 返回Python对象
+ 参数可以静态化

###  C的可调用对象 (cdef)

这种类型的函数特点:

+ 用`cdef`语句声明
+ 无法在python解释器中访问
+ 可以被Python对象或C值调用
+ 内部变量必须申明
+ 可以返回Python对象或C值

### Python和C的可调用(cpdef)

这种类型的函数特点:

+ 用cpdef语句声明.
+ 可以从任何地方调用
+ 当从其他Cython代码调用时,使用更快的C调用约定


### cython的内置函数


Cython将对大多数内置函数的调用编译为对相应的Python / C API例程的直接调用,使它们特别快。
只有使用这些名称的直接函数调用已优化.如果你使用这些名称中的一个假设它是一个Python对象，例如将它分配给一个Python变量，然后调用它，那么该调用将作为一个Python函数调用.

内置函数|返回类型|相当于Python/C API中的类型
---|---|---
`abs(obj)`|	object, double, ...|PyNumber_Absolute, fabs, fabsf, ...
`callable(obj)`|bint|PyObject_Callable
`delattr(obj, name)`|None|PyObject_DelAttr
`exec(code, [glob, [loc]])`|object	
`dir(obj)`|	list|PyObject_Dir
`divmod(a, b)`|	tuple|PyNumber_Divmod
`getattr(obj, name, [default])`|object|PyObject_GetAttr
`hasattr(obj, name)`|bint|PyObject_HasAttr
`hash(obj)`|int / long|PyObject_Hash
`intern(obj)`|object|`Py*_InternFromString`
`isinstance(obj, type)`|bint|PyObject_IsInstance
`issubclass(obj, type)`|bint|PyObject_IsSubclass
`iter(obj, [sentinel])`|object|PyObject_GetIter
`len(obj)`|	Py_ssize_t|PyObject_Length
`pow(x, y, [z])`|object|PyNumber_Power
`reload(obj)`|object|PyImport_ReloadModule
`repr(obj)`|object|PyObject_Repr
`setattr(obj, name)`|void|PyObject_SetAttr

## 类申明(扩展类型)

cython扩展类型可以使用`cdef class`来定义.

### 属性

其中的元素可以使用`cdef`来定义,默认是私有的,但可以使用`public`或者`readonly`关键字指定其封装形式.


```cython
%%cython
cdef class Rectangle:
    cdef public int x0
    cdef readonly int y0
    cdef int x1, y1
    def __init__(self, int x0, int y0, int x1, int y1):
        self.x0 = x0; self.y0 = y0; self.x1 = x1; self.y1 = y1
        
    cdef int _area(self):
        cdef int area
        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

    def area(self):
        return self._area()
       
def rectArea(x0, y0, x1, y1):
    rect = Rectangle(x0, y0, x1, y1)
    return rect.area()
```


```python
r = Rectangle(1, 2, 3, 1)
```


```python
r.x0
```




    1




```python
r.y0
```




    2




```python
r.x1
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-10-1a1a3632ad5d> in <module>()
    ----> 1 r.x1
    

    AttributeError: '_cython_magic_31443cea76eb5b8780ecd933e92cc406.Rec' object has no attribute 'x1'



```python
r.x0=2
r.x0
```




    2




```python
r.y0 = 4
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-12-ba0ed4f3a4a8> in <module>()
    ----> 1 r.y0 = 4
    

    AttributeError: attribute 'y0' of '_cython_magic_31443cea76eb5b8780ecd933e92cc406.Rectangle' objects is not writable



```python
r.area()
```




    1




```python
r._area()
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-14-91116c074669> in <module>()
    ----> 1 r._area()
    

    AttributeError: '_cython_magic_31443cea76eb5b8780ecd933e92cc406.Rec' object has no attribute '_area'


### 特性

cython特性除了一般python语句一样的装饰器语法外,还可以使用如下特殊定义方式,两者效果一致.

```cython
cdef class Spam:

    property cheese:

        "A doc string can go here."

        def __get__(self):
            # This is called when the property is read.
            ...

        def __set__(self, value):
            # This is called when the property is written.
            ...

        def __del__(self):
            # This is called when the property is deleted.
```

`__get__()`，`__set__()`和`__del__()`方法都是可选的.如果省略，属性访问会引发异常.


不推荐这种写法,因为看起来和python差别太大


```cython
%%cython
cdef class CheeseShop:

    cdef object cheeses

    def __cinit__(self):
        self.cheeses = []

    property cheese:   # note that this syntax is deprecated

        def __get__(self):
            return "We don't have: %s" % self.cheeses

        def __set__(self, value):
            self.cheeses.append(value)

        def __del__(self):
            del self.cheeses[:]
```


```python
shop = CheeseShop()
print(shop.cheese)

shop.cheese = "camembert"
print(shop.cheese)

shop.cheese = "cheddar"
print(shop.cheese)

del shop.cheese
print(shop.cheese)
```

    We don't have: []
    We don't have: ['camembert']
    We don't have: ['camembert', 'cheddar']
    We don't have: []


### 方法

`Rectangle`中`_area`是C级别的函数,不可被访问,所以需要使用`area`方法来封装.不过通常是使用`cpdef`直接实现的


```cython
%%cython
cdef class Rectangle:
    cdef int x0, y0
    cdef int x1, y1
    def __init__(self, int x0, int y0, int x1, int y1):
        self.x0 = x0; self.y0 = y0; self.x1 = x1; self.y1 = y1
        
    cpdef int area(self):
        cdef int area
        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

def rectArea(x0, y0, x1, y1):
    cdef Rectangle rect
    rect = Rectangle(x0, y0, x1, y1)
    return rect.area()
```


```python
r = Rectangle(1, 2, 3, 1)
```

### 方法重载

在扩展类型中同一申明方式的可以相互重载,而不同申明方式的则有一套优先级:
+ `cpdef`可以重载`cdef`,而反过来就不行
+ `def`可以重载`cpdef`,而反过来就不行


```cython
%%cython
cdef class A:
    cdef foo(self):
        print("A")
cdef class AA(A):
    cdef foo(self):
        print("AA")
    cpdef bar(self):
        self.foo()
        
        
```


```python
AA().bar()
```

    AA



```cython
%%cython
cdef class A:
    cdef foo(self):
        print("A")

cdef class B(A):
    cpdef foo(self, x=None):
        print("B", x)

class C(B):
    def foo(self, x=True, int k=3):
        print("C", x, k)
```


```python
B(12).foo()
```

    B None



```python
C().foo()
```

    C True 3


## 继承

基类的完整定义必须可用于Cython，因此如果基类是内置类型，它必须先前已声明为extern扩展类型.如果基类型在另一个Cython模块中定义，则必须声明为extern扩展类型或使用cimport语句导入.

一个扩展类型只能有一个基类(cython的扩展类不支持多重继承).但可以被python类继承,这种继承支持多继承.

有一种方法可以防止扩展类型在Python中被子类化.这是通过`final`指令完成的，通常使用装饰器在扩展类型上设置

```cython
cimport cython
 
@cython.final
cdef class Parrot:
   def done(self): pass
```

## 扩展类型快速实例化

Cython提供了两种方法来加速扩展类型的实例化.

+ 第一个是直接调用`__new__()`特殊静态方法，如从Python中所知。对于例子扩展类型Penguin，可以使用以下代码：


```cython
%%cython
cdef class Penguin:
    cdef public object food
 
    def __cinit__(self, food):
        self.food = food
 
    def __init__(self, food):
        print("eating!")
        
```


```python
normal_penguin = Penguin('fish')
```

    eating!



```python
normal_penguin.food
```




    'fish'




```python
fast_penguin = Penguin.__new__(Penguin, 'wheat') 
```


```python
fast_penguin.food
```




    'wheat'



`__new__()`实例化的对象会不运行`__init__()`只会运行`__cinit__()`

+ 第二个性能改进适用于经常在一行中创建和删除的类型，以便他们可以从freelist中受益.

    Cython为此提供了装饰器`@cython.freelist(N)`，它为给定类型创建了一个静态大小的N个实例的`freelist`.例：


```cython
%%cython
cimport cython
 
@cython.freelist(8)
cdef class Penguin:
    cdef object food
    def __cinit__(self, food):
        self.food = food
```


```python
penguin = Penguin('fish 1')
```


```python
penguin = None
penguin = Penguin('fish 2')
```

## 特殊方法

cython也支持特殊方法,它支持的特殊方法可在[这里看到](http://docs.cython.org/en/latest/src/reference/special_methods_table.html#special-methods-table)


扩展类型的特殊方法必须用`def`，而不是`cdef`声明,这不会影响他们的性能 -- Python使用不同的调用约定来调用这些特殊方法.

这边列举几个比较中要的:

### 初始化方法：`__cinit__()` 和`__init__()`

有两种方法与初始化对象有关.

+ `__cinit__()`

    方法是应该执行对象的基本C级初始化，包括对象将拥有的任何C数据结构的分配.你需要小心你在`__cinit__()`方法中做什么，因为对象可能还不是完全有效的Python对象.因此，你应该小心调用任何Python可能触摸对象的操作,特别是其方法.

    在调用`__cinit__()`方法时，已经为对象分配了内存，并且任何C属性已初始化为0或null。(任何Python属性也被初始化为None，但是你可能不应该依赖它.)你的`__cinit__()`方法一定只会被调用一次.
    
    如果扩展类型有基类，那么在调用`__cinit __()`方法之前，将自动调用基类的`__cinit__()`方法,你不能显式调用基类的`__cinit__()`方法。如果需要将修改的参数列表传递给基类,则必须在`__init__()`方法中执行初始化的相关部分(其中调用继承方法的正常规则适用).

+ `__init__()`

    在`__cinit__()`方法中不能安全完成的任何初始化都应该在`__init__()`方法中完成.当调用`__init __()`时，对象是一个完全有效的Python对象，所有操作都是安全的.在某些情况下,`__init__()`可能被多次调用或根本不被调用.

传递给构造函数的任何参数都将传递给`__cinit __()`方法和`__init__()`方法。如果你预计在Python中继承扩展类型,可能会将参数以`*和**参数`的形式传给`__cinit__()`方法，以便它可以接受和忽略额外的参数.否则，任何具有带有不同签名的`__init __()`的Python子类都必须覆盖`__new __()`以及`__init __()`，明显这样很不友好.或者，为了方便起见，如果你声明你的`__cinit__()`方法没有参数(除了`self`)，它将简单地忽略传递给构造函数的任何额外的参数.这种方式可能更加保险.

## 析构方法：`__dealloc__()`

与`__cinit__()`方法的逆向方法是`__dealloc__()`方法。`__cinit__()`方法中显式分配内存的任何C数据(例如通过malloc分配的空间)应在`__dealloc__()`方法中释放.你需要小心你在`__dealloc __()`方法中的操作.在调用`__dealloc__()`方法时，对象可能已经被部分销毁，并且对于Python而言可能不处于有效状态，如果你坚持只是释放C数据是最好的选择.

你不需要担心释放对象的Python属性，因为在`__dealloc __()`方法返回后，它将由Cython完成.
当子类化扩展类型时,请注意，超类的`__dealloc__()`方法将始终被调用，即使它被覆盖.这与典型的Python行为不同.


注意：

扩展类型没有`__del__()`方法。

## 逻辑运算方法

算术运算符方法(如`__add__()`)的行为与Python对应方法不同。这些方法没有单独的“反转”版本(`__radd __()`等).相反，如果第一个操作数不能执行操作，则调用第二个操作数的相同方法，操作数的顺序相同.


## 运算比较操作

对于不同的比较操作(`__eq__()`，`__le__()`等等)Cython没有单独的方法.而是有一个方法`__richcmp __()`，它接受一个整数，指示要执行哪种操作，如下所示:

操作|指示
---|---
<|0
==|2
>|4
<=|1
!=|3
>=|5

## 错误处理

如果你不做任何特殊的事情，用cdef声明的函数不返回任何Python对象，这样这个cdef函数就没有办法向其调用者报告其Python异常.如果在此类函数中检测到异常，则会打印一条警告消息，并忽略该异常.
如果你想要一个不返回Python对象的C函数能够将异常传播给它的调用者，你需要声明一个异常值。这里是一个例子：

```cython

cdef int spam() except -1:
    ...
```

使用此声明，每当`spam()`函数内发生异常时，它将立即返回值`-1`.此外，每当对`spam()`的调用返回`-1`时，将假定异常已经发生并将被传播.


当为函数声明异常值时，不应显式或隐式返回该值.特别是，如果异常返回值是一个`False`值，那么你应该确保函数永远不会通过隐式或空返回终止.

如果所有可能的返回值都是合法的，并且你不能完全保留一个用于信号错误，则可以使用异常值声明的替代形式：

```cython
cdef int spam() except? -1:
    ...
```

'?'号表示-1是个异常值，在这种情况下，Cython通过生成一个函数`PyErr_Occurred()`进行返回，从而知道该函数发生了异常值.


还有第三种定义方式：
```cython
cdef int spam() except *:
    ...
    
```
这种形式导致Cython在每次调用spam()后生成对`PyErr_Occurred()`的调用，而不管它返回什么值。如果你有一个函数返回void需要传播错误，你将不得不使用这种形式，因为没有任何返回值来测试.否则这种形式的定义应该尽量少用.

需要注意的是：

异常值只能为返回

+ 整数，
+ 枚举，
+ 浮点
+ 指针类型的函数声明.

并且该值必须是常量表达式。

void函数只能使用`except *`形式.

异常值规范是函数签名的一部分。如果将指针作为参数传递给函数或将其指定给变量，则声明的参数或变量的类型必须具有相同的异常值规范(或缺少).下面是一个具有异常值的指针到函数声明的示例：

```cython
int (*grail)(int, char*) except -1
```

## 模块导入

cython中的导入方式有3种:

+ python的`import`

    用于导入python模块,一般只在实现文件中导入

+ cython的`cimport`

    用于导入cpython中`.pxd`文件中申明的内容和一些cpython封装好的标准模块,可以在申明文件或者实现文件中导入

+ cython的`include`

    `include`语句用于导入`.pxi`文件.这种语法类似`C/C++`中的`#include`,是直接将目标文件内容复制到当前位置

### 使用C++的stl和C标准库

大多数C++标准库的容器已在位于`/Cython /Includes/libcpp`的pxd文件中声明.这些容器是：

+ deque 双向队列
+ list 列表
+ map 映射
+ pair 对
+ queue 队列
+ set集合
+ stack栈
+ vector 向量

这些容器的使用方法可以看C++的stl部分.

因此现在想用这些容器只需简单的cimport进来即可


```cython
%%cython
# distutils: language = c++
from libcpp.vector cimport vector
 
cdef vector[int] vect
cdef int i
for i in range(10):
    vect.push_back(i)
for i in range(10):
    print(vect[i])
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


现在在Cython中STL容器会从相应的Python内建类型中强制转换。转换通过对类型化变量（包括类型化函数参数）的赋值或显式转换触发，例如：


```cython
%%cython
# distutils: language = c++

from libcpp.string cimport string
from libcpp.vector cimport vector
 
cdef string s = b'py_bytes_object'
print(s)
cpp_string = <string> 'py_unicode_object'.encode('utf-8')
 
cdef vector[int] vect = xrange(1, 10, 2)
print(vect)              # [1, 3, 5, 7, 9]
 
cdef vector[string] cpp_strings = b'ab cd ef gh'.split()
print(cpp_strings[1])   # b'cd'
```

    b'py_bytes_object'
    [1, 3, 5, 7, 9]
    b'cd'


以下强制可用：

Python type =>|	C++ type	=>| Python type
---|---|---
bytes|	std::string|	bytes
iterable|	std::vector	|list
iterable|	std::list	|list
iterable|	std::set	|set
iterable (len 2)|	std::pair	|tuple (len 2)

所有转换都会创建一个新的容器并将数据复制到该容器中.容器中的项目会自动转换为相应的类型,包括递归转换容器内的容器,例如字符串`map`转换为`vector`.
支持在stl容器(或实际上任何类与`begin()`和`end()`方法返回支持递增,取消引用和比较的对象)通过for语法支持.包括列表解析.例如如下代码:


```cython
%%cython
# distutils: language = c++
from libcpp.vector cimport vector
cdef func(value):
    return value**2
cdef vector[int] v = [1,2,3,4,5,6,7,8]
for value in v:
    print(func(value))
y = [x*x for x in v if x % 2 == 0]
```

    1
    4
    9
    16
    25
    36
    49
    64



```python
y
```




    [4, 16, 36, 64]



## Cython中的array

Python有一个内置1维数组的原始类型的动态数组模块.可以从Cython中访问Python数组的底层C数组.同时,它们是普通的Python对象，可以存储在列表中并在多进程之间进行序列化.

与`malloc()`和`free()`的手动控制内存方法相比，这提供了对Python的安全和自动内存管理，与Numpy数组相比,无需安装依赖关系,因为数组模块内置于cPython和cython中.

### 使用内存视图的安全使用方式

注意：cython中需要同时导入cython级别的数组和常规Python数组对象引入到命名空间中.

当一个Python数组被分配给一个类型为内存视图的变量时，构造内存视图将会有一些微小的开销.但是,从这个角度来看,变量可以传递给其他函数而不需要开销,只要它被输入:


```cython
%%cython

from cpython cimport array
import array
cdef array.array a = array.array('i', [1, 2, 3])
cdef int[:] ca = a

print(ca[0])
```

    1



```cython
%%cython
from cpython cimport array
import array
cdef array.array a = array.array('i', [1, 2, 3])
cdef int[:] ca = a

cdef int overhead(object a):
    cdef int[:] ca = a
    return ca[0]

cdef int no_overhead(int[:] ca):
    return ca[0]

print(overhead(a))  # new memory view will be constructed, overhead
print(no_overhead(ca))  # ca is already a memory view, so no overhead
```

    1
    1


### 零开销，不安全访问原始C指针

为了避免任何开销，并且能够将C指针传递给其他函数，可以以底层的连续数组作为指针.没有类型或边界检查,所以要小心使用正确的类型和签名.

请注意,数组对象上的任何长度变化操作都可能使指针无效.


```cython
%%cython
from cpython cimport array
import array

cdef array.array a = array.array('i', [1, 2, 3])

# access underlying pointer:
print(a.data.as_ints[0])

from libc.string cimport memset
memset(a.data.as_voidptr, 0, len(a) * sizeof(int))
```

    1


### 克隆，扩展数组

为避免使用Python模块中的数组构造函数，可以创建与模板类型相同的新数组,并预先分配给定数量的元素.数组在请求时初始化为零.


```cython
%%cython
from cpython cimport array
import array

cdef array.array int_array_template = array.array('i', [])
cdef array.array newarray

# create an array with 3 elements with same type as template
newarray = array.clone(int_array_template, 3, zero=False)
```

一个数组也可以被扩展和调整大小;这避免了重复的内存重新分配,如果元素被逐个附加或删除,则会发生这种重新分配.


```cython
%%cython
from cpython cimport array
import array

cdef array.array a = array.array('i', [1, 2, 3])
cdef array.array b = array.array('i', [4, 5, 6])

# extend a with b, resize as needed
array.extend(a, b)
# resize a, leaving just original three elements
array.resize(a, len(a) - len(b))
```

### 相关接口

将内容强制转换
+ data.as_voidptr
+ data.as_chars
+ data.as_schars
+ data.as_uchars
+ data.as_shorts
+ data.as_ushorts
+ data.as_ints
+ data.as_uints
+ data.as_longs
+ data.as_ulongs
+ data.as_longlongs  # requires Python >=3
+ data.as_ulonglongs  # requires Python >=3
+ data.as_floats
+ data.as_doubles
+ data.as_pyunicodes

操作的相关函数

+ `int resize(array self, Py_ssize_t n) except -1`

快速调整大小/ realloc.不适合重复，小增量;将底层数组调整到正确的请求量.


+ `int resize_smart(array self, Py_ssize_t n) except -1`

小增量更加有效;使用提供摊销线性时间附加的增长模式.

+ `cdef inline array clone(array template, Py_ssize_t length, bint zero)`

给定一个模板数组，快速创建一个新数组.类型将与模板相同.如果为零,则将使用零初始化新数组.

+ `cdef inline array copy(array self)`

复制一个数组

+ `cdef inline int extend_buffer(array self, char* stuff, Py_ssize_t n) except -1`
对相同类型的新数据(例如，相同数组类型),高效附加n个元素数量的长度

+ `cdef inline int extend(array self, array other) except -1`
使用另一个数组的数据扩展数组;类型必须匹配。

+ `cdef inline void zero(array self)`
将数组内容全部置0

## Memoryviews内存视图

类型化的内存视图可以有效地访问内存缓冲区,例如NumPy数据库中的缓冲区,而不会导致任何Python开销. Memoryview类似于当前的NumPy数组缓冲区支持(np.ndarray [np.float64_t，ndim = 2]),但它们具有更多的功能和更清晰的语法.内存访问比旧的NumPy数组缓冲区支持更通用,因为它们可以处理更多种类的数组数据源.例如,他们可以处理C数组和Cython数组类型(Cython数组).可以在任何上下文(函数参数，模块级，cdef类属性等)中使用内存视图,并且可以从几乎任何通过`PEP 3118`缓冲区接口暴露可写缓冲区的对象获得.

如果习惯使用NumPy，以下示例应该让您开始使用Cython内存视图.


```cython
%%cython
from cython.view cimport array as cvarray
import numpy as np

# Memoryview on a NumPy array
narr = np.arange(27, dtype=np.dtype("i")).reshape((3, 3, 3))
cdef int [:, :, :] narr_view = narr

# Memoryview on a C array
cdef int carr[3][3][3]
cdef int [:, :, :] carr_view = carr

# Memoryview on a Cython array
cyarr = cvarray(shape=(3, 3, 3), itemsize=sizeof(int), format="i")
cdef int [:, :, :] cyarr_view = cyarr

# Show the sum of all the arrays before altering it
print("NumPy sum of the NumPy array before assignments: %s" % narr.sum())

# We can copy the values from one memoryview into another using a single
# statement, by either indexing with ... or (NumPy-style) with a colon.
carr_view[...] = narr_view
cyarr_view[:] = narr_view
# NumPy-style syntax for assigning a single value to all elements.
narr_view[:, :, :] = 3

# Just to distinguish the arrays
carr_view[0, 0, 0] = 100
cyarr_view[0, 0, 0] = 1000

# Assigning into the memoryview on the NumPy array alters the latter
print("NumPy sum of NumPy array after assignments: %s" % narr.sum())

# A function using a memoryview does not usually need the GIL
cpdef int sum3d(int[:, :, :] arr) nogil:
    cdef size_t i, j, k
    cdef int total = 0
    I = arr.shape[0]
    J = arr.shape[1]
    K = arr.shape[2]
    for i in range(I):
        for j in range(J):
            for k in range(K):
                total += arr[i, j, k]
    return total

# A function accepting a memoryview knows how to use a NumPy array,
# a C array, a Cython array...
print("Memoryview sum of NumPy array is %s" % sum3d(narr))
print("Memoryview sum of C array is %s" % sum3d(carr))
print("Memoryview sum of Cython array is %s" % sum3d(cyarr))
# ... and of course, a memoryview.
print("Memoryview sum of C memoryview is %s" % sum3d(carr_view))
```

    NumPy sum of the NumPy array before assignments: 351
    NumPy sum of NumPy array after assignments: 81
    Memoryview sum of NumPy array is 81
    Memoryview sum of C array is 451
    Memoryview sum of Cython array is 1351
    Memoryview sum of C memoryview is 451


### 基本语法

内存视图使用Python切片语法，与NumPy类似。要在一维int缓冲区上创建一个完整的视图：

+ 一维视图:

```cython
cdef int[:] view1D = exporting_object
```

+ 三维视图:


```cython
cdef int[:,:,:] view3D = exporting_object
```

+ 2D视图将缓冲区的第一维度限制为从第二个(索引1)开始的100行，然后每秒(奇数)行跳过：


```cython
cdef int[1:102:2,:] partial_view = exporting_object
```

+ 这也可以方便地作为函数参数

```cython
def process_3d_buffer(int[1:102:2,:] view not None):
    ...
```

该参数的`not None`声明自动拒绝无值作为输入,否则将允许.默认情况下允许None的原因是它方便地用于返回参数:

```cython
def process_buffer(int[:,:] input not None,
              int[:,:] output = None):
    if output is None:
        output = ...  # e.g. numpy.empty_like(input)
    # process 'input' into 'output'
    return output
```

Cython将自动拒绝不兼容的缓冲区，例如将三维缓冲区传递到需要二维缓冲区的函数将引发`ValueError`。

### 索引

在Cython中，内存视图上的索引访问将自动转换为内存地址。以下代码向其中请求一个二维内存视图的C类型的项目和索引：

```cython
cdef int[:,:] buf = exporting_object

print(buf[1,2])
```

负指数也从各自的维度结束起计算：

```cython
print(buf[-1,-2])
```

以下函数循环遍历2D数组的每个维度，并为每个项添加1：

```cython
def add_one(int[:,:] buf):
    for x in xrange(buf.shape[0]):
        for y in xrange(buf.shape[1]):
            buf[x,y] += 1
```

可以使用或不使用GIL进行索引和切片。它基本上像NumPy一样工作.如果为每个维指定了索引，您将获得基本类型的元素(例如int).否则将获得一个新的视图.省略号意味着可以为每个未指定维度获得连续的切片：

```cython
cdef int[:, :, :] my_view = exporting_object

# These are all equivalent
my_view[10]
my_view[10, :, :]
my_view[10, ...]
```

### 复制

内存视图可以复制

```cython
cdef int[:, :, :] to_view, from_view
...

# copy the elements in from_view to to_view
to_view[...] = from_view
# or
to_view[:] = from_view
# or
to_view[:, :, :] = from_view

```
它们也可以用copy（）和copy_fortran（）方法复制

### 转置

在大多数情况下内存视图可以以与NumPy切片相同的方式进行转置：

```cython
cdef int [:, :: 1] c_contig = ...

cdef int [:: 1，：] f_contig = c_contig.T
```
这一操作会给出一个新的，转置过的数据视图。调换要求存储器视图的所有维度都具有直接访问存储器布局(即，通过指针不存在任何指令).



## 内存视图与数组

这些类型对象的内存视图可以转换为Python memoryview对象(`cython.view.memoryview`).这些Python对象是可索引的，可切片的并且以与原始内存访问相同的方式进行转座。它们也可以随时转换回`Cython-space memoryviews`.

它们具有以下属性：

+ shape: size in each dimension, as a tuple.
+ strides: stride along each dimension, in bytes.
+ suboffsets
+ ndim: number of dimensions.
+ size: total number of items in the view (product of the shape).
+ itemsize: size, in bytes, of the items in the view.
+ nbytes: equal to size times itemsize.
+ base
+ T

当然还有上述的T属性（Transpose）。这些属性具有与NumPy相同的语义.例如，要检索原始对象：


```cython
%%cython

import numpy
cimport numpy as cnp

cdef cnp.int32_t[:] a = numpy.arange(10, dtype=numpy.int32)
a = a[::2]

print(a)
print(numpy.asarray(a))
print(a.base)
```

    <MemoryView of 'ndarray' object>
    [0 2 4 6 8]
    [0 1 2 3 4 5 6 7 8 9]


请注意，此示例返回从中获取视图的原始对象，同时视图已被重新生成.

每当复制Cython内存视图（使用任何copy或copy_fortran方法）时，都会获得新创建的cython.view.array对象的新内存视图.这个数组也可以手动使用,并会自动分配一个数据块.它可以随后被分配给C或Fortran连续片(或跨片).它可以像下面:

```cython
from cython cimport view

my_array = view.array(shape=(10, 2), itemsize=sizeof(int), format="i")
cdef int[:, :] my_slice = my_array
```

它还需要一个可选的参数模式（'c'或'fortran'）和一个布尔的`allocate_buffer`，它指示当超出范围时是否应该分配和释放缓冲区：

```cython
cdef view.array my_array = view.array(..., mode="fortran", allocate_buffer=False)
my_array.data = <char *> my_data_pointer

# define a function that can deallocate the data (if needed)
my_array.callback_free_data = free
```

还可以将数组的指针或C数组转换为数组：

```cython
cdef view.array my_array = <int[:10, :2]> my_data_pointer
cdef view.array my_array = <int[:, :]> my_c_array
```

当然，也可以立即将`cython.view.array`指定给类型化的内存视图切片.可以将C数组直接分配给内存视图切片：

```cython
cdef int[:, ::1] myslice = my_2d_c_array
```

数组可以像Python空间一样可索引和可切换，就像`memoryview`对象一样，并且具有与`memoryview`对象相同的属性.

`cython.view.array`的替代方法是Python标准库中的数组模块。在Python 3中，array.array类型本身支持缓冲区接口，所以在没有额外的设置的情况下，`memoryviews`就可以工作.


```cython
%%cython
cimport cpython.array

def sum_array(int[:] view):
    """
    >>> from array import array
    >>> sum_array( array('i', [1,2,3]) )
    6
    """
    cdef int total
    for i in range(view.shape[0]):
        total += view[i]
    return total
```

请注意，cimport还为阵列类型启用旧的缓冲区语法.因此,以下内容也起作用:
```cython
from cpython cimport array

def sum_array(array.array[int] arr):  # using old buffer syntax
```

## 内存控制

动态内存分配大多时候在Python中不是一个问题.一切都是一个对象,引用计数系统和垃圾收集器会在不再使用系统时自动返回内存.当涉及到更低级别的数据缓冲区时,Cython通过NumPy,内存视图或Python的stdlib数组类型,为简单类型的(多维)数组提供了特殊的支持.它们是全功能,带垃圾收集,比C中的裸指针更容易工作;同时仍然保持速度和静态类型的好处.然而,在某些情况下,这些对象仍然会产生不可接受的开销,从而可以在C中进行手动内存管理.

简单的C语言值和结构(例如局部变量cdef double x)通常分配在堆栈上并通过值传递.但是对于较大和更复杂的对象(例如动态大小的双精度列表),必须手动请求内存并发布. C为此提供了`malloc()`，`realloc()`和`free()`的功能，可以从`clibc.stdlib`导入`cython`.他们的签名是：
```cython
void* malloc(size_t size)
void* realloc(void* ptr, size_t size)
void free(void* ptr)
```

下面是一个简单的例子:


```cython
%%cython
import random
from libc.stdlib cimport malloc, free

def random_noise(int number=1):
    cdef int i
    # allocate number * sizeof(double) bytes of memory
    cdef double *my_array = <double *>malloc(number * sizeof(double))
    if not my_array:
        raise MemoryError()

    try:
        ran = random.normalvariate
        for i in range(number):
            my_array[i] = ran(0,1)

        return [ my_array[i] for i in range(number) ]
    finally:
        # return the previously allocated memory to the system
        free(my_array)
```


```python
random_noise(10)
```




    [-1.6609585787562682,
     0.2930416975778874,
     1.0867854313042287,
     0.4215754219750379,
     -0.020794290445162556,
     -0.9283056817997914,
     1.1385359763229776,
     -0.6051526240377219,
     -0.6630213916869704,
     -0.14696302042299017]



请注意，在Python堆上分配内存的C-API函数通常比上面的低级C函数更为优先,因为它们提供的内存实际上是在Python的内部存储器管理系统中解决的.它们还对较小的内存块进行了特殊优化,从而通过避免昂贵的操作系统调用来加快其分配.

C-API函数可以在`cpython.mem`标准声明文件中找到：

```cython
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
```
它们的接口和用法与相应的低级C函数的接口和用法相同.

需要记住的一个重要的事情是,使用`malloc()`或`PyMem_Malloc()`获取的内存块必须在不再使用时对其调用`free()`或`PyMem_Free()`进行手动释放(并且必须始终使用匹配类型的自由功能).否则，直到python进程退出才会被回收.这被称为内存泄漏.


如果一块内存需要比可以由`try...finally`块管理的更长的生命周期，另一个有用的习惯是将其生命周期与Python对象相结合，以利用Python运行时的内存管理，例如：


```cython
%%cython
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
cdef class SomeMemory:

    cdef double* data

    def __cinit__(self, size_t number):
        # allocate some memory (uninitialised, may contain arbitrary data)
        self.data = <double*> PyMem_Malloc(number * sizeof(double))
        if not self.data:
            raise MemoryError()

    def resize(self, size_t new_number):
        # Allocates new_number * sizeof(double) bytes,
        # preserving the current content and making a best-effort to
        # re-use the original data location.
        mem = <double*> PyMem_Realloc(self.data, new_number * sizeof(double))
        if not mem:
            raise MemoryError()
        # Only overwrite the pointer if the memory was really reallocated.
        # On error (mem is NULL), the originally memory has not been freed.
        self.data = mem

    def __dealloc__(self):
        PyMem_Free(self.data)     # no-op if self.data is NULL  
```

## 去除gil限制


Cython提供了解除和使用全局锁（GIL）的设施。当从多线程代码调用（外部C）代码可能会阻止或希望从（本地）C线程回调使用Python时，这可能很有用.显然，释放GIL应该只对线程安全的代码或使用其他防止种族条件和并发问题的保护措施的代码进行.注意，获取GIL是一个阻塞线程同步操作，因此是潜在的昂贵开销。可能不值得发布GIL进行微小的计算。通常，并行代码中的I / O操作和实质性计算将从中受益.



### 释放GIL

可以使用`nogil语句`释放GIL周围的一段代码：

```cython
with nogil:
    <code to be executed with the GIL released>
```

在语句正文中的代码不得以任何方式引发异常或操纵Python对象，并且不得先调用任何操作Python对象的操作，从而无需先重新获取GIL.例如，Cython在编译时验证这些操作，但不能查看外部C函数.它们必须被正确声明为要求或不要求GIL（见下文），以使Cython的检查生效.

### 获得GIL

要用作没有GIL执行的C代码的回调的C函数需要在操作Python对象之前获取GIL。这可以通过在函数头中指定gil来完成：

```cython
cdef void my_callback(void *data) with gil:
    ...
```

如果可以从另一个非Python线程调用回调函数，则必须首先通过调用`PyEval_InitThreads()`来初始化GIL。如果你已经在你的模块中使用`cython.parallel`，这个已经被照顾了.GIL也可以通过gil语句获得：
```cython
with gil:
    <execute this block with the GIL acquired>
```

### 声明一个可调用的不受gil限制的的函数

您可以在C函数头或函数类型中指定nogil，以声明在没有GIL的情况下可以安全地调用：

```cython
cdef void my_gil_free_func(int spam) nogil:
    ...
```

当您在Cython中实现这样的函数时，它不能有任何Python参数或Python对象返回类型.此外,涉及Python对象(包括调用Python函数)的任何操作必须首先明确获取GIL,例如:通过使用gil块或调用已经用gil定义的函数.这些限制由Cython检查,如果在nogil代码部分找到任何Python交互,您将收到编译错误.

注意nogil函数注释声明在没有GIL的情况下调用该函数是安全的.完全可以在持有GIL的同时执行它.如果调用者持有该功能,本身并不释放GIL.

用gil来声明一个函数（即获取输入的GIL）也隐含地使它的签名nogil.

## 并行编程(使用openmp)

Cython通过`cython.parallel`模块支持本机并行.要使用这种并行性,必须释放GIL（请参阅释放GIL）.它目前支持OpenMP，但后来可能会支持更多后端.

+ `cython.parallel.prange([start,] stop[, step][, nogil=False][, schedule=None[, chunksize=None]][, num_threads=None])`

    此功能可用于并行循环.OpenMP自动启动一个线程池，并根据所使用的时间表分配工作.步骤不能为0.此功能只能与GIL一起使用.如果nogil为真，则循环将包裹在nogil部分。针对变量自动推断线程位置和裁减。如果您分配给一个prange块中的变量，它将变为lastprivate，这意味着该变量将包含上一次迭代中的值。如果在一个变量上使用一个inplace操作符，那么它会减少，这意味着该变量的线程本地副本的值将随着操作符而减少，并在循环后分配给原始变量。索引变量始终为lastprivate.与块并行分配的变量将在块之后是私有的和不可用的，因为没有连续的最后一个值的概念.
    
    schedule参数会传递给OpenMP，可以是以下之一：
    + static静态的：如果提供了一个`chunksize`，迭代将在给定的`chunksize`块中提前分发给所有线程。如果没有给出`chunksize`，则迭代空间被分成大小相等的块，并且至多一个块预先分配给每个线程。当调度开销重要时，这是最合适的，并且可以将问题减少到已知具有大致相同运行时的大小相同的块.
    + dynamic动态的:迭代被分发给线程，因为它们请求它们，默认块大小为1.当每个块的运行时间不同而不是预先知道时，这是适用的，因此使用较大数量的较小块来保持所有线程忙.
    + guided有指导的:与动态调度一样,迭代被分配给线程,因为它们请求它们,但是随着块大小的减小.每个块的大小与未分配迭代次数除以参与线程数减少到1(或者提供的`chunksize`)成比例.这已超过纯动态调度的优势,事实证明,当最后一个块需要比预期或以其他方式被严重计划更多的时间,使大部分线程开始运行闲置而最后块正在只有线程数量较少的制作.
    + runtime运行时的：调度和块大小取自运行时调度变量，可以通过`openmp.omp_set_schedule()`函数调用或`OMP_SCHEDULE`环境变量进行设置.请注意,这基本上禁用了调度代码本身的任何静态编译时间优化，因此可能会显示比在编译时静态配置相同调度策略时更差的性能.

+ `cython.parallel.threadid()`

    返回线程的ID。对于n个线程，ids的范围为0到n-1

+ `cython.parallel.parallel(num_threads=None)`

    该指令可以作为with语句的一部分，并行执行代码序列.这对于设置由prange使用的线程本地缓冲区目前是有用的.一个包含的prange将是一个并行的工作共享循环，因此在并行部分中分配的任何变量对于prange也是私有的.并行块中私有的变量在并行块之后不可用.


```python
%%writefile testomp.pyx
from cython.parallel import prange
import numpy as np
cimport numpy as np

from math import exp 
from libc.math cimport exp as c_exp

def array_f(X):
    
    Y = np.zeros(X.shape)
    index = X > 0.5
    Y[index] = np.exp(X[index])

    return Y

def c_array_f(double[:] X):

    cdef int N = X.shape[0]
    cdef double[:] Y = np.zeros(N)
    cdef int i

    for i in range(N):
        if X[i] > 0.5:
            Y[i] = c_exp(X[i])
        else:
            Y[i] = 0

    return Y

def c_array_f_multi(double[:] X):

    cdef int N = X.shape[0]
    cdef double[:] Y = np.zeros(N)
    cdef int i

    for i in prange(N, nogil=True):
        if X[i] > 0.5:
            Y[i] = c_exp(X[i])
        else:
            Y[i] = 0

    return Y
```

    Overwriting testomp.pyx



```python
%%writefile setup.py

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy
ext_modules = [
    Extension(
        "testomp",
        ["testomp.pyx"],
        #extra_compile_args=['-fopenmp'],
        #extra_link_args=['-fopenmp'],
        include_dirs=[numpy.get_include()],
        extra_compile_args=['/openmp'],
        extra_link_args=['-/openmp'],
        
    )
]

setup(
    name='hello-parallel-world',
    ext_modules=cythonize(ext_modules),
)
```

    Overwriting setup.py



```python
! python setup.py build_ext --inplace
```

    Compiling testomp.pyx because it changed.
    [1/1] Cythonizing testomp.pyx
    running build_ext
    building 'testomp' extension
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\87\Anaconda3\lib\site-packages\numpy\core\include -IC:\Users\87\Anaconda3\include -IC:\Users\87\Anaconda3\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\8.1\include\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\winrt" /Tctestomp.c /Fobuild\temp.win-amd64-3.6\Release\testomp.obj /openmp
    testomp.c
    c:\users\87\anaconda3\lib\site-packages\numpy\core\include\numpy\npy_1_7_deprecated_api.h(12) : Warning Msg: Using deprecated NumPy API, disable it by #defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
    testomp.c(2411): warning C4244: '=': conversion from 'Py_ssize_t' to 'int', possible loss of data
    testomp.c(2675): warning C4244: '=': conversion from 'Py_ssize_t' to 'int', possible loss of data
    testomp.c(2660): warning C4101: '__pyx_t_10': unreferenced local variable
    testomp.c(2663): warning C4101: '__pyx_t_13': unreferenced local variable
    testomp.c(2664): warning C4101: '__pyx_t_14': unreferenced local variable
    testomp.c(2661): warning C4101: '__pyx_t_11': unreferenced local variable
    testomp.c(2662): warning C4101: '__pyx_t_12': unreferenced local variable
    testomp.c(2665): warning C4101: '__pyx_t_15': unreferenced local variable
    testomp.c(21358): warning C4244: 'initializing': conversion from 'double' to 'float', possible loss of data
    testomp.c(21364): warning C4244: 'initializing': conversion from 'double' to 'float', possible loss of data
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\87\Anaconda3\libs /LIBPATH:C:\Users\87\Anaconda3\PCbuild\amd64 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB\amd64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x64" /EXPORT:PyInit_testomp build\temp.win-amd64-3.6\Release\testomp.obj /OUT:C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\python性能优化\Cython的基本模式\testomp.cp36-win_amd64.pyd /IMPLIB:build\temp.win-amd64-3.6\Release\testomp.cp36-win_amd64.lib -/openmp
    LINK : warning LNK4044: unrecognized option '//openmp'; ignored
    testomp.obj : warning LNK4197: export 'PyInit_testomp' specified multiple times; using first specification
       Creating library build\temp.win-amd64-3.6\Release\testomp.cp36-win_amd64.lib and object build\temp.win-amd64-3.6\Release\testomp.cp36-win_amd64.exp
    Generating code
    Finished generating code


    warning: testomp.pyx:37:12: Use boundscheck(False) for faster access
    warning: testomp.pyx:38:13: Use boundscheck(False) for faster access
    warning: testomp.pyx:38:26: Use boundscheck(False) for faster access
    warning: testomp.pyx:40:13: Use boundscheck(False) for faster access



```python
from testomp import c_array_f_multi,c_array_f
```


```python
import numpy as np
```


```python
X = -1 + 2*np.random.rand(10000000)
```


```python
%timeit c_array_f_multi(X)
```

    10 loops, best of 3: 52.3 ms per loop



```python
%timeit c_array_f(X)
```

    10 loops, best of 3: 81.3 ms per loop

