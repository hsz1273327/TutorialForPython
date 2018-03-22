
#coding:utf-8
from tkinter import Frame,Label,Button


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
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