
# 文件与IO流

计算机离不开文件与IO流,文件是多数操作系统的基本构成单位,而IO流则是将数据用于运算和输出结果的工具.


本文就是介绍python处理文件系统和文件io的方法,python在异步关键字出现前只有同步的文件和文件系统接口,而现在有异步关键字后主流也还是使用同步接口,异步接口则是由第三方模块提供支持.

## 同步接口

这是到目前为止的主流方式,也是原生的文件相关操作方式.同步接口功能最全最多样,也最成熟,因此也更推荐这种写法.

### 文件系统

我们知道主流的操作系统文件系统都是由两部分组成

+ 文件夹
+ 文件

文件夹是保存文件的容器,基本上是起到分类管理不同文件的功能.文件埋藏在一层一层的文件夹之下,生成一个路径.多个路径组合成树状就可以描述一个系统的整体文件结构.

python3.4开始python标准库提供了一个文件系统的高级接口模块[pathlib](https://docs.python.org/3/library/pathlib.html)其常用功能大致在:

> 判断路径

功能|接口
---|---
判断路径是否存在|`.exists()`
判断路径是否是文件|`.is_file()`
判断路径是否是文件夹|`.is_dir()`
判断路径是否是符合特定的文本规则(由re定义)|`.match(pattern)`

> 获取路径信息

功能|接口
---|---
拼接路径|`.joinpath(str)`
拆分路径中的文件/文件夹|`.parts`
获取路径上一层的路径|`.parent`
获取文件/文件夹名|`.name`
获取文件多级后缀|`.suffixes`
获取文件后缀|`.suffix`
获取文件除后缀外的名字|`.stem`
通过路径获取其对应的uri表示|`.as_uri()`
获取路径的绝对路径表示|`.absolute()`
获取文件夹路径下的文件路径生成器|`.iterdir()`

> 文件系统操作

功能|接口
---|---
创建文件夹|`.mkdir()`
删除文件夹|`.rmdir()`
创建文件|`.touch()`
删除文件|`.unlink()`
查看文件/文件夹基本信息|`.stat()`
文件/文件夹改名|`.rename(target)`
文件/文件夹修改权限|`.chmod(mode)`


python还额外提供了两个包

+ [shutil](https://docs.python.org/3/library/shutil.html)用于将文件/文件夹递归的迁移至别处或整个文件/文件夹递归的删除
+ [tempfile](https://docs.python.org/3/library/tempfile.html)用于创建临时文件/文件夹


```python
from pathlib import Path

Path(".").absolute()
```




    PosixPath('/Users/huangsizhe/Workspace/Documents/TutorialForPython/python-io')



### 文件的IO流对象

python中的文件IO流,都是由bytes构成的,表现形式也只有两种:

+ `str`经过编码的bytes,默认为`utf-8`编码
+ `bytes`未经编码的bytes,一般图片音频等使用bytes

python的流对象都定义在`io`模块中,包括如下种类:

+ `TextIOWrapper`,继承自`TextIOBase`,`IOBase`

+ `BufferedReader`/`BufferedWriter`,继承自`BufferedIOBase`,`IOBase`

+ `StringIO`继承自`TextIOBase`, `IOBase`

+ `BytesIO`继承自`BufferedIOBase`,`IOBase`

+ `FileIO`继承自`RawIOBase`, `IOBase`


#### 文件对象

python从硬盘中读入的文件会被封装为文件对象(TextIOWrapper).

文件对象实质上是一个流对象.

从文件中提取文件对象的方式是使用

+ `open(filepath, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)`

    + buffering 指定缓冲策略,0为关闭缓冲(必须带`b`),大于0的整数为缓冲区大小,-1表示不固定
    + encoding 指定编码方式
    + errors 解码报错时报什么错
    + newline 定义使用何种方式换行可以是`None, '', '\n', '\r', and '\r\n'`
    + closefd,如果closefd为False，底层文件描述符将保持打开状态,文件关闭时。当给出文件名时，这不起作用在这种情况下必须为True。
    + opener,传递一个可打开的作为`opener`可以使用自定义的开启者。默认通过os.open作为`opener`
    + mode,  指定文件的读写模式
 
模式|描述
---|---
`r`	|以只读方式打开文件.文件的指针将会放在文件的开头.这是默认模式.
`rb`|以二进制格式打开一个文件用于只读.文件指针将会放在文件的开头.这是默认模式.
`r+`|打开一个文件用于读写.文件指针将会放在文件的开头.
`rb+`|以二进制格式打开一个文件用于读写.文件指针将会放在文件的开头.
`w`	|打开一个文件只用于写入.如果该文件已存在则将其覆盖.如果该文件不存在,创建新文件.
`wb`|以二进制格式打开一个文件只用于写入.如果该文件已存在则将其覆盖.如果该文件不存在,创建新文件.
`w+`|打开一个文件用于读写.如果该文件已存在则将其覆盖.如果该文件不存在,创建新文件.
`wb+`|以二进制格式打开一个文件用于读写.如果该文件已存在则将其覆盖.如果该文件不存在,创建新文件.
`a`	|打开一个文件用于追加.如果该文件已存在,文件指针将会放在文件的结尾.也就是说新的内容将会被写入到已有内容之后.如果该文件不存在,创建新文件进行写入.
`ab`|以二进制格式打开一个文件用于追加.如果该文件已存在,文件指针将会放在文件的结尾.也就是说新的内容将会被写入到已有内容之后.如果该文件不存在,创建新文件进行写入.
`a+`|打开一个文件用于读写.如果该文件已存在,文件指针将会放在文件的结尾.文件打开时会是追加模式.如果该文件不存在,创建新文件用于读写.
`ab+`|以二进制格式打开一个文件用于追加.如果该文件已存在,文件指针将会放在文件的结尾.如果该文件不存在,创建新文件用于读写.


`mode`中带有`b`的返回的对象是`BufferedReader`对象,不带的是`TextIOWrapper`而读写的不同也会带来方法的不同.open的使用方式最好结合上下文工具`with`语句使用


```python
with open("src/hello.txt","wb") as f:
    print(type(f).mro())
```

    [<class '_io.BufferedWriter'>, <class '_io._BufferedIOBase'>, <class '_io._IOBase'>, <class 'object'>]


针对不同的打开模式,文件对象的的方法会有些不同,但有些基本方法是共用的,就是继承自`IOBase`的方法

#### `IOBase`的基本方法

+ close()

    关闭文件对象

+ fileno()

    返回流的底层文件描述符(一个整数)(如果存在).如果IO对象不使用文件描述符,则会引发OSError.

+ flush()

    清空流的写入缓冲区(如果适用).这对于只读和非阻塞流不起作用.

+ isatty()

    如果流是交互式的(连接到终端/tty设备),返回True.

+ seek(offset[, whence])

    将流位置更改为给定的字节偏移.偏移量相对于由whence指示的位置进行解释.offset的默认值为SEEK_SET.可选的值为:

    + SEEK_SET or 0 – 流的开始(默认);偏移量应为零或正数
    + SEEK_CUR or 1 – 当前流位置;偏移可能为负
    + SEEK_END or 2 – 流的结尾,偏移量通常为负数 

    返回新的绝对位置。

+ seekable()

    如果流支持随机访问,则返回True.

+ tell()

    返回当前流的位置。

+ truncate(size=None)

    将流调整为给定大小(以字节为单位)(如果未指定大小,则调整当前位置).当前流位置不变.这种调整大小可以扩展或减少当前的文件大小.在扩展的情况下,新文件区域的内容取决于平台(在大多数系统上,其他字节为零填充).将返回新的文件大小.

> 与读写相关的方法有

+ readable()

    如果流可以读取,返回True.如果为False,则`read()`将引发OSError.

+ readline(size=-1)

    从流中读取并返回一行.如果指定了大小,则读取最多大小的字节.对于二进制文件,行终止符始终为b'\ n';对于文本文件,open()的newline参数可用于选择识别的行终止符.

+ readlines(hint=-1)

    读取并返回流中的行列表.可以指定提示来控制读取的行数:如果所有行的总大小(以字节/字符为单位)超过提示,则不会读取更多行.请注意,现在更加推荐的方式是使用
    ```python
    
    for line in file:
        func(line)
    ```
    而不调用file.readlines().


+ writable()

    如果流支持写入,则返回True.如果为False，write()和truncate()将引发OSError。

+ writelines(lines)

    将行写入流



#### TextIOBase的基本方法


+ detach()

    将底层二进制缓冲区与TextIOBase分开并返回.底层缓冲区分离后TextIOBase处于不可用状态.一些TextIOBase实现(如StringIO)可能不具有底层缓冲区的概念,调用此方法将引发`UnsupportedOperation`.


+ read(size)

    读入

+　write(s)

    写字符串到对象


#### BufferedIOBase的基本方法

+ detach()

    将底层原始流与缓冲区分开并返回.原始流已分离后,缓冲区处于不可用状态.一些缓冲区如BytesIO没有从该方法返回的单个原始流的概念,它们引发`UnsupportedOperation`


+ read(size=-1)

    读取并返回到大小字节,如果省略参数,则None或者否定数据被读取并返回,直到达到EOF.如果流已经处于EOF则返回空字节对象.如果参数为正,并且底层原始流不具有交互性,则可能会发出多个原始读取以满足字节计数(除非首先达到EOF).但是对于交互式原始流,最多只会发出一次原始读取,结果并不意味着EOF即将到来.如果底层原始流处于非阻塞模式并且目前没有可用的数据,则会引发`BlockingIOError`


+ read1(size=-1)

    读取并返回到大小字节,最多只能调用底层原始流的`read()`或`readinto()`方法.如果要在`BufferedIOBase`对象之上实现自定义的缓冲区,这将非常有用.

+ readinto(b)

    将字节读入预先分配的可写入字节的对象b并返回读取的字节数.像`read()`一样,可能会向底层的原始流发出多次读取,除非后者是交互式的.如果底层原始流处于非阻塞模式并且目前没有可用的数据,则会引发BlockingIOError。


+ readinto1(b)

    将字节读入预先分配的可写入字节的对象b,最多使用一个对底层原始流的`read()`或`readinto`方法的调用.返回读取的字节数.如果底层原始流处于非阻塞模式并且目前没有可用的数据,则会引发`BlockingIOError`


+ write(b)

    编写给定的类似字节的对象b,并返回写入的字节数(总是等于b的长度,以字节为单位),因为如果写入失败(`OSError`将被引发).根据实际的实现,这些字节可以容易地写入底层流,或者由于性能和延迟原因而被保存在缓冲器中.当处于非阻塞模式时,如果数据需要写入原始流但无法接受所有数据而不阻塞,则会引发`BlockingIOError`.该方法返回后,调用者可能会释放或变异b.因此在方法调用期间实现只能访问b.

#### 另一种读写文件的方式

FileIO类是读写文件的另一种方式,与open不同之处在于它继承自`RawIOBase`,也就是说它是没有缓冲区也没有解码过的的单纯文件io


```python
from io import FileIO
```


```python
with FileIO("src/hello.txt", mode='r', closefd=True, opener=None) as f:
    print(f.read())
```

    b''


#### RawIOBase的基本方法

+ read(size=-1)

    读出bytes

+ readall()

    从流中读取并返回所有字节,直到EOF,如果需要,可以使用多个流调用.

+ readinto(b)

    将字节读入预分配的可写入字节的对象b,并返回读取的字节数.如果对象处于非阻塞模式,并且没有字节可用,则返回None.

+ write(b)

    写入bytes

### 内存中生成文件对象

`io`模块可以用于生成文件对象其中有`StringIO`和`BytesIO`两种,头一种文件对象保存字符串,后一种则保存字节流

使用`io`模块生成的文件对象更多的是作为流使用,因此有一些特别的方法


+ getvalue()

    返回一个包含缓冲区的全部内容的str或者bytes

+ read1()

    BytesIO对象可以使用,读取并返回到大小字节,最多只能调用底层原始流的read()(或readinto())方法.如果您在BufferedIOBase对象之上实现自己的缓冲区,这将非常有用.

+ readinto1()

    BytesIO对象可以使用,将字节读入预先分配的可写入字节的对象b,最多使用一个对底层原始流的read()(或readinto())方法的调用.返回读取的字节数.如果底层原始流处于非阻塞模式,并且目前没有可用的数据,则会引发BlockingIOError.

+ getbuffer()

    BytesIO对象可以使用,在缓冲区的内容上返回可读写的视图(memoryview),而不复制它们.另外,视图的突变将会透明地更新缓冲区的内容


```python
from io import StringIO ,BytesIO
```


```python
steam = BytesIO(b"asdfg")
```


```python
steam.read()
```




    b'asdfg'




```python
steam.write(b"1234")
```




    4




```python
steam.getvalue()
```




    b'asdfg1234'




```python
view = steam.getbuffer()
```


```python
view[2:4] = b"56"
steam.getvalue()
```




    b'as56g1234'



## 异步文件io

各个操作系统的文件io都是同步的,
[aiofiles](https://github.com/Tinche/aiofiles)是最常用的异步文件io模块,它实际是使用多线程执行器对同步io做了封装.其使用方法和一般的io差别不大:


```python
import aiofiles
async def test_aiofile():
    async with aiofiles.open('README.md', mode='r') as f:
        contents = await f.read()
    print(contents)
```


```python
await test_aiofile()
```

    # python-io
    
    `IO`(输入输出)通常来讲不属于语法的范畴,但又是任何语言任何程序不可缺少的一块--程序往往用来处理输入,而结果则通过输出告知用户.
    
    
    通常讲io分为3种
    
    1. 标准输入输出
    2. 文件读写
    3. socket
    
    
    本篇介绍python的输入输出相关工具.但socket过于底层,本篇更加关注实际的使用.因此会再做细分
    
    1. 标准输入输出
    2. 文件io
    3. 数据库
    4. 消息队列
    
    再由于python现在区分同步异步,而异步编程的主要用武之地就在于io一块,所以在有两种不同编程方式的章节中我也会做出区分.
    


aiofiles除了对文件读写做了封装,还额外做了几个与文件相关的异步包装在`aiofiles.os`:

+ stat
+ sendfile
+ rename
+ remove
+ mkdir
+ rmdir


```python
from aiofiles import os 
```


```python
await os.stat('README.md')
```




    os.stat_result(st_mode=33188, st_ino=10179981, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=622, st_atime=1558764955, st_mtime=1558764703, st_ctime=1558764703)


