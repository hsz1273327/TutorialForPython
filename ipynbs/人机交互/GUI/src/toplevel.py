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
    app2.geometry("200x200+0+0")#长x宽+x+y
    app1.mainloop()