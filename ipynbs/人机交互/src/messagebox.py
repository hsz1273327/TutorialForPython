

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