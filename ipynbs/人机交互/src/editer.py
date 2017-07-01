
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