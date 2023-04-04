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