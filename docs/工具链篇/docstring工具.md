
# docstring工具

python是一门高度自省的编程语言,每个对象都有一个`__doc__`字段用于保存一段自我描述的文本.这个文本可以

+ 被`help()`内置函数截获;
+ 被标准库`pydoc`读出生成注释文档;
+ 如果其中包含doctest语法的话也可以被doctest解析用于做测试

在每个模块/类/函数的定义过程中,定义体内的第一行最开头开始如果使用3个引号(`"""`或者`'''`)的形式来构建一个字符串段,那么它就会被赋值给这个对象的`__doc__`字段,也就是这段字符串就是这个对象的docstring.

## docstrings注释风格

我们的docstrings注释要简洁明了,并且最好符合大多数人的阅读习惯,这样才便于维护,这边推荐谷歌风格的注释规范.

如果使用vscode的话,有一个插件autoDocstring可以非常简单的创建符合各种风格的docstring模板,只需要在config中设置下`"autoDocstring.docstringFormat": "google",`即可.


### 模块docstrings

Python中有模块概念,可以简单的理解为每个文件都是一个模块,而每个文件夹也都是模块.只是文件夹模块的导入文件为其中的`__init__.py`文件.
通常模块也是要有docstring注释,用于在多人协作时记录一些元信息.
这些元信息包括:

+ 模块简单说明
+ Version 模块的版本
+ Author 模块的作者
+ Email 模块作者的邮箱
+ Copyright 模块的版权,包括日期和作者
+ License 模块的许可证样板
+ History 模块的跟新历史

我们来看一个例子:

```
"""定义一些标准错误和一些方法.

+ File: error.py
+ Version: 0.5
+ Author: hsz
+ Email: hsz1273327@gmail.com
+ Copyright: 2018-02-08 hsz
+ License: MIT
+ History

    + 2018-01-23 created by hsz
    + 2018-01-23 version-0.5 by hsz
"""
```

每个文件应该包含一个许可证样板. 根据项目[使用的许可](http://blog.hszofficial.site/blog/2016/06/11/%E5%85%B3%E4%BA%8E%E5%BC%80%E6%BA%90%E5%8D%8F%E8%AE%AE%E7%9A%84%E9%80%89%E6%8B%A9/), 选择合适的样板.



### 函数docstrings

一个函数必须要有文档字符串, 除非它满足以下条件:

+ 外部不可见
+ 非常短小
+ 命名简单明了

文档字符串应该包含函数做什么, 以及输入和输出的详细描述. 通常, 不应该描述”怎么做”, 除非是一些复杂的算法. 文档字符串应该提供足够的信息, 当别人编写代码调用该函数时, 他不需要看一行代码, 只要看文档字符串就可以了. 对于复杂的代码, 在代码旁边加注释会比使用文档字符串更有意义.

关于函数的几个方面应该在特定的小节中进行描述记录， 这几个方面如下文所述. 每节应该以一个标题行开始. 标题行以冒号结尾. 除标题行外, 节的其他内容应被缩进2个空格.


+ Args:
    列出每个参数的名字, 并在名字后使用一个冒号和一个空格, 分隔对该参数的描述.如果描述太长超过了单行80字符,使用2或者4个空格的悬挂缩进(与文件其他部分保持一致). 描述应该包括所需的类型和含义. 如果一个函数接受`*foo`(可变长度参数列表)或者`**bar` (任意关键字参数), 应该详细列出`*foo和**bar`.
+ Returns: (或者 Yields: 用于生成器)
    描述返回值的类型和语义. 如果函数返回None, 这一部分可以省略.
+ Raises:
    列出与接口有关的所有异常.
    
我们看一个例子:

```python
def flatten(items):
    """压扁序列,将多层结构的序列压为一列.

    
    Args:
        items (Iterable): 复杂的多层序列
    Returns:
        Iterable: 压扁后的单层序列
    """
    for item in items:
        is_iterable = isinstance(item, Iterable)
        is_string_or_bytes = isinstance(item, (str, bytes, bytearray))
        if is_iterable and not is_string_or_bytes:
            for i in flatten(item):
                yield i
        else:
            yield item

```
    
### 类docstrings

类应该在其定义下有一个用于描述该类的文档字符串. 如果你的类有公共属性(Attributes), 那么文档中应该有一个属性(Attributes)段. 并且应该遵守和函数参数相同的格式.

+ Attributes:
    成员属性
    
我们看一个例子:

```python
class SampleClass(object):
    """一个简单的类例子

    Attributes:
        likes_spam: 布尔型参数
        eggs: int型参数
    """

    def __init__(self, likes_spam=False):
        """Inits SampleClass with blah."""
        self.likes_spam = likes_spam
        self.eggs = 0

    def public_method(self):
        """Performs operation blah."""
        
```

## 文档生成

无论代码写的如何,如果没有一个详细清晰的文档会让使用和维护变得非常困难,负责任的开发者应该尽量为自己的代码维护一份文档.python可以使用自带的文档生成器`pydoc`,它可以读取代码中的`docstring`,自动的生成文档.

它的使用方式非常简单

```shell
!python -m pydoc <packagename>
```

+ -k 查找关键字
+ -p 用localhost打开网页版,后面填端口号
+ -g GUI版
+ -w 生成html文件

### `*`sphinx-autodoc

pydoc虽然方便,但实话说样式比较老旧,而且可定制性不强,现在的python包一般都用sphinx做文档,sphinx其实也是利用autodoc,结合docstring和规范化的文档格式,可以实现非常美观的项目文档.具体可以看[我的这篇博文](http://blog.hszofficial.site/blog/2016/11/29/%E4%BD%BF%E7%94%A8sphinx%E7%BB%93%E5%90%88markdown%E5%86%99%E9%A1%B9%E7%9B%AE%E6%96%87%E6%A1%A3/)
