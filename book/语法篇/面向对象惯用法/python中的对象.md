
# python中的对象

python中万物都是对象,构造这些对象的都是由继承自`object`的类型创建而得.而得益于python数据模型,自定义类型的行为可以像内置类型那样自然。实现如此自然的行为,靠的不是继承,而是鸭子类型(duck typing):我们只需按照预定行为实现对象所需的方法即可.

面向对象惯用法部分我们会用一个贯穿始终的例子--自定义向量,来解释python中的类与对象.这边先将这个类的最基本形式写出来



```python
from math import hypot,atan2
from array import array

class Vector2D:
    # 在 Vector2d 实例和字节序列之间转换时使用
    typecode = 'd'
    __slots__ = ('__x', '__y')
    
    @classmethod
    def frombytes(cls, octets):
        # 使用传入的`octets`字节序列创建一个 memoryview,
        # 然后使用 typecode 转换。
        # 拆包转换后的 memoryview,得到构造方法所需的一对参数。
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode) 
        return cls(*memv) 
    
    def __init__(self, x=0, y=0):
        # 把 x 和 y 转换成浮点数,尽早捕获错误,
        # 以防调用 Vector2d 函数时传入不当参数。
        self.__x = float(x)
        self.__y = float(y)
        
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    
    def __iter__(self):
        # 定义 `__iter__` 方法,把 Vector2d 实例变成可迭代的对象
        # 这样才能拆包(例如`x, y = my_vector`)
        # 这个方法的实现方式很简单,直接调用生成器表达式一个接一个产出分量.
        return (i for i in (self.x, self.y)) 
    
    def __repr__(self):
        # `__repr__` 方法使用 `{!r}` 获取各个分量的表示形式,然后插值,构成一个字符串;
        #因为Vector2d 实例是可迭代的对象,所以 `*self` 会把` x `和` y `分量提供给 `format` 函数
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)
    
    def __str__(self):
        return str(tuple(self))
    
    def __bytes__(self):
        # 为了生成字节序列,我们把 typecode 转换成字节序列,
        #然后迭代 Vector2d 实例,得到一个数组,再把数组转换成字节序列.
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))
    
    def __format__(self, fmt_spec=''):
        # 使用内置的 format 函数把 fmt_spec 应用到向量的各个分量上,构建一个可迭代的格式化字符串。
        # 再把格式化字符串代入公式 '(x, y)' 中。

        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle()) 
            outer_fmt = '<{}, {}>'
        else:
            coords = self 
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
    
    def __abs__(self):
        # 模是 x 和 y 分量构成的直角三角形的斜边长
        return hypot(self.x, self.y)
    
    def __bool__(self):
        # __bool__ 方法使用 abs(self) 计算模,然后把结果转换成布尔值,
        # 因此,0.0 是 False,非零值是 True。
        return bool(abs(self))
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return type(self)(x, y)
    def __mul__(self, scalar):
        return type(self)(self.x * scalar, self.y * scalar)
    
    def angle(self):
        return atan2(self.y, self.x)
    
    def __complex__(self):
        return complex(self.x, self.y)
```


```python
v1 = Vector2D(3, 4)
print(v1.x, v1.y)
```


```python
x, y = v1
x,y
```


```python
v1
```




    Vector2D(3.0, 4.0)




```python
v1_clone = eval(repr(v1))
v1 == v1_clone
```


```python
print(v1)
```

    (3.0, 4.0)



```python
octets = bytes(v1)
octets
```


```python
abs(v1)
```




    5.0




```python
bool(v1), bool(Vector2D(0, 0))
```




    (True, False)



## 对象表示形式 

每门面向对象的语言至少都有一种获取对象的字符串表示形式的标准方式.Python提供了两种方式.

+ `repr()`

    以便于开发者理解的方式返回对象的字符串表示形式.

+ `str()`

    以便于用户理解的方式返回对象的字符串表示形式.
    
估计你也猜到了,我们要实现接口`__repr_`和` __str__`特殊方法,为`repr()`和`str()`提供支持.

为了给对象提供其他的表示形式,还会用到另外两个特殊方法:
+ `__bytes__` 

    `__bytes__`方法与`__str__`方法类似:`bytes()`函数调用它获取对象的字节序列表示形式.

+ `__format__`

    `__format__`方法会被内置的`format()`函数和`str.format()`方法调用,使用特殊的格式代码显示对象的字符串表示形式.
    

### 格式化显示

内置的`format()`函数和`str.format()`方法把各个类型的格式化方式委托给相应的`.__format__(format_spec)`方法.`format_spec`是格式说明符,它是:

+ `format(my_obj, format_spec)`的第二个参数,或者
+ `str.format()`方法的格式字符串,{}里代换字段中冒号后面的部分


```python
brl = 1/2.43
```


```python
brl
```




    0.4115226337448559




```python
format(brl, '0.4f')
```




    '0.4115'




```python
'1 BRL = {rate:0.2f} USD'.format(rate=brl)
```




    '1 BRL = 0.41 USD'



格式规范微语言为一些内置类型提供了专用的表示代码.比如,`b`和`x`分别表示二进制和十六进制的`int`类型,`f`表示小数形式的`float`类型,而`%`表示百分数形式


```python
format(42, 'b')
```




    '101010'




```python
format(2/3, '.1%')
```




    '66.7%'



格式规范微语言是可扩展的,因为各个类可以自行决定如何解释`format_spec`参数.例如,`datetime`模块中的类,它们的 `__format__`方法使用的格式代码与`strftime()`函数一样.下面是内置的`format()`函数和`str.format()`方法的几个示例:


```python
from datetime import datetime
now = datetime.now()
format(now, '%H:%M:%S')
```




    '23:01:26'




```python
"It's now {:%I:%M %p}".format(now)
```




    "It's now 11:01 PM"



如果类没有定义`__format__`方法,从`object`继承的方法会返回`str(my_object)`我们为`Vector2D`类定义了`__str__`方法,因此可以这样做.

我们实现自己的微语言来解决这个问题.首先,假设用户提供的格式说明符是用于格式化向量中各个浮点数分量的.

要在微语言中添加一个自定义的格式代码:

如果格式说明符以'p'结尾,那么在极坐标中显示向量,即`<r, θ >`,其中`r`是模,`θ`(西塔)是弧度;其他部分('p' 之前的部分)像往常那样解释.

为自定义的格式代码选择字母时,我会避免使用其他类型用过的字母.在[格式规范微语言](https://docs.python.org/3/library/string.html#formatspec)中我们看到,

+ 整数使用的代码有`'bcdoxXn'`
+ 浮点数使用的代码有`'eEfFgGn%'`
+ 字符串使用的代码有`'s'`

因此,我为极坐标选的代码是`'p'`(polar coordinates).各个类使用自己的方式解释格式代码,在自定义的格式代码中重复使用代码字母不会出错,但是可能会让用户困惑.

对极坐标来说,我们已经定义了计算模的`__abs__`方法,因此还要定义一个简单的`angle`方法,使用`math.atan2()`函数计算角度

这样便可以增强`__format__`方法,计算极坐标.


```python
v1 = Vector2D(3, 4)
```


```python
format(v1)
```




    '(3.0, 4.0)'




```python
format(v1, '.3f')
```




    '(3.000, 4.000)'




```python
format(v1, '.3e')
```




    '(3.000e+00, 4.000e+00)'




```python
format(Vector2D(1, 1), 'p')
```




    '<1.4142135623730951, 0.7853981633974483>'




```python
format(Vector2D(1, 1), '.3ep')
```




    '<1.414e+00, 7.854e-01>'




```python
format(Vector2D(1, 1), '0.5fp')
```




    '<1.41421, 0.78540>'



## 静态方法和类方法

Python使用`classmethod`和`staticmethod`装饰器声明类方法和静态方法.学过Java面向对象编程的人可能觉得奇怪,为什么`Python`提供两个这样的装饰器,而不是只提供一个?java中只有静态方法.

先来看`classmethod`它的用法:定义操作类,而不是操作实例的方法.`classmethod`改变了调用方法的方式,因此类方法的第一个参数是类本身,而不是实例.`classmethod`最常见的用途是定义备选构造方法.

再看`staticmethod`装饰器也会改变方法的调用方式,但是第一个参数不是特殊的值.其实,静态方法就是普通的函数,只是碰巧在类的定义体中,而不是在模块层定义.

`classmethod`装饰器非常有用,但是我从未见过不得不用`staticmethod`的情况.如果想定义不需要与类交互的函数,那么在模块中定义就好了.有时,函数虽然从不处理类,但是函数的功能与类紧密相关,因此想把它放在近处.即便如此,在同一模块中的类前面或后面定义函数也就行了.


下面的例子是静态方法与类方法的对比


```python
class Demo:
    @classmethod
    def klassmeth(*args):
        return args 
    @staticmethod
    def statmeth(*args): 
        return args 
```


```python
Demo.klassmeth()
```




    (__main__.Demo,)




```python
Demo.klassmeth('spam')
```




    (__main__.Demo, 'spam')




```python
Demo.statmeth()
```




    ()




```python
Demo.statmeth('spam')
```




    ('spam',)



## 备选构造方法

我们可以把`Vector2D`实例转换成字节序列了;同理,也应该能从字节序列转换成`Vector2D`实例.

在标准库中探索一番之后,我们发现`array.array`有个类方法 `.frombytes`正好符合需求.


```python
v1 = Vector2D(3, 4)
v1
```




    Vector2D(3.0, 4.0)




```python
vb1 = bytes(v1)
vb1
```




    b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'




```python
v2 = Vector2D.frombytes(vb1)
v2
```




    Vector2D(3.0, 4.0)



## *可散列的对象*

如果对象不是可散列的,那么就不能放入集合(set)中,而要可散列必须保证3点:
+ 必须实现`__hash__`方法
+ 必须实现`__eq__` 方法
+ 要让向量不可变

## `*`使用`特性`让对象的分量只读

`property`装饰器可以把读值方法标记为特性.

我们让这些向量不可变是有原因的,因为这样才能实现`__hash__`方法.这个方法应该返回一个整数,理想情况下还要考虑对象属性的散列值(`__eq__`方法也要使用),因为相等的对象应该具有相同的散列值.`Vector2d.__hash__`方法的代码十分简单--使用位运算符异或(`^`)混合各分量的散列值.

要想创建可散列的类型,不一定要实现特性,也不一定要保护实例属性.只需正确地实现 `__hash__` 和 `__eq__` 方法即可.但是,实例的散列值绝不应该变化,因此我们借机提到了只读特性.

## Python的私有属性和"受保护的"属性

Python不能像`Java`那样使用`private`修饰符创建私有属性,但是`Python`有个简单的机制,能避免子类意外覆盖"私有"属性.

举个例子:有人编写了一个名为`Dog`的类,这个类的内部用到了`mood`实例属性,但是没有将其开放.现在,你创建了`Dog`类的子类:`Beagle`.如果你在毫不知情的情况下又创建了名为`mood`的实例属性,那么在继承的方法中就会把`Dog`类的`mood`属性覆盖掉.这是个难以调试的问题.

为了避免这种情况,如果以`__mood`的形式(两个前导下划线,尾部没有或最多有一个下划线)命名实例属性,Python会把属性名存入实例的`__dict__`属性中,而且会在前面加上一个下划线和类名.因此,对`Dog`类来说,`__mood`会变成`_Dog__mood`;对`Beagle`类来说,会变成`_Beagle__mood`.这个语言特性叫名称改写(name mangling).

名称改写是一种安全措施,不能保证万无一失:它的目的是避免意外访问,不能防止故意做错事,只要知道改写私有属性名的机制,任何人都能直接读取私有属性——这对调试和序列化倒是有用.此外,只要编写`v1._Vector__x = 7`这样的代码,就能轻松地为 Vector2D实例的私有分量直接赋值.如果真在生产环境中这么做了,出问题时可别抱怨.

不是所有Python程序员都喜欢名称改写功能,也不是所有人都喜欢 `self.__x` 这种不对称的名称。有些人不喜欢这种句法,他们约定使用一个下划线前缀编写"受保护"的属性(如`self._x`)。批评使用两个下划线这种改写机制的人认为,应该使用命名约定来避免意外覆盖属性.Ian Bicking有一句话,那句话的完整表述如下:

>绝对不要使用两个前导下划线,这是很烦人的自私行为.如果担心名称冲突,应该明确使用一种名称改写方式(如 `_MyThing_blahblah`).这其实与使用双下划线一样,不过自己定的规则比双下划线易于理解.
    
Python解释器不会对使用单个下划线的属性名做特殊处理,不过这是很多 Python 程序员严格遵守的约定,他们不会在类外部访问这种属性.遵守使用一个下划线标记对象的私有属性很容易,就像遵守使用全大写字母编写常量那样容易.

Python文档的某些角落把使用一个下划线前缀标记的属性称为"受保护的"属性.使用`self._x`这种形式保护属性的做法很常见,但是很少有人把这种属性叫作"受保护的"属性.有些人甚至将其称为"私有"属性.

总之,Vector2D的分量都是"私有的",而且Vector2D实例都是"不可变的".我用了两对引号,这是因为并不能真正实现私有和不可变.

## 使用`__slots__`类属性节省空间

默认情况下,Python在各个实例中名为`__dict__`的字典里存储实例属性.为了使用底层的散列表提升访问速度,字典会消耗大量内存.如果要处理数百万个属性不多的实例,通过`__slots__`类属性,能节省大量内存,方法是让解释器在元组中存储实例 属性,而不用字典.

继承自超类的`__slots__`属性没有效果.Python只会使用各个类中定义的`__slots__`属性.

定义`__slots__`的方式是,创建一个类属性,使用`__slots__`这个名字,并把它的值设为一个字符串构成的可迭代对象,其中各个元素表示各个实例属性.我喜欢使用元组,因为这样定义的`__slots__`中所含的信息不会变化.

在类中定义`__slots__`属性的目的是告诉解释器:"这个类中的所有实例属性都在这儿了!"这样,Python会在各个实例中使用类似元组的结构存储实例变量,从而避免使用消耗内存的`__dict__`属性.如果有数百万个实例同时活动,这样做能节省大量内存.

在类中定义`__slots__`属性之后,实例不能再有`__slots__`中所列名称之外的其他属性.这只是一个副作用,不是`__slots__`存在的真正原因.不要使用`__slots__`属性禁止类的用户新增实例属性.`__slots__`是用于优化的,不是为了约束程序员.

然而,"节省的内存也可能被再次吃掉":如果把`__dict__`这个名称添加到`__slots__`中,实例会在元组中保存各个实例的属性,此外还支持动态创建属性,这些属性存储在常规的`__dict__`中.当然,把 `__dict__` 添加到`__slots__`中可能完全违背了初衷,这取决于各个实例的静态属性和动态属性的数量及其用法.粗心的优化甚至比提早优化还糟糕.

此外,还有一个实例属性可能需要注意,即`__weakref__`属性,为了让对象支持弱引用,必须有这个属性.用户定义的类中默认就有`__weakref__`属性.可是,如果类中定义了`__slots__`属性,而且想把实例作为弱引用的目标,那么要把 `__weakref__`添加到`__slots__`中.

综上,`__slots__`属性有些需要注意的地方,而且不能滥用,不能使用它限制用户能赋值的属性.处理列表数据时`__slots__`属性最有用,例如模式固定的数据库记录,以及特大型数据集.

### `__slots__`的问题

总之,如果使用得当,`__slots__`能显著节省内存,不过有几点要注意.

+ 每个子类都要定义 `__slots__` 属性,因为解释器会忽略继承的`__slots__`属性。
+ 实例只能拥有 `__slots__` 中列出的属性,除非把 `__dict__` 加入 `__slots__`中(这样做就失去了节省内存的功效).
+ 如果不把 `__weakref__` 加入 `__slots__`,实例就不能作为弱引用的目标.

如果你的程序不用处理数百万个实例,或许不值得费劲去创建不寻常的类,那就禁止它创 建动态属性或者不支持弱引用.与其他优化措施一样,仅当权衡当下的需求并仔细搜集资料后证明确实有必要时,才应该使用`__slots__`属性.


### 覆盖类属性

Python有个很独特的特性:类属性可用于为实例属性提供默认值.Vector2D中有个`typecode`类属性,`__bytes__`方法两次用到了它,而且都故意使用`self.typecode`读取它的值.因为`Vector2D`实例本身没有`typecode`属性,所以`self.typecode`默认获取的是`Vector2D.typecode`类属性的值.

但是,如果为不存在的实例属性赋值,会新建实例属性.假如我们为`typecode`实例属性赋值,那么同名类属性不受影响.然而,自此之后,实例读取的`self.typecode`是实例属性`typecode`,也就是把同名类属性遮盖了.借助这一特性,可以为各个实例的`typecode`属性定制不同的值.


`Vector2D.typecode`属性的默认值是`'d'`,即转换成字节序列时使用8字节双精度浮点数表示向量的各个分量.如果在转换之前把Vector2D实例的`typecode`属性设为`'f'`,那么使用4字节单精度浮点数表示各个分量.

现在你应该知道为什么要在得到的字节序列前面加上`typecode`的值了:为了支持不同的格式.如果想修改类属性的值,必须直接在类上修改,不能通过实例修改.如果想修改所有实例(没有`typecode`实例变量)的`typecode`属性的默认值,可以这么做: 

```python
Vector2d.typecode = 'f'
```

然而,有种修改方法更符合Python风格,而且效果持久,也更有针对性.类属性是公开的,因此会被子类继承,于是经常会创建一个子类,只用于定制类的数据属性.


```python
v11 = Vector2D(3, 4)
```


```python
v11.x, v11.y
```




    (3.0, 4.0)




```python
v11.x = 123
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-39-18bccdc40952> in <module>()
    ----> 1 v11.x = 123
    

    AttributeError: can't set attribute



```python
v22 = Vector2D(3.1, 4.2)
```


```python
hash(v11), hash(v22)
```




    (7, 384307168202284039)




```python
len(set([v11, v22]))
```




    2



## 用于构建,解构,反射对象的工具

### `__new__`构造运算符

也就是面向对象编程中常提到的构造方法了

这是一旦被调用就会执行的运算符,也是正常情况下一个实例第一个执行的运算符.该方法会返回一个对应对象的实例.我们来看看他的特性.

例: 建立一个可以记录调用次数的类


```python
class Count_new:
    counter = 0
    def __new__(cls):
        cls.counter += 1
        print(cls.counter," times has been called. ")
        return super(Count_new,cls).__new__(cls)
```


```python
Count_new()#没有指定变量也会返回一个对象
```

    1  times has been called. 





    <__main__.Count_new at 0x10f120828>




```python
a = Count_new()
```

    2  times has been called. 


### `__init__`实例初始化

最常见的运算符重载应用就是`__init__`方法了,即实例初始化方法.该方法无返回值.

这个方法我们在将继承的时候就有过接触,所以不多说,主要看看他和`__new__`的关系.

`__new__`运算符返回的是一个对象,这个对象就是类对象


```python
class Count_new_init:
    counter = 0
    def __new__(cls):
        cls.counter += 1
        print(cls.counter," times has been called. ")
        return object.__new__(cls)
    def __init__(self):
        self.name = self.counter<<2
        print("My name is ",self.name," , you've Created me!")
```


```python
Count_new_init()
```

    1  times has been called. 
    My name is  4  , you've Created me!





    <__main__.Count_new_init at 0x10f1ed6a0>




```python
a = Count_new_init()
```

    2  times has been called. 
    My name is  8  , you've Created me!



```python
b = Count_new_init()
```

    3  times has been called. 
    My name is  12  , you've Created me!



```python
c = b.__new__(Count_new_init)
```

    4  times has been called. 



```python
d = c.__init__()
```

    My name is  16  , you've Created me!



```python
e = a.__new__(Count_new_init)
```

    5  times has been called. 


### `__del__`析构运算符

析构运算符`__del__`定义当对象实例被删除或者释放时的操作,继续修改那个例子


```python
class Count_new_init__del(object):
    counter = 0
    def __new__(cls):
        cls.counter += 1
        print(cls.counter," times has been called. ")
        return super(Count_new_init__del,cls).__new__(cls)
    def __init__(self):
        self.name = self.counter<<2
        print("My name is ",self.name," , you've Created me!")

    def __del__(self):
        print("I'm ",self.name,", I'll leave now!")
```


```python
c = Count_new_init__del()
```

    1  times has been called. 
    My name is  4  , you've Created me!



```python
c = 1
```

    I'm  4 , I'll leave now!



```python
d = Count_new_init__del()
```

    2  times has been called. 
    My name is  8  , you've Created me!



```python
del d
```

    I'm  8 , I'll leave now!


### `__dir__()`反射实现的所有属性,包括特殊方法


```python
v11.__dir__()
```




    ['__module__',
     'typecode',
     '__slots__',
     'frombytes',
     '__init__',
     'x',
     'y',
     '__iter__',
     '__repr__',
     '__str__',
     '__bytes__',
     '__format__',
     '__eq__',
     '__hash__',
     '__abs__',
     '__bool__',
     '__add__',
     '__mul__',
     'angle',
     '__complex__',
     '_Vector2D__x',
     '_Vector2D__y',
     '__doc__',
     '__getattribute__',
     '__setattr__',
     '__delattr__',
     '__lt__',
     '__le__',
     '__ne__',
     '__gt__',
     '__ge__',
     '__new__',
     '__reduce_ex__',
     '__reduce__',
     '__subclasshook__',
     '__init_subclass__',
     '__sizeof__',
     '__dir__',
     '__class__']



### `__class__`反射对象所属的类


```python
v11.__class__
```




    __main__.Vector2D



### `__sizeof__()`反射对象所占的内存空间


```python
v11.__sizeof__()
```




    32



## 类作为对象

python中类也是对象,Python数据模型为每个类定义了很多属性.

+ `cls.__class__`

    构造类对象的对象(元类)

+ `cls.__bases__`

    由类的基类组成的元组.
    
+ `cls.__qualname__`和`cls.__name__`

    Python 3.3新引入的属性,其值是类或函数的限定名称,即从模块的全局作用域到类的点分路径.内部类`ClassTwo`的 `__qualname__` 属性,其值是字符串'ClassOne.ClassTwo',而`__name__`属性的值是`'ClassTwo'`.
    
+ `cls.__subclasses__()`

    这个方法返回一个列表,包含类的直接子类.这个方法的实现使用弱引用,防止在超类和子类(子类在`__bases__`属性中储存指向超类的强引用)之间出现循环引用.这个方法返回的列表中是内存里现存的子类.

+ `cls.__mro__`

    记录类的继承顺序
    
+ `cls.mro()`

    构建类时,如果需要获取储存在类属性`__mro__` 中的超类元组,解释器会调用这个方法.元类可以覆盖这个方法,定制要构建的类解析方法的顺序.
