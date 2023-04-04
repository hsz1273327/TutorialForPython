
from tkinter import Frame,Canvas

    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.can = Canvas(self,width = 400,height=300,bg = "#233333")
        self.can.create_line((0,0),(200,200),width = 8)
        self.can.create_text(300,30,text = "一个画板")
        self.can.pack()
if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')
    # 主消息循环:
    app.mainloop()