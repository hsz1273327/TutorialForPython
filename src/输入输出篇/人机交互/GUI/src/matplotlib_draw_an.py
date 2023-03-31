import datetime
from tkinter import Tk,Button,IntVar
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg





def plot(i):
    fig, ax = plt.subplots()
    x = np.arange(0, 2*np.pi, 0.01)
    line, = ax.plot(x, np.sin(x+ i/10.0))
    return fig,ax


    

def main():
    
    root = Tk()
    I = 0
    f,ax = plot(I)
    canvas =FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
    toolbar =NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side="top", fill="both", expand=1)
    def callback():
        nonlocal I
        ax.clear()
        x = np.arange(0, 2*np.pi, 0.01)
        line, = ax.plot(x, np.sin(x+ I/10.0))
        I+=1
        canvas.draw()
        root.after(200,callback)
        
    
    #canvas.new_timer(interval=200,callbacks=callback)
    #定义并绑定键盘事件处理函数
    def on_key_event(event):
        print('you pressed %s'% event.key)
        key_press_handler(event, canvas, toolbar)
    canvas.mpl_connect('key_press_event', on_key_event)
    
    def _quit():
        #结束事件主循环，并销毁应用程序窗口
        root.quit()
        root.destroy()
    button =Button(master=root, text='Quit', command=_quit)
    button.pack(side="bottom")
    root.after(200,callback)
    root.mainloop()

if __name__=="__main__":
    main()