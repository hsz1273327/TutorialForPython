
from tkinter import Frame,Label,Button


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.LabelL = Label(self, text='左边')
        self.LabelL.pack(side="left")
        self.LabelR = Label(self, text='右边')
        self.LabelR.pack(side="right")
        self.LabelT = Label(self, text='顶')
        self.LabelT.pack(side="top")
        self.LabelB = Label(self, text='底')
        self.LabelB.pack(side="bottom")

        self.LabelN = Label(self, text='N')
        self.LabelN.pack(anchor="n")
        self.LabelE = Label(self, text='E')
        self.LabelE.pack(anchor="e")
        self.LabelS = Label(self, text='S')
        self.LabelS.pack(anchor="s")
        self.LabelW= Label(self, text='W')
        self.LabelW.pack(anchor="w")
        self.LabelCENTER= Label(self, text='CENTER')
        self.LabelCENTER.pack(anchor="center")


        self.quitButton = Button(self, text='Quit',background="red", command=self.quit)
        self.quitButton.pack(side="bottom")

if __name__ =="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('pack布局测试')
    #窗口大小位置
    #app.master.geometry("600x400+100+400")#长x宽+x+y
    # 主消息循环:
    app.mainloop()