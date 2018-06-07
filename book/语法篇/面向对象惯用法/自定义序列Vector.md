
# 自定义序列Vector

本篇通过自定义Vector来看如何使用组合模式实现`Vector`类,而不使用继承.既然是使用组合,那么我们首先想到的就是Mixin.

向量的分量存储在浮点数数组中,而且还将实现不可变扁平序列所需的方法.

不过,在实现序列方法之前,我们要确保`Vector`类与之前定义的`Vector2D`类兼容,除非有些地方让二者兼容没有什么意义.

## 第一版--与Vector2D兼容


```python
from array import array
from typing import Sequence,Optional,Iterator
import reprlib
from math import sqrt
class VectorBase:
    typecode:str = 'd'
    _components:Optional[array]=None
    def __init__(self, components:Sequence):
        self._components = array(self.typecode, components)
        self._dimension = None
    def __iter__(self)->Iterator:
        return iter(self._components)
    def __bool__(self)->bool:
        return bool(abs(self))
    
```


```python
class DimensionMixin:
    _components:Optional[array]=None
    _dimension:Optional[int]=None
    def __len__(self)->int:
        return len(self._components)
    @property
    def dimension(self)->int:
        if not self._dimension:
            self._dimension = len(self)
        return self._dimension
```


```python
class AbsMixin:
    def __abs__(self)->float:
        return sqrt(sum(x * x for x in self))
```


```python
from typing import Optional
from array import array
class LiteralMixin:
    _components:Optional[array]=None
    def __str__(self)->str:
        return str(tuple(self))
    def __repr__(self)->str:
        """
        如果 Vector 实例的分量超过 6 个,`repr()` 生成的字符串就会使用 ... 省略一 部分,
        包含大量元素的集合类型一定要这么做,因为字符串表示形式是用于调试的
        (因此不想让大型对象在控制台或日 志中输出几千行内容).
        使用 reprlib 模块可以生成长度有限的表示形式.
        """
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)
    def __format__(self,fmt_spec='')->str:
        return NotImplemented
```


```python
from array import array
class CodecMixin:
    typecode:str
    _components:Optional[array]
    def __bytes__(self)->bytes:
        return (bytes([ord(self.typecode)]) + bytes(self._components))
    
    @classmethod
    def frombytes(cls, octets:bytes)->'VectorBase':
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode) 
        return cls(memv)
```


```python
class Vector(VectorBase,DimensionMixin,AbsMixin, LiteralMixin,CodecMixin):
    pass
```


```python
Vector([3.1, 4.2])
```




    Vector([3.1, 4.2])




```python
Vector((3, 4, 5))
```




    Vector([3.0, 4.0, 5.0])




```python
Vector(range(10))
```




    Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])




```python
bytes(Vector(range(10)))
```




    b'd\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@\x00\x00\x00\x00\x00\x00\x14@\x00\x00\x00\x00\x00\x00\x18@\x00\x00\x00\x00\x00\x00\x1c@\x00\x00\x00\x00\x00\x00 @\x00\x00\x00\x00\x00\x00"@'




```python
Vector.frombytes(b'd\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@\x00\x00\x00\x00\x00\x00\x14@\x00\x00\x00\x00\x00\x00\x18@\x00\x00\x00\x00\x00\x00\x1c@\x00\x00\x00\x00\x00\x00 @\x00\x00\x00\x00\x00\x00"@')
```




    Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])




```python
Vector([3.1, 4.2]).dimension
```




    2



## 第二版--实现可切片的序列

实现可切片需要实现`__len__` 和`__getitem__`,我们希望切片后得到的还是Vector.实际上切片是通过`slice`实现




```python
class MySeq:
    def __getitem__(self, index):
        return index
```


```python
s = MySeq()
```


```python
s[1]
```




    1




```python
s[1:4]
```




    slice(1, 4, None)




```python
s[1:4:2]
```




    slice(1, 4, 2)




```python
s[1:4:2, 9]
```




    (slice(1, 4, 2), 9)




```python
s[1:4:2, 7:9]
```




    (slice(1, 4, 2), slice(7, 9, None))



### 切片原理

`slice`是内置的类型.它有`start`、`stop` 和`step`数据属性，以及`indices`方法.


`indices`这个方法有很大的作用,但是鲜为人知`.help(slice.indices)`给出的信息如下:

```python
S.indices(len) -> (start, stop, stride)
```

给定长度为len的序列,计算S表示的扩展切片的起始(start)和结尾(stop)索引,以及步幅(stride).超出边界的索引会被截掉,这与常规切片的处理方式一样.

换句话说,`indices`方法开放了内置序列实现的棘手逻辑,用于优雅地处理缺失索引和负数索引,以及长度超过目标序列的切片.这个方法会"整顿"元组,把start、stop 和stride都变成非负数,而且都落在指定长度序列的边界内.



```python
slice(None, 10, 2).indices(5)
```




    (0, 5, 2)




```python
slice(-3, None, None).indices(5)
```




    (2, 5, 1)




```python
from array import array
import numbers
from typing import Optional,Union
class SliceMixin:
    """需要实现`__len__`"""
    _components:array
    def __getitem__(self, index:int)->Optional[Union[VectorBase,float]]:
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))
```


```python
class Vector(VectorBase,AbsMixin,DimensionMixin, LiteralMixin,CodecMixin,SliceMixin):
    pass
```


```python
v7 = Vector(range(7))
```


```python
v7[-1]
```




    6.0




```python
v7[1:4]
```




    Vector([1.0, 2.0, 3.0])




```python
v7[-1:]
```




    Vector([6.0])




```python
v7[1,2]
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-28-0f616761b0d9> in <module>()
    ----> 1 v7[1,2]
    

    <ipython-input-22-86386b349576> in __getitem__(self, index)
         13         else:
         14             msg = '{cls.__name__} indices must be integers'
    ---> 15             raise TypeError(msg.format(cls=cls))
    

    TypeError: Vector indices must be integers


## 第三版 动态存取属性

Vector2D变成Vector之后,就没办法通过名称访问向量的分量了(如v.x 和v.y).现在我们处理的向量可能有大量分量.不过,若能通过单个字母访问前几个分量的话会比较方便.比如,用x、y和z代替v[0]、v[1] 和v[2].

我们想额外提供下述句法,用于读取向量的前四个分量:

```python
v = Vector(range(10))
v.x
>>> 0.0
v.y, v.z, v.t
>>> (1.0, 2.0, 3.0)
```

在Vector2D中,我们使用`@property`装饰器把x和y标记为只读特性.我们可以在`Vector`中编写四个特性,但这样太麻烦.特殊方法`__getattr__`提供了更好的方式.

属性查找失败后,解释器会调用`__getattr__`方法.简单来说，对`my_obj.x`表达式:

1. Python会检查my_obj实例有没有名为x的属性
2. 如果没有,到类（`my_obj.__class__`）中查找
3. 如果还没有,顺着继承树继续查找
4. 如果依旧找不到,调用my_obj所属类中定义的`__getattr__`方法,传入self 和属性名称的字符串形式(如'x')

下例中列出的是我们为`Vector`类定义的`__getattr__`方法.这个方法的作用很简单,它检查所查找的属性是不是xyzt中的某个字母


```python
from typing import Optional
class DynamicAccessMixin:
    shortcut_names = 'xyzt'
    def __getattr__(self, name:str)->Optional[float]:
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))
```


```python
class Vector(VectorBase,AbsMixin, DimensionMixin,LiteralMixin,CodecMixin,SliceMixin,DynamicAccessMixin):
    pass
```


```python
v = Vector(range(5))
v
```




    Vector([0.0, 1.0, 2.0, 3.0, 4.0])




```python
v.x
```




    0.0




```python
v.x = 10
v.x
```




    10




```python
v
```




    Vector([0.0, 1.0, 2.0, 3.0, 4.0])



可以看到,为v.x 赋值没有抛出错误但是前后矛盾.上面之所以前后矛盾是`__getattr__`的运作方式导致的:


仅当对象没有指定名称的属性时,Python才会调用那个方法,这是一种后备机制.


可是像`v.x = 10`这样赋值之后`v`对象有`x`属性了,因此使用`v.x`获取`x`属性的值时不会调用`__getattr__`方法了,解释器直接返回绑定到`v.x`上的值即10.另一方面,`__getattr__`方法的实现没有考虑到`self._components`之外的实例属性,而是从这个属性中获取`shortcut_names`中所列的"虚拟属性".

为了避免这种前后矛盾的现象,我们要改写mixin中设置属性的逻辑


多数时候,如果实现了`__getattr__`方法,那么也要定义`__setattr__`方法,以防对象的行为不一致


```python
class DynamicAccessMixin:
    shortcut_names = 'xyzt'
    def __getattr__(self, name:str)->Optional[float]:
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))
        
    def _setattr_error_handler(self,name:str)->bool:
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        return True

```


```python
class Vector(VectorBase,AbsMixin,DimensionMixin, LiteralMixin,CodecMixin,SliceMixin, DynamicAccessMixin):
    def __setattr__(self, name:str, value:float):
        self._setattr_error_handler(name)
        super().__setattr__(name, value)
```


```python
v = Vector(range(5))
v
```




    Vector([0.0, 1.0, 2.0, 3.0, 4.0])




```python
v.x
```




    0.0




```python
v.x = 10
v.x
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-39-76d34b21bf2a> in <module>()
    ----> 1 v.x = 10
          2 v.x


    <ipython-input-36-a7f3e037c51e> in __setattr__(self, name, value)
          1 class Vector(VectorBase,AbsMixin,DimensionMixin, LiteralMixin,CodecMixin,SliceMixin, DynamicAccessMixin):
          2     def __setattr__(self, name:str, value:float):
    ----> 3         self._setattr_error_handler(name)
          4         super().__setattr__(name, value)


    <ipython-input-35-682b78adde5e> in _setattr_error_handler(self, name)
         21             if error:
         22                 msg = error.format(cls_name=cls.__name__, attr_name=name)
    ---> 23                 raise AttributeError(msg)
         24         return True


    AttributeError: readonly attribute 'x'



```python
v
```




    Vector([0.0, 1.0, 2.0, 3.0, 4.0])



## Vector类第4版：散列和快速等值测试

我们要再次实现`__hash__`方法.加上现有的`__eq__`方法,这会把`Vector`实例变成可散列的对象.

我们的散列方式就是计算各个分量的散列值,然后聚合求异或



```python
from functools import reduce
from operator import xor
class HashableMixin:
    def __eq__(self, other:VectorBase)->VectorBase:
        """使用`and`运算符的截断特性和迭代器工具惰性计算特性判断是否一致,一旦有不一致就会终止后面的计算"""
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))
    def __hash__(self)->int:
        hashes = (hash(x) for x in self._components) # 
        return reduce(xor, hashes, 0)
```


```python
class Vector(VectorBase,AbsMixin, DimensionMixin,LiteralMixin,CodecMixin,SliceMixin, DynamicAccessMixin,HashableMixin):
    def __setattr__(self, name:str, value:float):
        self._setattr_error_handler(name)
        super().__setattr__(name, value)
```

## 但是还没暖点每次这这有 Vector类第5版:格式化 

Vector类的`__format__`方法与Vector2D类的相似,但是不使用极坐标,而使用超球面坐标,因为Vector类支持n个维度,而超过四维后,球体变成了"超球体".

因此,我们会把自定义的格式后缀由'p'变成'h'


```python
from math import sqrt,atan2,pi
from typing import Tuple
class HypersphereMixin:
    """需要实现`__len__`"""
    def angle(self, n:int)->float: 
        """使用["n 维球体"词条](http://en.wikipedia.org/wiki/N-sphere)中的公式计算某个角坐标"""
        r = sqrt(sum(x * x for x in self[n:]))
        a = atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return pi * 2 - a
        else:
            return a
    def angles(self)->Tuple[float]: 
        """创建生成器表达式，按需计算所有角坐标"""
        return (self.angle(n) for n in range(1, len(self)))
```


```python
from itertools import chain

class LiteralMixin:
    """需要HypersphereMixin"""
    _components:Optional[array]=None
    def __str__(self)->str:
        return str(tuple(self))
    def __repr__(self)->str:
        """
        如果 Vector 实例的分量超过 6 个,`repr()` 生成的字符串就会使用 ... 省略一 部分,
        包含大量元素的集合类型一定要这么做,因为字符串表示形式是用于调试的
        (因此不想让大型对象在控制台或日 志中输出几千行内容).
        使用 reprlib 模块可以生成长度有限的表示形式.
        """
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)
    def __format__(self,fmt_spec:str='')->str:
        if fmt_spec.endswith('h'): # 超球面坐标
            fmt_spec = fmt_spec[:-1]
            coords = chain([abs(self)],self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))
```


```python
class Vector(VectorBase, AbsMixin,DimensionMixin,CodecMixin,SliceMixin, DynamicAccessMixin,HashableMixin,HypersphereMixin,LiteralMixin):
    def __setattr__(self, name:str, value:float):
        self._setattr_error_handler(name)
        super().__setattr__(name, value)
```


```python
v = Vector(range(5))
```


```python
format(v)
```




    '(0.0, 1.0, 2.0, 3.0, 4.0)'




```python
format(Vector([2, 2, 2, 2]), '.3eh')
```




    '<4.000e+00, 1.047e+00, 9.553e-01, 7.854e-01>'



## Vector类第6版:运算符重载

向量的求反运算就是每位求反

向量的求和运算就是对应位求和.

向量的标量乘法就是每位乘以一个常数

向量点乘则是各位相乘后再相加


```python
class PositiveNegativeMixin:
    def __neg__(self)->VectorBase:
        cls = type(self)
        return cls(-x for x in self)
    def __pos__(self)->VectorBase:
        cls = type(self)
        return cls(self)
```


```python
from itertools import zip_longest
class AddMixin:
    def __add__(self, other:VectorBase)->VectorBase:
        cls = type(self)
        if isinstance(other, cls) and self.dimension == other.dimension:
            try:
                pairs = zip_longest(self, other, fillvalue=0.0)
                result = cls(a + b for a, b in pairs)
                return result
            except TypeError:
                return NotImplemented
        else:
            return NotImplemented
        
    def __radd__(self, other:VectorBase)->VectorBase:
        print("radd")
        return self + other
```


```python
import numbers
class MulMixin:
    def __mul__(self, scalar:numbers.Real)->VectorBase:
        cls = type(self)
        if isinstance(scalar, numbers.Real):
            return cls(n * scalar for n in self)
        else:
            return NotImplemented
    def __rmul__(self, scalar:numbers.Real)->VectorBase:
        return self * scalar 
```


```python
class MatmulMixin:
    def __matmul__(self, other:VectorBase)->float:
        cls = type(self)
        
        if isinstance(other,cls) and self.dimension == other.dimension:
            try:
                return sum(a * b for a, b in zip(self, other))
            except TypeError:
                return NotImplemented
        else:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other
```


```python
class CalculMixin(PositiveNegativeMixin,AddMixin,MulMixin,MatmulMixin):
    pass
```


```python
class Vector(VectorBase, AbsMixin,DimensionMixin,CodecMixin,SliceMixin,
             DynamicAccessMixin,HashableMixin,HypersphereMixin,LiteralMixin,
              CalculMixin):
    def __setattr__(self, name:str, value:float):
        self._setattr_error_handler(name)
        super().__setattr__(name, value)
```


```python
v1 = Vector([1,2,3,4,5])
v2 = Vector([1,2,3,4,5,6])
v3 = Vector([5,4,3,2,1])
n = 10
```


```python
v1+v2
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-56-d5c43dac28db> in <module>()
    ----> 1 v1+v2
    

    TypeError: unsupported operand type(s) for +: 'Vector' and 'Vector'



```python
v1+v3
```




    Vector([6.0, 6.0, 6.0, 6.0, 6.0])




```python
v1*3
```




    Vector([3.0, 6.0, 9.0, 12.0, 15.0])




```python
3*v1
```




    Vector([3.0, 6.0, 9.0, 12.0, 15.0])




```python
v1@v3
```




    35.0




```python
-v1
```




    Vector([-1.0, -2.0, -3.0, -4.0, -5.0])



## Vector类第7版:比较符号

使用`==`或者`!=`判断两个向量是否一致


```python
class EqualityMixin:
    def __eq__(self, other):
        cls = type(self)
        if isinstance(other, cls):
            return (len(self) == len(other) and all(a == b for a, b in zip(self, other)))
        else:
            return NotImplemented 
```


```python
class Vector(VectorBase, AbsMixin,DimensionMixin,CodecMixin,SliceMixin,
             DynamicAccessMixin,HashableMixin,HypersphereMixin,LiteralMixin,
              CalculMixin,EqualityMixin):
    def __setattr__(self, name:str, value:float):
        self._setattr_error_handler(name)
        super().__setattr__(name, value)
```


```python
v1 = Vector([1,2,3,4,5])
v2 = Vector([1,2,3,4,5,6])
v3 = Vector([1,2,3,4,5])
```


```python
v1==v2
```




    False




```python
v1==v3
```




    True




```python
v1 != v2
```




    True


