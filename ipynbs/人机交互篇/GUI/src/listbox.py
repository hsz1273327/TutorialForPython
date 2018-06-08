
from tkinter import Frame,Listbox,END

    
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.list = Listbox(self)
        self.list.pack()
        self.list.insert(END, "a list entry")
        for item in ["one", "two", "three", "four"]:
            self.list.insert(END, item)
if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')
    # 主消息循环:
    app.mainloop()