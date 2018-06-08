# 使用Cython优化python程序的性能

使用Cython是最主要的python扩展工具.本部分是性能优化篇最主要的内容.这部分首先是介绍cython的基本用法

+ Cython的基本使用流程
+ Cython的纯净模式
+ Cython的基本模式
+ Cython的包装模式

本篇我们用cython主要是使用基本模式,以后写C++攻略后会在其中补上包装模式的例子.
接着我们来应用Cython做些简单的工作

+ 使用cython结合numpy实现一个简单的感知器模型
+ 使用cython和矩阵运算库eigency,结合openmp实现一个简单的感知器模型
