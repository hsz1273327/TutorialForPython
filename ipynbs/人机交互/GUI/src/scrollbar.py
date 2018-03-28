from tkinter import Tk,Scrollbar,Listbox
master = Tk()
scrollbar = Scrollbar(master)
scrollbar.pack(side='right', fill='y')

listbox = Listbox(master, yscrollcommand=scrollbar.set)
for i in range(1000):
    listbox.insert('end', str(i))
listbox.pack(side='left', fill='both')

scrollbar.config(command=listbox.yview)

master.mainloop()