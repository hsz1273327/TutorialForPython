# 命令行工具

计算机最基础的应用就是命令行工具了,众所周知的linux便是因为拥有shell和一众方便好用的命令行工具而备受程序员和geek喜欢.

这种交互方式优缺点都很显而易见,因此喜欢的人非常喜欢,不喜欢的人非常不喜欢.

## 优点

+ 功能简单单一,使用灵活
    一般命令行工具都是很小巧简单,专注只做一件事
+ 形式统一,对开发人员更友好
    命令行工具只接收固定的参数运作,以一问一答的形式或者指派开始进程,指派结束进程的方式与人交互,几乎可以说没有太多的交互可言,因此便于开发
+ 便于自动化
    可以通过脚本将多个工具串联实现复杂功能

## 缺点

+ 交互不友好
    命令行工具几乎没有交互可言,因此看起来比较丑陋而且不连贯

+ 选择困难
    对于一般不熟悉的用户,众多的工具会让人无从下手

+ 跨平台学习成本高
    linux,windows都有各自的系统接口和语言环境,他们往往并不通用,因此工具可移植性比较差,不同平台要记不同的命令增加了学习成本.


## 使用脚本语言编写命令行工具

静态语言编写命令行工具虽然便于分发,但写起来太过费事因此往往不是快速开发最好的选择
现在的很多工具都是用脚本语言写的,为了让脚本语言写的工具用起来像静态语言编写的那样,不用声明使用的是什么解释器,
在unix和它的衍生平台上,我们常在脚本开头写上比如:

```python
#!/usr/bin/env python
```

这样的标识,这叫[Shebang (Unix)](https://zh.wikipedia.org/wiki/Shebang),
之后再使用`chmod +x <name>`为全局赋予执行权限,或者使用`chmod u+x <name>`为当前用户提供执行权限.

而在windows上,我们可以通过后缀选择运行的工具.


# 使用python编写命令行工具

python的简易语法和很多很"魔法"的语言工具,非常适合编写命令行工具.其标准库就已经提供了足够好用的命令行参数解析工具,而社区很多有才的开发者又设计了许多对开发人员更加友好的同类工具,本文将对几个典型的工具做说明.

## 标准库中的命令行解析工具(argparse)

python标准库中的argparse模块是官方推荐的命令行工具.它可以解析命令行参数,可以生成次级菜单等

### 基本命令

argparse模块的命令可以归结为就3条

#### ArgumentParser

创建命令行解析对象,其完整签名为:

```python
parser = argparse.ArgumentParser(prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=argparse.HelpFormatter, prefix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True)
```

其中的参数:
+ `prog`,程序的名字(默认:`sys.argv[0]`)
+ `usage`,描述程序用法的字符串(默认:从解析器的参数生成)
+ `description`,参数帮助信息之前的文本(默认:`None`)
+ `epilog`, 参数帮助信息之后的文本(默认:`None`)
+ `parents`,`ArgumentParser`对象的一个列表,这些对象的参数应该包括进去像有时候需要解析非常复杂的关键字参数,比如像git那样的复杂命令行工具,例子如下:



```python
import argparse
```


```python
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('--parent', type=int)

foo_parser = argparse.ArgumentParser(parents=[parent_parser])
foo_parser.add_argument('foo')
foo_parser.parse_args(['--parent', '2', 'XXX'])

```




    Namespace(parent=2, foo='XXX')




```python
bar_parser = argparse.ArgumentParser(parents=[parent_parser])
bar_parser.add_argument('--bar')
bar_parser.parse_args(['--bar', 'YYY'])

```




    Namespace(parent=None, bar='YYY')



+ `formatter_class`,定制化帮助信息的类
+ `prefix_chars`,`选项`的前缀字符集(默认:`-`)
+ `fromfile_prefix_chars`,额外的参数应该读取的文件的前缀字符集(默认:`None`)
+ `argument_default`,参数的全局默认值(默认:`None`）
+ `conflict_handler`,解决冲突的可选参数的策略(通常没有必要额外设置)
+ `add_help`,给解析器添加`-h/–help`选项(默认:`True`)

#### add_argument

增加命令行参数,其完整签名如下:

`parser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])` 

方法的参数说明如下:

+ `name or flags`
    命令行参数名或者选项，如上面的`address`或者`-p,--port`.其中`命令行参数`指的是不以`-`或`--`开头的项,`选项`则是以`-`或`--`开头的项.
    `命令行参数`类似函数中没有默认值的位置参数,在解析时是必填的,且如果为其设置`default`也不会生效.
    `选项`则类似函数中的关键字参数,我们可以用default设置默认值.一般来说选项是选填的.
    `add_argument()`方法必须知道要设置的是`命令行参数`还是`选项`

+ `action`
    `action`关键字参数指出应该如何处理命令行参数.支持的动作有:
    
    + `store`,只是保存参数的值,这是默认的动作
    + `store_const`,保存由参数`const`指出的值.(注意`const`默认是None.)`store_const`动作最常用于指定某种标记的可选参数.
    + `store_true`和`store_false`,它们是`store_const`的特殊情形,分别用于保存值`True`和`False`.另外它们分别会创建对应的默认值
    + `append`,保存一个列表并将每个参数值附加在列表的后面.这对于允许指定多次的`选项`很有帮助.示例用法: `-I /usr/include -I /local/include`
    + `append_const`,保存一个列表并将`const`关键字参数指出的值附加在列表的后面.(注意`const`关键字参数默认是`None`).`append_const` 动作在多个参数需要保存常量到相同的列表时特别有用.
    + `count`,计算`选项`字面量出现的次数.比如定义选线为`-v`,如果输入为`-vvv`则`v`会被记为`3`
    + `help`,打印当前解析器中所有选项的完整的帮助信息然后退出.默认情况下`help`动作会自动添加到解析器中.
    + `version`,它需要配合参数`version`,在调用时打印出版本信息并退出.这个动作只对输出版本信息有用,用法类似:`parser.add_argument('--version', action='version', version='2.0.0')`

+ `nargs`, 命令行参数的个数,一般使用通配符表示,其中
    + `'?'`表示只用一个
    + `'*'`表示0到多个
    + `'+'`表示至少一个
+ `default`,默认值,当设置命令行参数时无效

+ `type`,参数的类型,命令行中传入的参数默认是字符串`str`类型,我们可以设置`type`为其指定类型转换函数.这也就顺便监测了输入参数是否符合要求.通常有这些设置:
    + `float`,`int`等
    + `ascii`
    + `pathlib.Path`
    我们当然也可以用类似`open`这样的函数直接处理文件,但这样写不利于关闭文件,因此不推荐
    
+ `choices`,可以看做是`default`的扩展,参数的值必须在`choices`的范围内
    
+ `required`,一般情况下,`argparse`模块假定`选项`是可选的,如果要使得选项变成必选的可以指定`required=True`
    
+ `help`,和`ArgumentParser`方法中的参数作用相似，出现的场合也一致


#### parse_args

执行解析命令行参数,完整签名为:

`parser.parse_args()` 

### 一个简单的例子

我们来写一个实现求整数开根的命令行工具,它有`--help(-h)`和`--version(-v)`两个参数信息

代码如下:


```python
%%writefile src/cmd/std/sqrt_std.py
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import argparse
from math import sqrt
__version__="0.1.0"

def sqrtarg(number):
    return sqrt(number)

def version():
    return "version:"+__version__

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, help=u"求开根的参数")
    parser.add_argument("-v","--version", help=u"查看版本号",action="version",version=__version__)
    args = parser.parse_args()
    if args.number:
        print(sqrtarg(args.number))

if __name__ == '__main__':
    main()
```

    Writing src/cmd/std/sqrt_std.py



```python
!python src/cmd/std/sqrt_std.py
```

    usage: sqrt_std.py [-h] [-v] number
    sqrt_std.py: error: the following arguments are required: number



```python
!python src/cmd/std/sqrt_std.py -h
```

    usage: sqrt_std.py [-h] [-v] number
    
    positional arguments:
      number         求开根的参数
    
    options:
      -h, --help     show this help message and exit
      -v, --version  查看版本号



```python
!python src/cmd/std/sqrt_std.py -v
```

    0.1.0



```python
!python src/cmd/std/sqrt_std.py 36
```

    6.0


### 运行细节

1. type参数只是类型检验,传入的参数还是字符串
2. 不需要写usage
3. 有`nargs`参数的话获取的对应是一个list
4. 参数传入实际上是被存入了一个namespace的空间中.这个空间有俩参数,其中一个是方法名命名的一个list,要调用使用`args.方法名`即可
5. 如果参数中有只能接受一个的情况,可以加入判断
    ```python
    if args.methodname1 == args.methodname1:  
        print 'usage: ' + __file__ + ' --help'  
        sys.exit(2)  
    ```

    来判断两个参数,要么都存在,要么都不存在,即可满足要求  


### 子解析

如果要写一个类似git那样复杂的有子命令如add,push pull等的工具,单单用上面的解析工具是不够的,需要使用`add_subparsers([title][, description][, prog][, parser_class][, action][, option_string][, dest][, help][, metavar])`命令

其中:
+ `title`,在输出的帮助中子解析器组的标题.默认情况下如果提供`description`参数则为"subcommands",否则使用位置参数的标题
+ `description`,在输出的帮助中子解析器组的描述,默认为`None`
+ `prog`,与子命令的帮助一起显示的使用帮助信息,默认为程序的名字和子解析器参数之前的所有位置参数
+ `parser_class`,用于创建子解析器实例的类,默认为当前的解析器(例如ArgumentParser)
+ `dest`,子命令的名字应该存储的属性名称;默认为`None`且不存储任何值
+ `help`,在输出的帮助中子解析器中的帮助信息,默认为`None`
+ `metavar`,在帮助中表示可用的子命令的字符串;默认为`None`并以`{cmd1, cmd2, ..}`的形式表示子命令


```python
parser = argparse.ArgumentParser()
parser.add_argument('--foo', action='store_true', help='foo help')

subparsers = parser.add_subparsers(help='sub-command help')
parser_a = subparsers.add_parser('a', help='a help')
parser_a.add_argument('bar', type=int, help='bar help')

parser_b = subparsers.add_parser('b', help='b help')
parser_b.add_argument('--baz', choices='XYZ', help='baz help')
parser.parse_args(['a', '12'])
```




    Namespace(foo=False, bar=12)




```python
parser.parse_args(['--foo', 'b', '--baz', 'Z'])
```




    Namespace(foo=True, baz='Z')



处理子命令的一个特别有效的方法是将`add_subparsers()`方法和`set_defaults()`调用绑在一起使用,这样每个子命令就可以知道它应该执行哪个Python函数.例如:


```python
def foo(args):
    print(args.x * args.y)
def bar(args):
    print('((%s))' % args.z)
```


```python
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_foo = subparsers.add_parser('foo')
parser_foo.add_argument('-x', type=int, default=1)
parser_foo.add_argument('y', type=float)
parser_foo.set_defaults(func=foo)

parser_bar = subparsers.add_parser('bar')
parser_bar.add_argument('z')
parser_bar.set_defaults(func=bar)

```


```python
args = parser.parse_args('foo 1 -x 2'.split())
args
```




    Namespace(x=2, y=1.0, func=<function foo at 0x7f7f10822950>)




```python
args.func(args)
```

    2.0



```python
args = parser.parse_args('bar XYZYX'.split())
args
```




    Namespace(z='XYZYX', func=<function bar at 0x7f7f10822ef0>)




```python
args.func(args)
```

    ((XYZYX))


这样的话你可以让`parse_args()`在参数解析完成之后去做调用适当的函数的工作.像这种方式将函数和动作关联起来是最简单的方法来处理你每个子命令的不同动作.然而如果需要检查调用的子命令的名字,用`dest`关键字参数调用`add_subparsers()`就行


```python
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser_name')
subparser1 = subparsers.add_parser('1')
subparser1.add_argument('-x')
subparser2 = subparsers.add_parser('2')
subparser2.add_argument('y')
parser.parse_args(['2', 'frobble'])
```




    Namespace(subparser_name='2', y='frobble')



### 参数分组

很多时候参数是相互配合使用的,这就可以用`add_argument_group(title=None, description=None)`分组


```python
parser = argparse.ArgumentParser(prog='PROG', add_help=False)
group1 = parser.add_argument_group('group1', 'group1 description')
group1.add_argument('foo', help='foo help')
group2 = parser.add_argument_group('group2', 'group2 description')
group2.add_argument('--bar', help='bar help')
```




    _StoreAction(option_strings=['--bar'], dest='bar', nargs=None, const=None, default=None, type=None, choices=None, required=False, help='bar help', metavar=None)




```python
parser.print_help()
```

    usage: PROG [--bar BAR] foo
    
    group1:
      group1 description
    
      foo        foo help
    
    group2:
      group2 description
    
      --bar BAR  bar help


要一组参数互斥,可以使用`add_mutually_exclusive_group(required=False)`.注意`required`参数用于指示互斥分组中至少有一个参数是必需的


```python
%xmode Plain
parser = argparse.ArgumentParser(prog='PROG')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--foo', action='store_true')
group.add_argument('--bar', action='store_false')
parser.parse_args(["--foo","--bar"])
```

    Exception reporting mode: Plain


    usage: PROG [-h] (--foo | --bar)
    PROG: error: argument --bar: not allowed with argument --foo



    An exception has occurred, use %tb to see the full traceback.


    Traceback (most recent call last):


      File ~/anaconda3/lib/python3.10/argparse.py:1859 in parse_known_args
        namespace, args = self._parse_known_args(args, namespace)


      File ~/anaconda3/lib/python3.10/argparse.py:2072 in _parse_known_args
        start_index = consume_optional(start_index)


      File ~/anaconda3/lib/python3.10/argparse.py:2012 in consume_optional
        take_action(action, args, option_string)


      File ~/anaconda3/lib/python3.10/argparse.py:1931 in take_action
        raise ArgumentError(action, msg % action_name)


    ArgumentError: argument --bar: not allowed with argument --foo


    
    During handling of the above exception, another exception occurred:


    SystemExit: 2



    /Users/mac/anaconda3/lib/python3.10/site-packages/IPython/core/interactiveshell.py:3468: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
      warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)



```python
parser.parse_args([])
```

    usage: PROG [-h] (--foo | --bar)
    PROG: error: one of the arguments --foo --bar is required



    An exception has occurred, use %tb to see the full traceback.


    SystemExit: 2




```python
parser.parse_args(["--foo"])
```




    Namespace(foo=True, bar=True)



### 多级子命令

如果我们的命令行工具有更加复杂的子命令解析需求,那么我们可以使用如下的方式做扩展:

```python

class Command:

    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            description='xxxxxx',
            usage='''xxxx <command> [<args>]

The most commonly used xxx commands are:

   clean       clean a project
   install     install a package

   
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        self.argv = argv
        args = parser.parse_args(argv[0:1])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()


    def clean(self):
        parser = argparse.ArgumentParser(
            description='clean a project')
        parser.add_argument(
            '-A', '--all', action='store_true')
        parser.set_defaults(func=clean)
        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def install(self):
        parser = argparse.ArgumentParser(
            description='install a package for this project')
        parser.add_argument('packages', nargs='?', type=str, default="DEFAULT")
        parser.add_argument(
            '-D', '--dev', action='store_true')
        parser.add_argument(
            '-T', '--test', action='store_true')
        parser.add_argument(
            '-A', '--all', action='store_true')
        parser.set_defaults(func=install)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("install done!")
        
def main(argv: Sequence[str]=sys.argv[1:]):
    Command(argv)
```

### 更加pythonic的替代品

实话说python的标准库还是比较有C/C++语言的风格残留的,而现如今的python代码风格会更加'魔法'一些,会用到比较多的装饰器工具.
[click](http://click.pocoo.org/)就是一个比较符合现在python编程风格的工具.它是一个比较重的命令行解析工具,它还包括了参数类型检验等复杂的功能,很适合构建复杂的命令行工具.不过命令行工具做的太复杂就不太符合它的定位了,因此这边不多讲.

他的用法也不复杂,使用python的装饰器声明参数,并自动构建帮助文档,具体的细节可以看官方文档.



## 所见即所得的命令行的工具(docopt)

[docopt](https://github.com/docopt/docopt)的特色是利用文件的`__doc__`,解析命令行参数构建参数组成的字典来自动识别.它可以使用pip安装,并完全支持pypy

我们用docopt改写上面的开方工具


```python
%%writefile src/cmd/doc/sqrt_doc.py
#!/usr/bin/env python
# coding:utf-8 
u"""
Usage: 
  test1.py [option] <num>...
  test1.py (-v|--version)
  test1.py (-a|--all)
  test1.py (-h|--help)
  

Options:
  -h --help      帮助
  -v --version   显示版本号.
  -a --all       显示全部参数
"""

from docopt import docopt
from math import sqrt
__version__="0.1.0"



def version():
    return "version:"+__version__

def main():
    args = docopt(__doc__)
    
    if args.get("-h") or args.get("-help"):
        print(__doc__)
    elif args.get("-v") or args.get("--version"):
        print(__version__)
    elif args.get("-a") or args.get("--all"):
        print(args)
    elif args.get("<num>"):
        print(" ".join(map(lambda x :str(sqrt(float(x))),args.get("<num>"))))
    else:
        print("wrong args!")
        print(__doc__)



if __name__ == '__main__':
    main()
```

    Overwriting src/cmd/doc/sqrt_doc.py



```python
!python src/cmd/doc/sqrt_doc.py
```

    Usage: 
      test1.py [option] <num>...
      test1.py (-v|--version)
      test1.py (-a|--all)
      test1.py (-h|--help)



```python
!python src/cmd/doc/sqrt_doc.py -a
```

    {'--all': True,
     '--help': False,
     '--version': False,
     '<num>': [],
     'option': False}



```python
!python src/cmd/doc/sqrt_doc.py -v
```

    0.1.0



```python
!python src/cmd/doc/sqrt_doc.py -h
```

    Usage: 
      test1.py [option] <num>...
      test1.py (-v|--version)
      test1.py (-a|--all)
      test1.py (-h|--help)
      
    
    Options:
      -h --help      帮助
      -v --version   显示版本号.
      -a --all       显示全部参数



```python
!python src/cmd/doc/sqrt_doc.py 36
```

    6.0


### 细节

+ 用`<>`包裹表示参数,如果参数后面有`...`则表示参数是列表
+ 用`[]`包裹选项
+ 用`()`包裹必选内容
+ 用`|`区分选项

这边有一个详细的[匹配细节](http://docopt.org)和[测试工具](http://try.docopt.org/)

docopt写起来并不会省代码,但它所见即所得,更加直观,当你写完注释的时候你的命令行解析也实现了.


## 补充: 为命令行工具自动创建gui

[Gooey](https://github.com/chriskiehl/Gooey)是一个可以将python命令行自动转成gui的工具,它依赖`wxpython`,废话不多说,看例子.我们来将之前的命令行工具转化一下


```python
%%writefile src/cmd/std/sqrt_std_gui.py
#!/usr/bin/env python3
import argparse
from math import sqrt
from gooey import Gooey, GooeyParser


__version__="0.1.0"

def sqrtarg(number):
    return sqrt(number)

def version():
    return "version:"+__version__
@Gooey(language='chinese')
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, help=u"求开根的参数")
    parser.add_argument("-v","--version", help=u"查看版本号",action="store_true")

    args = parser.parse_args()
    
    if args.version:
        print(version())
    if args.number:
        print(sqrtarg(args.number))

if __name__ == '__main__':
    main()
```

    Overwriting src/cmd/std/sqrt_std_gui.py



```python
!python src/cmd/std/sqrt_std_gui.py
```

    This program needs access to the screen. Please run with a
    Framework build of python, and only when you are logged in
    on the main display of your Mac.


## 补充: python3命令行工具的发布

我的用python写的脚本直接运行当然是可以,用Shebang结合权限设定也可以在一般的情况下使用,但如果我们的希望它成为可以随时使用的工具,更好的方式是将它用setuptool安装到python的脚本位置(当然也可以上传到pypi上供大家使用),

这边给出两个的`setup.py`文件作为参考

将std文件夹中文件结构改成

```
|-lib\
|    |-__init__.py
|    |-sqrt_std.py
|-setup.py
```


```python
%%writefile src/cmd/std/setup.py

from setuptools import setup,find_packages
import os
pathroot = os.path.split(os.path.realpath(__file__))[0]
setup(
    name='sqrt_std',
    version='0.1.0',
    packages = find_packages(),
    entry_points = {
        'console_scripts': ['sqrt_std=lib.sqrt_std:main'],
    }
)
```

    Writing src/cmd/std/setup.py


之后到目录下开始编译
`python setup.py install`
