
from tkinter import Frame,Label,Button,Menu

    
class Application(Frame):
    def __init__(self, master=None,):
        Frame.__init__(self, master)
        #窗口大小位置
        self.pack()
        self.createWidgets()
        menu = self.creatMenu()
        self.master.config(menu=menu)


    def creatMenu(self):
        #主菜单
        menubar = Menu(self.master)
        #子菜单
        menufile = Menu(menubar)
        #多选菜单
        menuradio = Menu(menubar)
        #单选菜单
        menucheck = Menu(menubar)
        for item in ["1","2","3","4"]:
            menufile.add_command(label = item)
        menubar.add_cascade(label = "子菜单",menu=menufile)
        for i in ["a","b","c"]:
            menuradio.add_radiobutton(label = i)
        menubar.add_cascade(label = "多选菜单",menu=menuradio)
        for i in ["a1","b2","c3"]:
            menucheck.add_checkbutton(label = i)
        menubar.add_cascade(label = "单选菜单",menu=menucheck)
        return menubar


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
    app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()