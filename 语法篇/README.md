
# 总章

就像九阴真经秘籍一样,总章部分讲的是python这门语言的"内功",也就是其设计哲学.python虽然现在很潮,但看现在的版本号和第三方包生态也知道其实这门语言挺古老的.回顾历史上种种编程语言,大多都是昙花一现,但最终还是被埋没在历史的长河中,能长期发展并逐渐构建出一个庞大而有活力的社区的屈指可数.一门语言能经久不衰一定会有其内在原因,而这往往与其设计哲学有相当大的关系.就像搞革命,胜利往往是思想的胜利.

# 设计哲学

每次给人安利python我都会搬出来python的设计主旨,不废话看下面


```python
import this
```

    The Zen of Python, by Tim Peters
    
    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    

python强调实用性,一致性和中庸,奉行少即是多的哲学思想.在这门编程语言的任何地方都可以看到这种设计哲学.

## 代码可读性

高质量代码有三要素--可读性,可维护性,可变更性.python设计思想非常强调可读性,很多人把它当做能运行的伪代码用.这也是为啥很多非计算机专业的人学习使用python的原因,没有难以阅读的符号,一切看起来就和英语差不多,加上缩进,天然的条理清晰容易理解.

## 胶水语言

很多人觉得python慢,但他们忽略了python是除lua外最易使用C语言扩展的胶水语言.在多数情况下python的性能足够使用,而在性能遇到瓶颈时可以找到短板将其用C重写以获得性能提升.

在计算密集型应用中python借助其良好的扩展性用哟很大的作为.
python是当今最流行的开源科学计算语言没有之一;tensorflow,pytorch等深度学习使用的高性能GPU符号计算工具都是以python作为语言平台的交互层.而blender,pg等许多软件也使用python作为其内嵌脚本语言.

在i/o密集型应用中python同样优秀.借助协程和uvloop,单进程下python服务器可以达到惊人的吞吐量和极短的响应时间.而uvloop是利用`cython`和`libuv`实现的事件循环.本质上是一个优秀的C扩展.


## 安全性

Python自然也是有局限性的,总的来说它的局限性体现在安全性上,而根源来自'用户是守规矩的'这一假设上:

+ 基于协议的语言设计让动态重载成为了可能,一旦被滥用除了影响可维护性外更加容易引起安全隐患
+ 类没有语言级别的可见度设定功能,只是人为的以成员命名规范来划分可见度,这种防君子不防小人的做法同样有安全隐患,因此可以说python的类不存在真正意义上的封装
+ Python字节码的反编译相当简单,借助一些反编译工具可以相当简单的查看到源码,甚至可以查看到运行中程序的特定变量.

因此可以说Python"不安全".但讨论一个编程语言安不安全似乎又有些傻,任何语言都不是安全的,即便是汇编写出来的程序也是可以破解反编译的.而安全更多的应该在架构层面上进行保证.当你的服务可以直接让未认证过的用户访问时你就已经败了,任何语言都是如此.
