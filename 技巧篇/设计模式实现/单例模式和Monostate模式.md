# 单例模式


假设这边有这样一个场景:

我们要描述一个现代家庭(丈夫,妻子,孩子),那就就应该是不管怎么样都只有一个丈夫,一个妻子,但是孩子可以数量不定.因此丈夫这个类型在这个系统中就是特指,妻子也是特指,而孩子就是泛指所有的孩子.

使用面向对象的思想来看,丈夫妻子都既是类,又各特指一个固定的实例.因此应该是单例模式,而孩子是一个类型,是泛指一类对象.


单例模式实际上可以类比全局变量,只是全局变量对应的是变量,而单例模式则是全局类特指固定的实例.


说道底什么是单例模式呢?

**确保类有且只有一个特定类型的对象,并提供全局的访问点.**

可以看出单例模式是一个面向对象编程范式的扩展,它必须完全依托于面向对象编程.

最常见的单例模式应用场景像日志记录,数据库操作,打印机后台,全局累加器等.



## 实现思路

单例模式无非是想让每次调用类的构造函数时返回的是一个统一的实例.因此python来实现的思路就是:

1. 找个地方存放类和实例的映射
2. 修改类的构造过程,使每次构造过程都返回固定的实例

## 使用元类构造单例

我们知道元类可以构造类.只要重载其`__call__`方法即可.因此可以使用如下的元类来构建


```python
singleton_instances={}

class SingletonMeta(type):    
    def __call__(cls,*args,**kwargs):
        if cls not in singleton_instances:
            singleton_instances[cls] = super().__call__(*args,**kwargs)
        return singleton_instances[cls]
    
class SingletonAbc(metaclass = SingletonMeta):
    pass

class C_Mixin:
    def func(self):
        print(f"a:{self.a};b:{self.b}")
        
        
class B(C_Mixin,SingletonAbc):
    def __init__(self,a,b):
        self.a = a
        self.b = b
        
class C(B):
    pass
```


```python
b = B(1,2)
b.func()
```

    a:1;b:2



```python
bb = B(11,22)
bb.func()
```

    a:1;b:2



```python
c = C(2,3)
c.func()
```

    a:2;b:3



```python
c = C(22,33)
c.func()
```

    a:2;b:3



```python
singleton_instances
```




    {__main__.B: <__main__.B at 0x10ccd04a8>,
     __main__.C: <__main__.C at 0x10ccd03c8>}



## 覆写`__new__`方法构建单例

我们知道`__neww__`方法可以定义实例化的的行为,因此也可以通过这种方式来构建单例


```python
class AA:
    def __new__(cls,*args,**kwargs):
        print(__name__+"."+cls.__name__)
        if not singleton_instances.get(cls):
            try:
                temp = super(AA,cls).__new__(cls,*args,**kwargs)
            except TypeError as te:
                temp = object.__new__(cls)
            except Exception as e:
                raise e
            finally:
                singleton_instances[cls]=temp
        return singleton_instances[cls]
    
    def __init__(self,a,b):
        self.a=a
        self.b=b
        
    def func(self):
        print(f"a:{self.a};b:{self.b}")
```


```python
aa = AA(1,2)
```

    __main__.AA



```python
aa.func()
```

    a:13;b:22



```python
aaaa = AA(11,22)
aaaa.func()
```

    a:11;b:22



```python
aaaa.func()
```

    a:13;b:22



```python
aa.a = 13
```


```python
aaaa.a
```




    13




```python
list(singleton_instances.keys())[-1] == list(singleton_instances.keys())[-2]
```




    False




```python
list(singleton_instances.keys())[-1]
```




    __main__.AA




```python
list(singleton_instances.keys())[-2]
```




    __main__.AA




```python

```

## 使用模块代替单例模式

python中由于`import`的机制问题,导入模块这个行为本身就只会执行一次,再加上模块在python中也是对象,因此不在意形式上不统一的问题的话,我们完全可以把模块作为单例模式中的类来使用.

这种方案总结如下:

优点|缺点
---|---
完全原生,不用额外的代码|无法继承;无法扩展,不能定义`__call__`这样的魔术方法;没有初始化操作




```python

```
