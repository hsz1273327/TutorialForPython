from tkinter import Tk

win = Tk()
win.title("first window")
win.iconbitmap(r"C:\Users\87\Documents\GitHub\my\TutorialForPython\ipynbs\人机交互\GUI\src\myredis.ico")
win.geometry("600x400+100+400")
win.configure(background="Blue")
win.attributes('-alpha',0.5)
win.mainloop()