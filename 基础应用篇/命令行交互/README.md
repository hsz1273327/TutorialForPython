# 命令行交互

我们肯定希望机器的输入和输出都是人类可以轻易理解的东西,但说起来简单做起来难,人和人沟通都时常有无法相互理解的情况更何况人和机器.在gui诞生之前人机交互的平台就是命令行.使用命令行本身就是一件有门槛的事情,熟练各种命令的人可以行云流水,但不熟练的人则会一脸懵逼,毕竟你只能通过键盘打字和程序沟通,这看起来很极客但其实还是很枯燥的.

Python作为一个初始设定就是系统脚本的编程语言,在命令行交互方面优缺点都非常明显:

优点:

+ 语法灵活,第三方工具多,可以快速实现很多东西.
+ 可以根据需要非常轻易的修改脚本以更新实现

缺点:

+ 依赖解释器,再小的功能也要带一整套python环境以及一堆依赖
+ 复杂功能由于依赖树过于复杂可能会很难移植

因此python的命令行交互通常使用上也会扬长避短:

+ 用于python程序的启动
+ 用于有比较复杂功能的命令行工具中
+ 用于快速构造或者在需求不明确的时候使用

在这部分我们会介绍如下几个方面:

1. 标准输入输出
2. 使用python如何构造一个命令行工具
3. 使用python如何构造一个repl
