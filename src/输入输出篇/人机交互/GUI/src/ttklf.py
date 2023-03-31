
#coding:utf-8
from tkinter.ttk import LabelFrame,Label,Button,Style

style = Style()
style.configure("RW.TLabel", foreground="red", background="white")

class Application(LabelFrame):
    def __init__(self, master=None):
        super().__init__(master)
        #窗口大小位置
        self.master.geometry("600x400+100+400")#长x宽+x+y
        self.pack()
        self.createWidgets()
        self.config(text="test_text",labelanchor="w")

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!')
    
        self.helloLabel.pack()
        self.quitButton = Button(self,text='Quit',style="RW.TLabel",command=self.quit)
        self.quitButton.pack()

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')

    app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()