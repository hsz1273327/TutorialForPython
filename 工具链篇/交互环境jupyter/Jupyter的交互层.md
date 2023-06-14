# Jupyter的交互层

Jupyter的交互层大致可以分为两种:

1. REPL交互式解释器前端,包括ipython,QT,Console这类直接输入python代码文本的前端界面.
2. Notebook解释器前端,就是Jupyter Notebook和Jupyter Lab两个基于网页技术的前端界面.

第一种没啥值得说的,正常用就好.第二种可以说是Jupyter项目的精华所在.

`Notebook`是Jupyter定义的一种文本文件.通常以`.ipynb`作为后缀,这种文件提供了一个文本,富文本,代码混合的开发环境,想象一下你可以在同一个文件中写作,编辑公式推导,编码,演示成果,这让Jupyter真正成为了神器.

Jupyter提供的Notebook解释器前端有两种,他们定位并不太一样:

+ `Jupyter Notebook`,基础版Notebook解释器前端,安装Jupyter就会默认安装.`Jupyter Notebook`的交互逻辑围绕notebook文件展开,官方的说法是上一代的Notebook解释器前端,但事实上是用的最广泛的一种形式.
+ `Jupyter Lab`,下一代的Notebook解释器前端,需要安装`jupyterlab`.交互逻辑更加接近编辑器.左侧有命令行系统,右侧则是编辑区.官方主推的交互形式,但似乎主要是企业单位用,个人用的不多.

## 基本用法

`Notebook`每个文件都由多个顺序的`cell`构成,无论在`Jupyter Notebook`还是`Jupyter Lab`中,每个`cell`可以在`code(代码模式)`,`markdown(markdown文本模式)`和`raw(字面量文本模式)`三种模式间切换.可以单独执行(shift+回车),也可以让`cell`上下移动改变执行顺序.

我们可以在`kernel`菜单中对当前执行的kernel进行中断,重启切换等操作.

## 插件

`Jupyter Notebook`和`Jupyter Lab`都支持插件扩展,但目前为止,由于历史原因他们的扩展并不通用.`Jupyter Notebook`既然是基础版,我个人会更加偏向于让它保持原始的状态.这边就单介绍`Jupyter Lab`了.

在`Jupyter Lab`界面的最左侧有个拼图一样的图标,它就是管理插件的位置.

插件一般是优化交互用的,因此通常依赖`node.js`和`ipywidgets`.前者需要再系统中安装,后者则可以使用pip安装.

在插件管理位置的`DISCOVER`栏目下可以查看到所有的第三方插件.我们可以在其中进行选择安装.这个交互逻辑总体来说类似在vscode插件管理的交互逻辑.

这里推荐几个插件

+ `@lckr/jupyterlab_variableinspector`,变量反射插件,可以唤出变量表格汇总所有变量状态