
from tkinter import Frame,Label,Button,Radiobutton, IntVar

    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #窗口大小位置
        self.master.geometry("600x400+100+400")#长x宽+x+y
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        self.var = IntVar()
        self.helloLabel = Label(self, text='Hello, world!\n')
        self.helloLabel.pack()
        self.rbframe=Frame(self)
        self.rbframe.pack()
        self.c1 = Radiobutton(
            self.rbframe,
            indicatoron=False,
            text = "1",
            value=1,
            variable=self.var,
            command = self._callback
        )
        self.c1.pack()
        self.c2 = Radiobutton(
            self.rbframe,
            indicatoron=False,
            text = "2",
            value=2,
            variable=self.var,
            command = self._callback
        )
        self.c2.pack()
        self.quitButton = Button(self, text='Quit',fg="red", command=self.quit)
        self.quitButton.pack()
        
    def _callback(self):
        self.helloLabel.config(text = "值为{}".format(self.var.get()))

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')

    app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()