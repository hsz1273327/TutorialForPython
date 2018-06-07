from tkinter import Tk,Message

master = Tk()

w = Message(master, text="this is a message")
w.pack()

master.mainloop()