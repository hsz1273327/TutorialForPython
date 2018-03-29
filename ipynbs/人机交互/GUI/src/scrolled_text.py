from tkinter import Tk,END
from tkinter.scrolledtext import ScrolledText
root = Tk()
stext = ScrolledText(root,bg='white', height=10)
stext.pack(fill="both", side="left", expand=True)
stext.focus_set()
root.mainloop()