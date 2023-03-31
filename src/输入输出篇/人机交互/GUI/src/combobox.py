from tkinter import Tk,StringVar
from tkinter.ttk import Combobox
master = Tk()
number = StringVar()
w = Combobox(master,textvariable=number)
w['values'] = (1, 2, 4, 42, 100)     # 设置下拉列表的值
w.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
w.current(0) 
w.pack()
master.mainloop()