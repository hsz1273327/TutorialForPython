
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