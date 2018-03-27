
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
        for item in ["新建","打开","保存","另存为"]:
            menubar.add_command(label = item)
        for item in ["1","2","3","4"]:
            menufile.add_command(label = item)
            menufile.add_separator()
        menubar.add_cascade(label = "子菜单",menu=menufile)
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