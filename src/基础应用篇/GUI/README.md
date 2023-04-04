# GUI

鼠标和微软苹带来了GUI这种交互方式,它的最大特点是图像化,依靠点击来选择指令,而且一般除了主页面外,还会有多层的子页面.交互模式开始复杂了起来.


从GUI诞生开始,设计和美学开始进入这个领域,而对用户的友好程度成为了一个软件的衡量标准之一.

本文的执行环境需要自己为`ipython notebook`编写的子进程执行魔术命令`%exec_py`,可以参考[这篇文章](http://blog.hszofficial.site/TutorialForJupyter/ipython%E4%B8%8E%E9%AD%94%E6%B3%95%E5%91%BD%E4%BB%A4/ipython%E4%B8%8E%E9%AD%94%E6%B3%95%E5%91%BD%E4%BB%A4.html)自行实现和配置.

## GUI的设计原则

GUI的图形化特点带了了用户学习难度的降低,因此GUI包括后来的各种交互模式的设计最重要的就是以人为本,关注用户体验

+ 必须考虑目标用户群体是个什么样的群像

+ 必须考虑用户的学习成本,突出简化最主要的需求的操作,并尽量让用户用更少的步骤完成需求

+ 设计应该符合常识习惯

+ 避免频繁的切换界面,界面间应该风格统一和谐


本文的GUI编程攻略是针对python标准库Tkinter,网络上相关的资料比较少,因此很多人对其有"难用"的映像,实际上Tkinter可以说是最符合Python风格的gui框架了--极少的组件通过简单组合就可以构造一个简洁够用的GUI界面.

本文的执行环境需要自己为`ipython notebook`编写的子进程执行魔术命令`%exec_py`,可以参考[这篇文章](http://blog.hszofficial.site/TutorialForJupyter/ipython%E4%B8%8E%E9%AD%94%E6%B3%95%E5%91%BD%E4%BB%A4/ipython%E4%B8%8E%E9%AD%94%E6%B3%95%E5%91%BD%E4%BB%A4.html)自行实现和配置.