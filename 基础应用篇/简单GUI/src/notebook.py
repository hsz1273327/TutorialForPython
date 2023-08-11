from tkinter import Tk,PhotoImage
from tkinter.ttk import Notebook,Frame,Button


root = Tk()

scheduledimage=PhotoImage("source/canvas.png")
note = Notebook(root)

tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
Button(tab1, text='Exit', command=root.destroy).pack(padx=100, pady=100)
note.add(tab1, text = "Tab One",image=scheduledimage, compound="top")
note.add(tab2, text = "Tab Two")
note.add(tab3, text = "Tab Three")
note.pack()
root.mainloop()