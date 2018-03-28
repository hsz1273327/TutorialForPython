from tkinter import Tk,Spinbox

master = Tk()

w = Spinbox(master, from_=0, to=10)
w.pack()
master.mainloop()