from tkinter import Tk

win = Tk()
win.title("first window")
win.geometry("600x400+100+400")
win.configure(background="Blue")
win.attributes('-alpha',0.5)
win.mainloop()