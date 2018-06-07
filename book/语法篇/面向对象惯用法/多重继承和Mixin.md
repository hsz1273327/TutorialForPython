
# 多重继承

很多人觉得多重继承得不偿失.不支持多重继承的 Java 显然没有什么损失,C++ 对多重继承的滥用伤害了很多人,这可能还坚定了使用 Java 的决心.然而,Java的巨大成功和广泛影响,也导致很多刚接触Python的程序员没怎么见过真实的代码使用多重继承.

## 子类化内置类型很麻烦

在 Python 2.2 之前,内置类型(如`list`或`dict`)不能子类化.在Python2.2之后,内置类型可以子类化了,但是有个重要的注意事项--内置类型(使用 C 语言编写)不会调用用户定义的类覆盖的特殊方法.


```python
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)
```


```python
dd = DoppelDict(one=1)
```


```python
dd
```




    {'one': 1}




```python
dd['two'] = 2
```


```python
dd
```




    {'one': 1, 'two': [2, 2]}




```python
dd.update(three=3)
```


```python
dd
```




    {'one': 1, 'three': 3, 'two': [2, 2]}



原生类型的这种行为违背了面向对象编程的一个基本原则:始终应该从实例(self)所属的类开始搜索方法,即使在超类实现的类中调用也是如此.在这种糟糕的局面中,`__missing__`方法却能按预期方式工作,不过这只是特例.

不只实例内部的调用有这个问题(`self.get()`不调用`self.__getitem__()`),内置类型的方法调用的其他类的方法,如果被覆盖了,也不会被调用.

例子:`dict.update`方法会忽略`AnswerDict.__getitem__`方法


```python
class AnswerDict(dict):
    def __getitem__(self, key):
        return 42
```


```python
ad = AnswerDict(a='foo')  
ad['a'] 
```




    42




```python
d = {}
d.update(ad) 
d['a']
```




    'foo'




```python
d
```




    {'a': 'foo'}



直接子类化内置类型(如`dict`、`list` 或`str`)容易出错,因为内置类型的方法通常会忽略用户覆盖的方法.不要子类化内置类型,用户自己定义的类应该继承`collections`模块中的类,例如 `UserDict`、`UserList` 和 `UserString`,这些类做了特殊设计,因此 易于扩展.

如果不子类化 dict,而是子类化`collections.UserDict`,上面例子中暴露的问题便迎刃而解了


```python
import collections

class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)
```


```python
dd = DoppelDict2(one=1)
dd
```




    {'one': [1, 1]}




```python
dd['two'] = 2
dd
```




    {'one': [1, 1], 'two': [2, 2]}




```python
dd.update(three=3)
dd
```




    {'one': [1, 1], 'two': [2, 2], 'three': [3, 3]}




```python
class AnswerDict2(collections.UserDict):
    def __getitem__(self, key):
        return 42
```


```python
ad = AnswerDict2(a='foo')
ad['a']
```




    42




```python
d = {}
d.update(ad)
d['a']
```




    42




```python
d
```




    {'a': 42}



## 多重继承和方法解析顺序

任何实现多重继承的语言都要处理潜在的命名冲突,这种冲突由不相关的祖先类实现同名方法引起.这种冲突称为'菱形问题'
![菱形问题](source/dimo.PNG)


```python
class A:

    def ping(self):
        print('ping:', self)
class B(A):

    def pong(self):
        print('pong:', self)
class C(A):

    def pong(self):
        print('PONG:', self)
class D(B, C):
    def sp(self):
        return super()
    def ping(self):
        super().ping()
        print('post-ping:', self)
    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)
```


```python
d = D()
```


```python
d.sp()
```




    <super: __main__.D, <__main__.D at 0x10c8f5e48>>




```python
d.pong()# 直接调用 d.pong() 运行的是 B 类中的版本。
```

    pong: <__main__.D object at 0x10c8f5e48>



```python
C.pong(d) #超类中的方法都可以直接调用,此时要把实例作为显式参数传入
```

    PONG: <__main__.D object at 0x10c8f5e48>


Python能区分`d.pong()`调用的是哪个方法,是因为`Python`会按照特定的顺序遍历继承图.这个顺序叫方法解析顺序(Method Resolution Order,MRO).类都有一个名为`__mro__`的属性,它的值是一个元组,按照方法解析顺序列出各个超类,从当前类一直向上,直到`object`类.`D` 类的`__mro__`属性如下:


```python
D.__mro__
```




    (__main__.D, __main__.B, __main__.C, __main__.A, object)



若想把方法调用委托给超类,推荐的方式是使用内置的`super()`函数.在Python 3中,这种方式变得更容易了.然而有时可能需要绕过方法解析顺序,直接调用某个超类的方法--这样做有时更方便,例如,`D.ping`方法可以这样写:


```python
class D(B, C):
    def ping(self):
        A.ping(self) # 而不是super().ping() 
        print('post-ping:', self)

    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)
```


```python
d = D()
```


```python
d.ping()
```

    ping: <__main__.D object at 0x10c907be0>
    post-ping: <__main__.D object at 0x10c907be0>


## 使用`super()`处理父类引用

`super()`方法是python用于处理超类引用的推荐方法

+ `super(type, obj_or_type)`会按照`MRO`的順序去委託`type`的超类或兄弟类的方法來调用.光`super()`则是会指向定义类时最左边的那个超类.

下例中:

+ `super().__init__(author)`会找到`<class '__main__.Song'>`并调用其`__init__(author)`
+ `super(Song, self).__init__(name)`会找到`<class '__main__.Singer'>`並調用其 `__init__(name)`


```python
class Song(object):
    def __init__(self, author):
        self._author = author
        print("init Song")

class Singer(object):
    def __init__(self, name):
        self._name = name
        print("init Singer")

class Mtv(Song, Singer):
    def __init__(self, name, author):
        super().__init__(author) # init Song
        super(Song, self).__init__(name) # init Singer

mtv = Mtv('name', 'author')
```

    init Song
    init Singer



```python
Mtv.__mro__
```




    (__main__.Mtv, __main__.Song, __main__.Singer, object)



## Mixin

我们知道多重继承是危险的,很容易造成继承混乱,如何解决这个问题呢,就是使用mixin.原则上,应该只在使用Mixin组件制作工具时进行多重继承.


mixin是一个行为的集合,是受限制的多重继承.mixin定义的这个行为可以被加到任意class里,然而在一些情况下,使用mix-in的类,可以要求宿主满足一些协议(contract),这个协议可以是属性也可以是方法.如果有协议要求的话,协议应该是被声明在mixin内的.这样更容易复用.


Mixin是一种非常谨慎的多重继承用法,它的特点是:

+ Mixin 类是单一职责的
+ Mixin 类对宿主类一无所知
+ 不存在超类方法调用(super)以避免引入 MRO 查找顺序问题

### 例:把内存中的python对象转换为字典形式


```python
class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)
    def _traverse_dict(self,instance_dict):
        output = {}
        for key,value in instance_dict.items():
            output[key] = self._traverse(key,value)
        return output
    def _traverse(self,key,value):
        """递归的将对象转化为字典形式"""
        if isinstance(value,ToDictMixin):
            return value.to_dict()
        elif isinstance(value,dict):
            return self._traverse_dict(value)
        elif isinstance(value,list):
            return [self._traverse(key,i) for i in value]
        elif hasattr(value,'__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value
```


```python
class BinaryTree(ToDictMixin):
    def __init__(self,value,left=None,right=None):
        self.value = value
        self.left = left
        self.right = right
```


```python
tree = BinaryTree(10,
                  left=BinaryTree(7,
                                  right = BinaryTree(9)),
                  right = BinaryTree(13,
                                  left = BinaryTree(11))
                 )
```


```python
tree.to_dict()
```




    {'left': {'left': None,
      'right': {'left': None, 'right': None, 'value': 9},
      'value': 7},
     'right': {'left': {'left': None, 'right': None, 'value': 11},
      'right': None,
      'value': 13},
     'value': 10}



Mixin最大的优势是使用者可以随时安插这些功能,并且可以在必要的时候覆写他们,比如二叉树中节点也要求有指向父节点的引用,那么上面的树就会陷入死循环,解决办法是可以在其中覆写`_traverse`方法以避免这个问题.


```python
class BinaryTreeWithParent(BinaryTree):
    def __init__(self,value,left=None,right=None,parent = None):
        super().__init__(value,left=left,right=right)
        self.parent = parent
    def _traverse(self,key,value):
        if isinstance(value,BinaryTreeWithParent) and key == 'parent':
            return value.value
        else:
            return super()._traverse(key,value)
```


```python
root = BinaryTreeWithParent(10)
```


```python
root.left = BinaryTreeWithParent(7,parent = root)
```


```python
root.left.right = BinaryTreeWithParent(9,parent = root.left)
```


```python
root.to_dict()
```




    {'left': {'left': None,
      'parent': 10,
      'right': {'left': None, 'parent': 7, 'right': None, 'value': 9},
      'value': 7},
     'parent': None,
     'right': None,
     'value': 10}



并且如果其他类的某个属性也是`BinaryTreeWithParent`,那么`ToDictMixin`也会自动处理好这些属性


```python
class NamedSubTree(ToDictMixin):
    def __init__(self,name,tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent
```


```python
mytree = NamedSubTree("foobar",root.left.right)
```


```python
mytree.to_dict()
```




    {'name': 'foobar',
     'tree_with_parent': {'left': None, 'parent': 7, 'right': None, 'value': 9}}



多个Mixin之间也可以相互转化组合,例如可以编写一个这样的Mixin,可以将任意类提供通用的JSON序列化功能.我们这个Mixin要求宿主类提供`to_dict`接口.


```python
from typing import Callable,Dict
import json
class JsonMixin:
    to_dict:Callable[...,Dict]
    @classmethod
    def from_json(cls,data):
        kwargs = json.loads(data)
        return cls(**kwargs)
    def to_json(self):
        return json.dumps(self.to_dict())
        
```

有了这样的Mixin后,我们只需要极少的代码既可以通过继承体系轻松创建相关工具类.


```python
class NamedSubTree(ToDictMixin,JsonMixin):
    def __init__(self,name,tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent
```


```python
mytree = NamedSubTree("foobar",root.left.right)
```


```python
mytree.to_json()
```




    '{"name": "foobar", "tree_with_parent": {"value": 9, "left": null, "right": null, "parent": 7}}'



## 处理多重继承的原则

继承有很多用途,而多重继承增加了可选方案和复杂度.使用多重继承容易得出令人费解和脆弱的设计.我们还没有完整的理论,根据上面的内容,下面是总结的避免把类图搅乱的一些建议:

1. 把接口继承和实现继承区分开 使用多重继承时,一定要明确一开始为什么创建子类.主要原因可能有:

    + 继承接口,创建子类型,实现“是什么”关系 
    + 继承实现,通过重用避免代码重复
    
    其实这两条经常同时出现,不过只要可能,一定要明确意图.通过继承重用代码是实现细节,通常可以换用组合和委托模式.而接口继承则是框架的支柱.
      
2. 使用抽象基类显式表示接口

    现代的 Python 中,如果类的作用是定义接口,应该明确把它定义为抽象基类.Python 3.4及以上的版本中,我们要创建`abc.ABC`或其他抽象基类的子类.
    
3. 通过混入重用代码 

    如果一个类的作用是为多个不相关的子类提供方法实现,从而实现重用,但不体现"是什么"关系,应该把那个类明确地定义为混入类(mixin class).从概念上讲,混入不定义新类型,只是打包方法,便于重用.混入类绝对不能实例化,而且具体类不能只继承混入类.混入类应该提供某方面的特定行为,只实现少量关系非常紧密的方法.
    
4. 在名称中明确指明混入

    因为在Python中没有把类声明为混入的正规方式,所以强烈推荐在名称中加入`xxxMixin`后缀.
    
5. 抽象基类可以作为混入,反过来则不成立 

    抽象基类可以实现具体方法,因此也可以作为混入使用.不过,抽象基类会定义类型,而混入做不到.此外,抽象基类可以作为其他类的唯一基类,而混入决不能作为唯一的超类,除非继承另一个更具体的混入--真实的代码很少这样做.
    
    抽象基类有个局限是混入没有的:抽象基类中实现的具体方法只能与抽象基类及其超类中的方法协作.这表明,抽象基类中的具体方法只是一种便利措施,因为这些方法所做的一切,用户调用抽象基类中的其他方法也能做到.
    
6. 不要子类化多个具体类

    具体类可以没有,或最多只有一个具体超类.也就是说,具体类的超类中除了这一个具体超类之外,其余的都是抽象基类或混入.例如,在下述代码中,如果 `Alpha` 是具体类,那么 `Beta` 和 `Gamma` 必须是抽象基类或混入:

    ```python
    class MyConcreteClass(Alpha, Beta, Gamma): 
        """这是一个具体类,可以实例化。"""
        # ......更多代码......
    ```

7. 为用户提供聚合类 

    如果抽象基类或混入的组合对客户代码非常有用,那就提供一个类,使用易于理解的方式把它们结合起来.Grady Booch把这种类称为聚合类(aggregate class).
    例如,下面是 tkinter.Widget 类的完整代码:
    ```python
    class Widget(BaseWidget, Pack, Place, Grid):
        """Internal class.
        Base class for a widget which can be positioned with the
        geometry managers Pack, Place or Grid.
        """
        pass
    ```
    
8. "优先使用对象组合,而不是类继承"

    这句话引自"设计模式:可复用面向对象软件的基础"一书.
    
    熟悉继承之后,就太容易过度使用它了.出于对秩序的诉求,我们喜欢按整洁的层次结构放置物品,程序员更是乐此不疲.然而,优先使用组合能让设计更灵活.例如,对`tkinter.Widget`类来说,它可以不从全部几何管理器中继承方法,而是在小组件实例中维护一个几何管理器引用,然后通过它调用方法.毕竟小组件"不是"几何管理器,但是可以通过委托使用相关的服务.这样,我们可以放心添加新的几何管理器,不必担心会触动小组件类的层次结构,也不必担心名称冲突.即便是单继承,这个原则也能提升灵活性,因为子类化是一种紧耦合,而且较高的继承树容易倒.组合和委托可以代替混入,把行为提供给不同的类,但是不能取代接口继承去定义类型层次结构.

