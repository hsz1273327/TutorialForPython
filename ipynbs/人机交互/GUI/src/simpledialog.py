
import tkinter
from tkinter import simpledialog

def inputStr():
    r = simpledialog.askstring('Python Tkinter', 'Input String', initialvalue = 'Python Tkinter')
    print(r)
def inputInt():
    r = simpledialog.askinteger('Python Tkinter', 'Input Integer')
    print(r)
def inputFloat():
    r = simpledialog.askfloat('Python Tkinter', 'Input Float')
    print(r)

root = tkinter.Tk()
btn1 = tkinter.Button(root, text='Input String', command=inputStr)
btn2 = tkinter.Button(root, text='Input Integer', command=inputInt)
btn3 = tkinter.Button(root, text='Input Float', command=inputFloat)

btn1.pack(side='left')
btn2.pack(side='left')
btn3.pack(side='left')

root.mainloop()