
# GUI

鼠标和微软苹带来了GUI这种交互方式,它的最大特点是图像化,依靠点击来选择指令,而且一般除了主页面外,还会有多层的子页面.交互模式开始复杂了起来.


从GUI诞生开始,设计和美学开始进入这个领域,而对用户的友好程度成为了一个软件的衡量标准之一.

# GUI的设计原则

GUI的图形化特点带了了用户学习难度的降低,因此GUI包括后来的各种交互模式的设计最重要的就是以人为本,关注用户体验

+ 必须考虑目标用户群体是个什么样的群像

+ 必须考虑用户的学习成本,突出简化最主要的需求的操作,并尽量让用户用更少的步骤完成需求

+ 设计应该符合常识习惯

+ 避免频繁的切换界面,界面间应该风格统一和谐

# python的GUI编程(Tk)

GUI也就是图形界面啦,Python有不少GUI框架,而tkinter是自带的,为啥选这个呢,因为一般用Python写GUI都不会写多复杂,也就是够用就好.最符合这一要求的就是tkinter了,Python自带,逻辑简单,模块少而够用.


## 第一个例子


```python
%%writefile src/first.py
import tkinter

tkinter._test()
```

    Overwriting src/first.py


运行这个脚本,是不是跳出了一个小框框.这是tk的自带例子


```python
%exec_py3 src/first.py
```

## 第一个例子 +

我们来自己写个例子,体会下tk的逻辑


```python
%%writefile src/firstGUI.py

#coding:utf-8
from tkinter import Frame,Label,Button


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #窗口大小位置
        self.master.geometry("600x400+100+400")#长x宽+x+y
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!')
    
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit',fg="red", command=self.quit)
        self.quitButton.pack()

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')

    app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/firstGUI.py



```python
%exec_py3 src/firstGUI.py
```

运行后出现如图小对话框

![]()


可以看出,主类继承自Frame基类

每个Button、Label、输入框等，都是一个Widget。Frame则是可以容纳其他Widget的Widget，所有的Widget组合起来就是一棵树。

pack()方法把Widget加入到父容器中，并实现布局。pack()是最简单的布局，grid()可以实现更复杂的布局。

在createWidgets()方法中，我们创建一个Label和一个Button，当Button被点击时，触发self.quit()使程序退出

## 组件

tkinter的控件主要有这些:

+ Label 标签
+ Button 按钮
+ Toplevel
+ Canvas
+ Checkbutton
+ Entry
+ Frame
+ LabelFrame
+ Listbox
+ Menu 
+ Menubutton
+ Message
+ OptionMenu
+ PaneWindow 
+ Radiobutton 
+ Scale 
+ Scrollbar 
+ Spinbox 
+ Text 
+ Bitmap
+ Image
+ ScrolledText.frame
+ ScrolledText.vbar


> 标签 Label

标签可以定义的属性主要有:

+ text 标签的内容,文本信息

+ font 字体

+ background 背景色


> 按钮 Button

按钮算是最常用的控件之一了,它的属性主要有:

+ 宽度 width
+ 高度 height
+ 背景色 background
+ 显示文字 text 

但是说到按钮当然最重要的是触发事件了

+ 命令 command 接受一个函数名,注意是函数名,没有括弧

>输入框 Entry

属性:

+ get() 获取输入(返回一个str)

例:一个用户登录界面


```python
%%writefile src/entry.py

from tkinter import Frame,Label,Button,Entry


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.userLabel = Label(self, text='用户名:')
        self.userLabel.grid(row = 0,column = 0,sticky="w")
        self.userEntry = Entry(self)
        self.userEntry.grid(row = 0,column = 1,sticky="e")
        self.pwLabel = Label(self, text='密码:')
        self.pwLabel.grid(row = 1,column = 0,sticky="w")
        self.pwEntry = Entry(self)
        self.pwEntry.grid(row = 1,column = 1,sticky="e")

        self.enterButton = Button(self,text = "登录",command = self.reg)
        self.enterButton.grid(row = 2,column = 1,sticky = "e")

        self.logLabel = Label(self, text='')
        self.logLabel.grid(row = 3)

    def reg(self):
        s1 = self.userEntry.get()
        s2 = self.pwEntry.get()
        if s1 == "www.google.com" and s2 == "www.bing.com":
            self.logLabel["text"]="登录成功"
        else:
            self.logLabel["text"]="用户名或密码错误"
            self.userEntry.delete(0,len(s1))
            self.pwEntry.delete(0,len(s1))

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('登录界面')
    #窗口大小位置
    #app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/entry.py



```python
%exec_py3 src/entry.py
```

>单选按钮 Radiobutton

一般是几个里面选一个用

直接看代码:




```python
%%writefile src/radiobutton.py

from tkinter import Frame,Label,Button,Radiobutton

    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #窗口大小位置
        self.master.geometry("600x400+100+400")#长x宽+x+y
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!\n')
        self.helloLabel.pack()

        self.c1 = Radiobutton(self,text = "1",command = lambda : self.helloLabel.config(
                                                                text = "1被选中了奇数次\n") )
        self.c1.pack()
        self.c2 = Radiobutton(self,text = "2",command = lambda : self.helloLabel.config(
                                                                text = "2被选中了奇数次\n") )
        self.c2.pack()
        self.quitButton = Button(self, text='Quit',fg="red", command=self.quit)
        self.quitButton.pack()

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')

    app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/radiobutton.py



```python
%exec_py3 src/radiobutton.py
```

>复选框 Checkbutton 

复选框通常是用来选择信息的时候的一种选择,它前面 有个小正方形的方块,如果选中则有一个对号,也可以再 次点击以取消该对号来取消选中。

看个例子




```python
%%writefile src/checkbutton.py
from tkinter import Frame,Label,Button,Checkbutton
    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #窗口大小位置
        self.master.geometry("600x400+100+400")#长x宽+x+y
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!\n')
        self.helloLabel.pack()

        self.c1 = Checkbutton(self,
                              text = "1",
                              command = lambda : self.helloLabel.config(
                                  text = self.helloLabel["text"]+"1被选中了奇数次\n"))
        self.c1.pack()
        self.c2 = Checkbutton(self,
                              text = "2",
                              command = lambda : self.helloLabel.config(
                                  text = self.helloLabel["text"]+"2被选中了奇数次\n"))
        self.c2.pack()
        self.quitButton = Button(self, text='Quit',fg="red", command=self.quit)
        self.quitButton.pack()

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')

    app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/checkbutton.py



```python
%exec_py3 src/checkbutton.py
```

>文本域 Text

也就是用来存放字符串的大空间

基本的定义也就是宽度width和高度height了



```python
%%writefile src/text.py

from tkinter import *

    
root = Tk()

text = Text(root)
text.pack()

# INSERT 索引表示插入光标当前的位置
text.insert(INSERT, "I love ")
text.insert(END, "Python!")

mainloop()
```

    Overwriting src/text.py



```python
%exec_py3 src/text.py
```

> 画布 Canvas

和html5中的画布一样,tk中的画布也是用来绘图的,直接看代码吧:




```python
%%writefile src/canvas.py

from tkinter import Frame,Canvas

    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.can = Canvas(self,width = 400,height=300,bg = "#233333")
        self.can.create_line((0,0),(200,200),width = 8)
        self.can.create_text(300,30,text = "一个画板")
        self.can.pack()
if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/canvas.py



```python
%exec_py3 src/canvas.py
```

> 多窗口 Toplevel


```python
%%writefile src/toplevel.py
from tkinter import Frame,Label,Button,Toplevel

    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #窗口大小位置
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world1!')

        self.helloLabel.pack()
class App2(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world2!')
        self.helloLabel.pack()

if __name__ =="__main__":
    app1 = Application()
    # 设置窗口标题:
    app1.master.title('Hello World1')
    app1.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app2 = App2()
    app2.title("helloword2")
    app1.mainloop()
```

    Overwriting src/toplevel.py



```python
%exec_py3 src/toplevel.py
```

>菜单 Menu

Menu 和其他的组件一样,第一个是 parent,这里通常可以为窗口。

然后我们可以用 add_commmand 方法来为它添加菜单项, 如果该菜单是顶层菜单,则添加的菜单项依次向右添加。 如果该菜单时顶层菜单的一个菜单项,则它添加的是下拉菜单的菜单项。
add_command 中的参数常用的有:

+ label 属性,用来指定的是菜单项的名称
+ command 属性用来指定被点击的时候调用的方法
+ acceletor 属性指定的是快捷键 
+ underline 属性 是是否拥有下划线。

最后可以用窗口的 menu 属性指定我们使用哪一个作为它 的顶层菜单.

>>子菜单

如果有子菜单,我们需则需要使用 add_cascade

cascade 可以理解为“级联”,即它 的作用只是为了引出后面的菜单。

add_cascade属性:

+ menu 属性,它指明了要把那个菜单级联到该菜单项上
+ label 属性,用于指定该菜单项的名称。


>>弹出菜单

一般弹出菜单是右键点击后出现的菜单,tk中的弹出菜单比较原始的,具体思路是这样:

+ 我们先新建一个菜单,
+ 然后向菜单项中添加各种功能,
+ 最后我们监听鼠标右键消息,如果是鼠标 右键被单击,
+ 此时可以根据需要判断下鼠标位置来确定是哪个弹出菜单被弹出,
+ 然后使用 Menu 类的 pop 方法来弹出 菜单。

Menu 类里面有一个post方法,它接收两个参数,即 x 和 y 坐标,它会在相应的位置弹出菜单。

>> 插入分割线

    .add_separator()
    
>> 插入单选菜单和复选菜单

单选菜单:

    .add_radiobutton() 
    
复选菜单:
    
    .add_checkbutton()

例子: 一个菜单栏


```python
%%writefile src/menu.py

from tkinter import Frame,Label,Button,Menu

    
class Application(Frame):
    def __init__(self, master=None,):
        Frame.__init__(self, master)
        #窗口大小位置
        self.pack()
        self.createWidgets()
        self.creatMenu()


    def creatMenu(self):
        #主菜单
        menubar = Menu(self)
        #子菜单
        menufile = Menu(menubar)
        for item in ["新建","打开","保存","另存为"]:
            menufile.add_radiobutton(label = item)
        menuedit = Menu(menubar)
        for item in ["复制","黏贴","剪切"]:
            menuedit.add_checkbutton(label = item)
        #子菜单与主菜单关联
        for name,submenu in zip(["文件","编辑"],[menufile,menuedit]):
            menubar.add_cascade(label=name,menu=submenu)
        #最关键的一步,主菜单与app关联
        self.master.config(menu=menubar)
        #右键菜单
        menu = Menu(self.master)
        for i in ('One', 'Two', 'Three'):
            menu.add_command(label=i)
        #插入分割线
        menu.add_separator()

        for i in ('1', '2', '3'):
            menu.add_command(label=i)
        #绑定鼠标右键呼出
        if (self.master.tk.call('tk', 'windowingsystem')=='aqua'):
            self.master.bind('<2>', lambda e: menu.post(e.x_root, e.y_root))
            self.master.bind('<Control-1>', lambda e: menu.post(e.x_root, e.y_root))
        else:
            self.master.bind('<3>', lambda e: menu.post(e.x_root, e.y_root))



    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!')
        self.helloLabel["background"] ="green"
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit',fg="red", command=self.quit)
        self.quitButton.pack()




if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')
    #app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/menu.py



```python
%exec_py3 src/menu.py
```

>对话框 Dialog 和消息盒子 messagebox

>>对话框

对话框就是那个点击以后跳出来的框框,让你选几个选项,选完给程序一个返回值,一般用来做问卷调查呀啥的,我们拿原来登录界面做做修改,把账号密码错误提示弄成对话框


```python
%%writefile src/dialog.py

from tkinter import Frame,Label,Button,Entry
from tkinter.dialog import Dialog
    

    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.userLabel = Label(self, text='用户名:')
        self.userLabel.grid(row = 0,column = 0,sticky="w")
        self.userEntry = Entry(self)
        self.userEntry.grid(row = 0,column = 1,sticky="e")
        self.pwLabel = Label(self, text='密码:')
        self.pwLabel.grid(row = 1,column = 0,sticky="w")
        self.pwEntry = Entry(self)
        self.pwEntry.grid(row = 1,column = 1,sticky="e")

        self.enterButton = Button(self,text = "登录",command = self.reg)
        self.enterButton.grid(row = 2,column = 1,sticky = "e")

        self.logLabel = Label(self, text='')
        self.logLabel.grid(row = 3)

    def reg(self):
        s1 = self.userEntry.get()
        s2 = self.pwEntry.get()
        if s1 == "www.google.com" and s2 == "www.bing.com":
            self.logLabel["text"]="登录成功"
        else:
            self.logLabel["text"]="用户名或密码错误"
            self.userEntry.delete(0,len(s1))
            self.pwEntry.delete(0,len(s1))
            d = Dialog(None,title = "错误信息",text = "用户名或密码错误",
                default=0,strings = ("重来","放弃"))

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('登录界面')
    #窗口大小位置
    #app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/dialog.py



```python
%exec_py3 src/dialog.py
```

>>消息盒子

消息盒子就是提示错误的那种弹窗,同样的还拿那个改


```python
%%writefile src/messagebox.py


from tkinter import Frame,Label,Button,Entry
from tkinter.messagebox import showinfo
    

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.userLabel = Label(self, text='用户名:')
        self.userLabel.grid(row = 0,column = 0,sticky="w")
        self.userEntry = Entry(self)
        self.userEntry.grid(row = 0,column = 1,sticky="e")
        self.pwLabel = Label(self, text='密码:')
        self.pwLabel.grid(row = 1,column = 0,sticky="w")
        self.pwEntry = Entry(self)
        self.pwEntry.grid(row = 1,column = 1,sticky="e")

        self.enterButton = Button(self,text = "登录",command = self.reg)
        self.enterButton.grid(row = 2,column = 1,sticky = "e")

        self.logLabel = Label(self, text='')
        self.logLabel.grid(row = 3)

    def reg(self):
        s1 = self.userEntry.get()
        s2 = self.pwEntry.get()
        if s1 == "www.google.com" and s2 == "www.bing.com":
            self.logLabel["text"]="登录成功"
        else:
            self.logLabel["text"]="用户名或密码错误"
            self.userEntry.delete(0,len(s1))
            self.pwEntry.delete(0,len(s1))
            showinfo(title = "错误",message="用户名或密码错误")

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('登录界面')
    #窗口大小位置
    #app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/messagebox.py



```python
%exec_py3 src/messagebox.py
```

## 大小和位置

对于窗口,大小可以通过geometry函数来控制

    'width x height + xoffset + yoffset'

## 控件布局

有3种方式可以为控件布局:

+ pack()
+ grid()
+ place()

>pack()
pack()默认会一个一个从上往下堆叠,但同样也可以接受几个参数

+ side (left,top,right,bottom)
+ fill ( X,Y,BOTH 和 NONE)水平方向填充,竖直方向填充,水平和竖直方向填充和不填充。
+ expand 参数可以是 YES 和 NO
+ anchor (n, ne, e, se, s, sw, w, nw, or center)NESW 表示上右下左以及他们的组合或者是 CENTER(表示中 间)。
+ ipadx 表示的是内边距的 x 方向
+ ipady 表示 的是内边距的 y 方向
+ padx 表示的是外边距的 x 方向
+ pady 表示的是外边距的 y 方向。


```python
%%writefile src/pack.py

from tkinter import Frame,Label,Button


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.LabelL = Label(self, text='左边')
        self.LabelL.pack(side="left")
        self.LabelR = Label(self, text='右边')
        self.LabelR.pack(side="right")
        self.LabelT = Label(self, text='顶')
        self.LabelT.pack(side="top")
        self.LabelB = Label(self, text='底')
        self.LabelB.pack(side="bottom")

        self.LabelN = Label(self, text='N')
        self.LabelN.pack(anchor="n")
        self.LabelE = Label(self, text='E')
        self.LabelE.pack(anchor="e")
        self.LabelS = Label(self, text='S')
        self.LabelS.pack(anchor="s")
        self.LabelW= Label(self, text='W')
        self.LabelW.pack(anchor="w")
        self.LabelCENTER= Label(self, text='CENTER')
        self.LabelCENTER.pack(anchor="center")


        self.quitButton = Button(self, text='Quit',background="red", command=self.quit)
        self.quitButton.pack(side="bottom")

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('pack布局测试')
    #窗口大小位置
    #app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/pack.py



```python
%exec_py3 src/pack.py
```

> grid() 最常用布局

grid()里的参数:

+ row 表示行(从0开始)
+ column 表示列(从0开始)
+ sticky  (N,E,S,W) 表 示上右下左,它决定了这个组件是从哪个方向开始的
+ ipadx,ipady,padx,pady,它们 的意思和 pack 函数是一样的,默认边距是 0。
+ rowspan 表示跨越的行数 columnspan 表示跨越的列数。


```python
%%writefile src/grid.py

from tkinter import Frame,Label,Button


    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.Label00 = Label(self, text='00')
        self.Label00.grid(row=0,column=0)
        self.Label10 = Label(self, text='10')
        self.Label10.grid(row=1,column=0)
        self.Label11 = Label(self, text='11')
        self.Label11.grid(row=1,column=1)
        self.Label30 = Label(self, text='30')
        self.Label30.grid(row=3,column=0)


        self.quitButton = Button(self, text='Quit',background="red", command=self.quit)
        self.quitButton.grid(row=2,column=2)

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('pack布局测试')
    #窗口大小位置
    #app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/grid.py



```python
%exec_py3 src/grid.py
```

> place() 最好不要用....不优雅

## 事件

> 事件绑定和解绑 bind() unbind()
>>绑定bind()

bind 函数的调用规则: 

    窗体对象.bind(事件类型,回调函数)

事件类型:

事件类型是一组字符串,它采用的描述方式是这 样的:

    <MODIFIER-MODIFIER-TYPE-DETAIL>
    
+ MODIFIER 即修饰符,它的全部取值如下:

Control|Mod1, M1, Command
---|---
Alt|Mod2, M2, Option
Shift|Mod3, M3
Lock|Mod4, M4
Extended|Mod5, M5
Button1, B1|Meta, M
Button2, B2|Double
Button3, B3|Triple
Button4, B4|Quadruple
Button5, B5|---



+ TYPE 表示类型,它的全部取值如下:

Activate|Destroy|Map
---|---|---
ButtonPress, Button|Enter|MapRequest
ButtonRelease|Expose|Motion
Circulate|FocusIn|MouseWheel
CirculateRequest|FocusOut|Property
Colormap|Gravity|Reparent
Configure|KeyPress, Key|ResizeRequest
ConfigureRequest|KeyRelease|Unmap
Create|Leave|Visibility
Deactivate|---|---



+ DETAIL 表示细节,其实也就是对第二个参数的一些辅助说明。
    
常用事件类型:

+ `<Button-1>` 表示鼠标左键单击,其中的 1 换成 3 表示右 键被单击,为 2 的时候表示鼠标中键
+ `<KeyPress-A>` 表示 A 键被按下,其中的 A 可以换成其他的键位。
+ `<Control-V>` 表示按下的是 Ctrl 和 V 键,V 可以换成其他 键位。
+ `<F1>`表示按下的是 F1 键,对于 Fn 系列的,都可以随便 换。

更加具体的可以看<http://www.tcl.tk/man/tcl8.5/TkCmd/bind.htm#M23>

bind()可以绑定所有继承自Misc类的组件,也就是说即便是标签也可以绑定动作.

bind()有两个扩展


+ 窗体对象.bind_all(事件类型,回调函数)全程序级别绑定事件

+ 窗体对象.bind_class(类名,事件类型,回调函数)类级别绑定事件,比如所有标签这样

>> 解绑 unbind()

窗体对象.unbind(事件类型)

## ttk

ttk是tk的扩展,主要是美化和新增了几个控件

还是看例子:



```python
%%writefile src/ttk.py

from tkinter import *
from tkinter.ttk import *


    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #窗口大小位置
        self.master.geometry("600x400+100+400")#长x宽+x+y
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!')

        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')

    app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/ttk.py



```python
%exec_py3 src/ttk.py
```

## gui 界的 helloworld, 一个记事本


```python
%%writefile src/editer.py

import os

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *



    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #窗口大小位置
        self.master.geometry("600x400+100+400")#长x宽+x+y
        self.pack()
        self.filename = ""
        self.creatMenu()
        self.createWidgets()

    def creatMenu(self):
        #主菜单
        menubar = Menu(self)
        #子菜单
        menufile = Menu(menubar)
        menufile.add_command(label = "打开",accelerator = "Ctrl + O",command = self.myopen)
        menufile.add_command(label = "新建",accelerator = "Ctrl + N",command = self.new)
        menufile.add_command(label = "保存",accelerator = "Ctrl + S",command = self.save)
        menufile.add_command(label = "另存为",accelerator = "Ctrl + Shift + S",command = self.saveas)

        menuedit = Menu(menubar)
        menuedit.add_command(label = "剪切",accelerator = "Ctrl + X",command = self.cut)
        menuedit.add_command(label = "复制",accelerator = "Ctrl + C",command = self.copy)
        menuedit.add_command(label = "黏贴",accelerator = "Ctrl + V",command = self.paste)
        menuedit.add_separator()
        menuedit.add_command(label = "全选",accelerator = "Ctrl + A",
                             command = lambda :self.textPad.tag_add('sel',1.0,"end"))

        menuaboutme = Menu(menubar)
        menuaboutme.add_command(label = "作者",command = self.author)
        menuaboutme.add_command(label = "版权",command = self.power)

        #子菜单与主菜单关联
        for name,submenu in zip(["文件","编辑","关于"],[menufile,menuedit,menuaboutme]):
            menubar.add_cascade(label=name,menu=submenu)
        #最关键的一步,主菜单与app关联
        self.master.config(menu=menubar)
        #右键菜单
        menu = Menu(self.master)
        menu.add_command(label = "剪切",command = self.cut)
        menu.add_command(label = "复制",command = self.copy)
        menu.add_command(label = "黏贴",command = self.paste)
        #绑定鼠标右键呼出
        if (self.master.tk.call('tk', 'windowingsystem')=='aqua'):
            self.master.bind('<2>', lambda e: menu.post(e.x_root, e.y_root))
            self.master.bind('<Control-1>', lambda e: menu.post(e.x_root, e.y_root))
        else:
            self.master.bind('<3>', lambda e: menu.post(e.x_root, e.y_root))

    def createWidgets(self):

        self.shortcutbar = Frame(self,height = 25,bg = "light sea green")
        self.shortcutbar.pack(expand = NO,fill =X)

        self.lnlabel = Label(self,width = 2,bg = "antique white")
        self.lnlabel.pack(side = LEFT,anchor = 'nw',fill = Y)

        self.textPad = Text(self,bg = "antique white")
        self.textPad.pack()
        self.textPad.insert(INSERT,"Hello")
        self.textPad.insert(END,"world")


        self.textPad.bind("<Control-N>",self.new)
        self.textPad.bind("<Control-n>",self.new)
        self.textPad.bind("<Control-O>",self.myopen)
        self.textPad.bind("<Control-o>",self.myopen)
        self.textPad.bind("<Control-S>",self.save)
        self.textPad.bind("<Control-s>",self.save)
        self.textPad.bind("<Control-A>",lambda : self.textPad.tag_add('sel',1.0,"end"))
        self.textPad.bind("<Control-a>",lambda : self.textPad.tag_add('sel',1.0,"end"))

    def  myopen(self):
        self.filename = askopenfilename(defaultextension = ".txt")
        if self.filename == "":
            self.filename = None
        else:
            self.master.title("一个记事本"+os.path.basename(self.filename))
            self.textPad.delete("1.0","end")
            with open(self.filename,"r") as f:
                s = f.read()
                self.textPad.insert("1.0",s)

    def new(self):
        self.master.title("未命名文件")
        self.filename = None
        self.textPad.delete("1.0",END)

    def save(self):
        try:
            with open(self.filename,"w") as f:
                msg = self.textPad.get(1.0,"end")
                f.write(msg)
        except :
            self.saveas()

    def saveas(self):
        f = asksaveasfilename(initialfile = "未命名. txt",defaultextension = ".txt")
        self.filename = f
        with open(f,"w") as fh:
            msg = self.textPad.get(1.0,"end")
            fh.write(msg)
        self.master.title("一个记事本"+os.path.basename(f))

    def cut(self):
        self.textPad.event_generate("<<Cut>>")

    def copy(self):
        self.textPad.event_generate("<<Copy>>")

    def paste(self):
        self.textPad.event_generate("<<Paste>>")

    def author(self):
        self.shouinfo("作者黄思喆")

    def power(self):
        self.showinfo("本软件使用BSD许可证")


if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('一个记事本')

    #app.master.geometry("300x300+100+100")#长x宽+x+y
    # 主消息循环:
    app.mainloop()
```

    Overwriting src/editer.py



```python
%exec_py3 src/editer.py
```
