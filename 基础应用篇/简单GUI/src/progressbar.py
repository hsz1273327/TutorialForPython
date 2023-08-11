from tkinter import *  
from tkinter import ttk  
import time  
  
def manu_increment(*args):  
    for i in range(100):  
        p1["value"] = i+1  
        root.update()  
        time.sleep(0.1)
    
def auto_increment(*args):  
    global flag,value  
    flag = not flag  
  
    if flag:  
        btn2["text"] = "暂停动画"  
        p2.start(10)  
    else:  
        btn2["text"] = "开始动画"  
        value = p2["value"]  
        p2.stop()  
        p2["value"] = value
root = Tk()  
root.title("Progressbar组件")
sg = ttk.Sizegrip(root).grid(row=99,column=99,sticky="se")
# 定量进度条 
p1 = ttk.Progressbar(root, length=200, mode="determinate", orient=HORIZONTAL)  
p1.grid(row=1,column=1)  
p1["maximum"] = 100  
p1["value"] = 0  
  
# 通过指定变量，改变进度条位置  
# n = IntVar()  
# p1["variable"] = n  
  
# 通过指定步长，改变进度条位置  
# p1.step(2)  
  
btn = ttk.Button(root,text="开始动画",command=manu_increment)  
btn.grid(row=1,column=0)  
  
# 非定量进度条  
flag = False   # 标志位  
value = 0      # 进度条位置  

# 分隔
sep = ttk.Separator(root)
sep.grid(sticky = "ew")  

p2 = ttk.Progressbar(root, length=200,orient = HORIZONTAL)  
p2.grid(row=3,column=1)  
  
btn2 = ttk.Button(root,text="自动动画",command=auto_increment)  
btn2.grid(row=3,column=0)  
  
root.mainloop()  