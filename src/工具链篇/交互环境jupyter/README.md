# `*`交互环境Jupyter

python是一门脚本语言,它可以按行执行.当你安装好了python环境后,在你的terminal中输入`python`就可以进入一个所谓的`交互环境`,你敲一行代码它执行一行代码.

交互环境已经被证明是非常有用的工具,现如今即便是java在java9中都有了交互环境支持.但老实说python的默认交互环境不好用,很原始很不智能.

[Jupyter](http://jupyter.org/)项目脱胎于ipython项目--一个更加友好的python交互环境工具.目前已经发展成了一个多功能的交互环境.这个交互环境的主要目标用户是数据科学家和在校学生老师.他们不同于一般开发者或者脚本小子,需要在交互环境下代码可以做修改,可以插入文本标记语言做更加专业的注释,需要可以插入`latex`公式,需要可以在交互界面直接展示可视化的成果,同时希望这个工具可以方便他们优化代码性能,甚至处理一些大规模分布式计算的需求.

这些需求造就了现在的jupyter项目.它也是数据科学家python技术栈中必定存在的一员.

## Jupyter的结构

Jupyter项目的模块化做的非常好,大致可以分为

+ 核心层`Kernels`,用于具体执行交互命令,其中python的核心层就是`ipykernel`,安装Jupyter后会默认安装并给出一个默认核心作为环境,其配置就指向安装jupyter的python.社区也提供了大量的第三方核心,这让Jupyter拥有了作为其他各种编程语言和软件交互环境的能力.
    核心层除了要安装对应的核心程序外还需要为其注册安装实例配置,管理当前环境下核心可以使用`jupyter kernelspec`相关的命令,配置一般会被放在`/usr/local/share/jupyter/kernels`或者`/Users/<用户名>/anaconda3/share/jupyter/kernels`下,其形式为一个带有`kernel.json`文件的的文件夹,一般文件夹名就是核心名.`kernel.json`中会有字段:
    + `language`: 指定编程语言
    + `display_name`: 指定在交互层中展示的命名
    + `argv`: 启动指定执行的命令
    + `interrupt_mode`(optional): 可选值为`signal`或`message`.指定客户端如何终止该内核上的单元执行.默认为`signal`.
    + `env`(optional): 为内核设置的环境变量字典.启动内核本质上就是启动一个进程,如果有设置则这些设置的环境变量将在内核启动前添加到内核进程的环境变量中.如果要导入当前进程中已经设置的环境变量则可以使用`${<ENV_VAR>}`作为值并将用相应的值替换.
    + `metadata`(optional): 描述内核的元信息字典,客户端用来帮助进行内核选择.

    除了必须有的`kernel.json`文件外,还可以有如下几个文件:
    + `logo-64x64.png`像素为64x64的logo图标
    + `logo-32x32.png`像素为32x32的logo图标
    + `logo-svg.svg`svg图标

    核心层中官方的就是python的核心`ipykernel`,这应该也是功能最全面支持最充分的核心,这块我们会在后面详细介绍.

+ 交互层,Jupyter提供了如下几种交互方式
    + `Jupyter Console`: 在命令行中启动一个交互界面,现在的`ipython`就相当于`Jupyter Console`+`ipykernel`.启动时需要使用`--kernel`指定核心名,比如在`Jupyter Console`启动`ipykernel`可以像下面这样启动

        ```bash
        jupyter console --kernel python3
        ```

    + `Qt console`: 启动一个qt界面,并将其作为交互界面进行交互操作,类似`Jupyter Console`,也需要使用`--kernel`指定核心名.比如在`Qt console`启动`ipykernel`可以像下面这样启动

        ```bash
        jupyter qtconsole --kernel python3
        ```

    + `Jupyter Notebook`:启动一个http服务,这个服务可以解析`.ipynb`文件并用它作为一个交互进程使用
    + `JupyterLab`: `Jupyter Notebook`的另一个版本,修改了notebook文件管理的交互逻辑让使用起来更像是ide

+ 多用户服务层,也就是`Jupyter hub`,专门用于为多用户提供隔离的环境

+ 工具层,专门处理notebook相关的工具,这些工具五花八门,后面会有一篇专门的介绍

## Jupyter的安装

Jupyter 现在是独立安装.当然,你依然需要装有`python`和`pip`.

```bash
pip install jupyter
```

如果你用brew 安装的python3,那么自然的

```bash
pip3 install jupyter
```

## 运行

```bash
jupyter <subcmd>
```
