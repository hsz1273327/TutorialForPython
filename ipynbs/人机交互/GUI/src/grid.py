
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