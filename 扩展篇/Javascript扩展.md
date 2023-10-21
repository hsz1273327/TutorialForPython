# Javascript扩展

在python中要调用js可以使用第三方库[PyMiniRacer](https://github.com/sqreen/PyMiniRacer),使用`pip install py-mini-racer`安装.

由于js本身也是个解释型脚本语言,py-mini-racer干的事其实就是把v8引擎嵌入了python中,我们可以直接使用`MiniRacer`类的实例方法`eval`,`call`以及`execute`来执行js代码文本.无论哪种方式运行过程都保存在实例中.


```python
from py_mini_racer import py_mini_racer
ctx = py_mini_racer.MiniRacer()
```

> 执行代码

使用`eval`接口就可以执行代码,代码在`MiniRacer`对象中执行,其中定义变量包括函数我们并不能在python中获得,通常两个用途:

+ 执行表达式,表达式的值会被python获取
+ 执行函数,类,模块,变量等的申明,然后使用`call`接口调用函数获取结果


```python
ctx.eval("1+1")
```




    2



> 调用函数


```python
ctx.eval("const fun = () => ({ foo: 1 })")
```


```python
ctx.call("fun")
```




    {'foo': 1}



## PyMiniRacer的安装

这个项目已经很久没人维护了,目前官方只支持x86_64平台上windows,macos和linux环境,如果你希望在arm64平台使用可以参考下面的方法:

+ linux:可以直接下载[网友编译好的wheel包](https://blog.csdn.net/KongDong/article/details/130182040),这个包本项目下也有备份
+ macos:直接安装`py-mini-racer`,然后将[libmini_racer.dylib](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/software/pyminiracer/libmini_racer.dylib)方到安装好的`py-mini-racer`项目根目录下.这个动态链接库本项目也有备份
