# Jupyter的核心层

Jupyter的核心层通常是由如下几个部分组成:

+ 可以使用`zeromq`以及`openssl`和交互层通信的核心程序,这个程序是一个,满足[特定协议](https://jupyter-client.readthedocs.io/en/latest/messaging.html)的zeromq服务
+ 声明核心配置,图标及扩展的配置文件夹,这个文件夹就被称为核`kernel`

因此Jupyter的核心层安装实际上是两步:

1. 安装核心程序,这个程序一般是一个可执行程序或者一个python的可执行脚本.
2. 安装核,也就是构造一个调用核心程序的配置文件夹

一些核心程序安装的时候就会顺道把核给安装了.

操作核的命令是`jupyter kernelspec <cmd>`

和常规一样,

+ `list`查看已有核的状态
+ `install`安装一个核,不过一般来说多数核心程序都自己提供了安装工具,普遍都不用这个方法装核
+ `remove/uninstall`移除一个核.

安装完的核一般会被放在如下几个位置(以在mac中为例):

+ anaconda原生级:`<anaconda根目录路径>/share/jupyter/kernels/`
+ 系统级:`/usr/local/share/jupyter/kernels/`
+ 用户级:`/Users/<用户名>/Library/Jupyter/kernels/`

anaconda原生级通常只会是安装anaconda后自己将默认的python核心放在里面,多数第三方核心程序提供的安装命令行工具通常会默认将核心安装在用户级,而系统级一班要在执行安装程序时指定flag才会被安装.

我们启动jupyter的时候相当于调用核的配置启动一个核心程序实例,然后再用前端交互层去与之通信让核心程序执行命令

## Jupyter的核心层与ipython

`jupyter`项目脱胎于`ipython`,而现在`ipython`依然具有完整的命令行交互功能,如果你的机器不需要Juypter那些特性只需要一个本分好用的python的命令行交互界面那直接安装ipython即可.在Jupyter体系下它更多的被用作如下几个用途:

+ 提供魔法命令支持
+ 在notebook中提供额外的输出优化.

`ipykernel`则是由`ipython`扩展出来专门支持Jupyter的一个库,它被用作:

+ 命令行脚本`ipykernel_launcher`作为python语言的核心程序
+ 以`ipykernel.kernelbase.Kernel`和`ipykernel.kernelapp.IPKernelApp`为基础构造新的核心程序

从另一个角度讲,Jupyter的核心程序可以认为有两种:

1. `Wrapper kernel`,即使用Ipython构建的核心程序.一般这类性能都一般,但胜在可扩展性会比较好
2. `Native kernels`,不使用Ipython构建的核心程序.一般这类就是直接用zeromq和前端进行通信交互了,性能往往会更好些,但一般都难以扩展.

![kernel_type](../../source/jupyter/kernel_type.webp)

### ipython的设置

ipython以及其他`Wrapper kernel`都会在启动时读取设置目录.这个设置目录有如下几个功能:

1. 配置ipython中的一些交互元素
2. 执行启动钩子

ipython的设置都在`~/.ipython`目录中,通过执行`ipython profile create`命令创建默认的ipython设置,这个设置在`~/.ipython/profile_default`文件夹下.
它会至少包含`ipython_config.py`和`ipython_kernel_config.py`两个配置文件.同时还会有一个`startup`文件夹用于配置启动时的额外加载项.