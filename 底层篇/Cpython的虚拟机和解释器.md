# Cpython的虚拟机和解释器


## 可执行文件`python`的启动

而当我们运行可执行文件`python`时,它实际做了如下动作

1. 加载环境变量设置: 系统会检查环境变量,加载与PYTHON相关的环境变量以及PATH
2. 启动解释器: 系统会查找并启动Python可执行文件
3. 加载用户设置,内置模块,标准库和用户自定义的启动脚本等.Python解释器会在启动时寻找并执行一些特定的脚本文件,如:
    + `site.py`：负责设置Python的`site-specific`配置例如模块搜索路径等
    + `.pythonrc`或`.pythonrc.py`: 用户的个人启动脚本,用于设置个性化的环境.

4. 根据有没有指定脚本文件会执行
    1. 执行脚本(有指定脚本文件): 从上到下的一行一行执行指定的脚本中的代码
    2. 交互式模式(没有指定脚本文件): 执行预加载脚本,进入交互式模式,等待用户输入Python代码并逐行执行

## CPython的虚拟机

CPython 使用一个基于栈的虚拟机.也就是说它完全面向栈数据结构的(你可以"推入(push)"一个东西到栈顶，或者从栈顶上"弹出(pop)"一个东西来).

CPython 使用三种类型的栈:

+ 调用栈(call stack)

    这是运行 Python 程序的主要结构.它为每个当前活动的函数调用使用了一个东西--"帧(frame)".栈底是程序的入口点.每个函数调用推送一个新的帧到调用栈,每当函数调用返回后,这个帧被销毁.

+ 计算栈(evaluation stack)

    也称为数据栈(data stack).在每个帧中有一个计算栈.这个栈就是 Python 函数运行的地方.运行的 Python 代码大多数是由推入到这个栈中的东西组成的,这个栈负责操作它们.然后在返回后销毁它们

+ 块栈(block stack)

    在每个帧中还有一个块栈.它被 Python 用于去跟踪某些类型的控制结构--循环、`try / except 块`、以及 `with 块`，全部推入到块栈中,当你退出这些控制结构时块栈被销毁.这将帮助 Python 了解任意给定时刻哪个块是活动的.比如一个 continue 或者 break 语句可能影响正确的块.

## python的字节码

cpython实际上运行的是字节码,我们所写的python源文件之所以可以被执行,其原因是当python程序加载时,源文件会被先翻译为字节码.然后保存在同级文件的`__pycache__`文件夹下.下次执行是,如果`__pycache__`下的字节码文件和源码文件修改时间匹配一致就会直接执行`__pycache__`中缓存的字节码,不一致则会将对应的字节码替换.

python的字节码在旧版本中有两种,一种是常规的`.pyc`文件,其加载速度相对于之前的.py文件有所提高,而且还可以实现源码隐藏,以及一定程度上的反编译;另一种是经过优化的`.pyo`文件(相比于`.pyc`文件更小),也可以提高加载速度.

而现在则统一都是以`.pyc`作为后缀,优化的等级则显式的放在编译后文件的命名上.

### 编译模块到`.pyc`

编译到`.pyc`我们可以使用两个标准库提供的工具:

+ `py_compile`用于编译单独的源码文件

+ `compileall`用于将某个文件夹下的源码文件递归地进行编译

#### **单文件编译**

使用`py_compile`单独编译一个文件的话,可以使用命令行工具

```shell
python -m py_compile /path/to/需要生成.pyc的脚本.py
```

即可.

也可以在python脚本下使用,调用`py_compile`:

```python
py_compile.compile(file[, cfile[, dfile[, doraise]]])
```

其中

+ `file`,表示需要生成`.pyc`或`.pyo`文件的源码路径;
+ `cfile`，表示需要生成`.pyc`或`.pyo`文件的目标文件路径.它默认是以`.pyc`为扩展名的形如`xxxx.cpython-36.pyc`这样形式的字符串.此外，当且仅当所使用的解释器允许编译成.pyo文件,才能以`.pyo`结尾,这个后文说.
+ `dfile`,表示编译出错时,将报错信息中的名字`file`替换为`dfile`
+ `doraise`，设置是否忽略异常.若为`True`,则抛出`PyCompileError`异常;否则直接将错误信息写入`sys.stderr`.

类似的,编译整个文件夹可以使用命令行工具`compileall`

```shell
python -m compileall <dir>
```

常用的参数有`-b`表示写入它们源文件同级并且同名不同后缀

也可以在python脚本下使用,调用`compileall`:

```python
import compileall

compileall.compile_dir('Lib/', force=True)
```

compile_dir参数有:

+ `dir`目标文件夹
+ `maxlevels=10`文件夹最大递归深度
+ `ddir=None`检查ddir中二进制文件的时间戳,如果与目标文件不一致才会编译
+ `force=False`强制编译
+ `rx=None`使用`re`查找目标文件夹下要编译的文件
+ `quiet=0`是否输出编译过程
+ `legacy=False`字节码文件是否被写入它们源文件同级并且同名(python2的默认编译行为),它们可能覆盖由另一版本的Python创建的字节码文件
+ `optimize=-1`优化等级,
+ `workers=1`多进程编译

#### **编译优化**

使用命令行工具编译是否优化的标志位在python一级,使用`-O`表示优化等级为1,`-OO`表示优化等级为2级(相比1级去掉了文档字符串),经过优化的字节码文件会被默认的命名为`xxxx.cpython-36.opt-2.pyc`这样的形式.

单文件的1级优化编译

```shell
python -O -m py_compile /path/to/需要生成.pyo的脚本.py
```

文件夹下递归2级优化编译:

```shell
python -O -m compileall -b <path>
```

需要注意编译后的字节码文件并不会提高运行时的执行速度,只会提高模块的加载速度.

### 反编译

指望通过编译python源文件来反编译是不现实的,使用[uncompyle6](https://github.com/rocky/python-uncompyle6)工具可以非常轻易的将`.pyc`反编译为源码`.py`文件.`uncompyle6`可以直接使用`pip`工具安装.

### Python解释器的REPL环境定制

Python解释器很多时候也作为REPL环境的入口.针对REPL环境,Python提供了一个预加载机制和其对应的环境变量`PYTHONSTARTUP`.

`PYTHONSTARTUP`需要指定一个`python`脚本文件,在其中我们可以定义函数,变量,类等等,他们会在REPL环境中称为全局对象,不用import就可以使用.具体例子可以看[python-startup这个项目](https://github.com/jezdez/python-startup/blob/master/startup.py).