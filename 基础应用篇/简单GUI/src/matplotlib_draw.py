import datetime
from tkinter import Tk,Button
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
import tushare as ts

mpl.use('TkAgg')

def date_to_num(dates):
    num_time = []
    for date in dates:
        date_time = datetime.datetime.strptime(date,'%Y-%m-%d')
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time

def plot(mat_wdyx):
    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(15,8))
    mpf.candlestick_ochl(ax1, mat_wdyx, width=1.0, colorup = 'g', colordown = 'r')
    ax1.set_title('wandayuanxian')
    ax1.set_ylabel('Price')
    ax1.grid(True)
    ax1.xaxis_date()
    plt.bar(mat_wdyx[:,0]-0.25, mat_wdyx[:,5], width= 0.5)
    ax2.set_ylabel('Volume')
    ax2.grid(True)
    return fig

def main():
    wdyx = ts.get_k_data('002739','2017-01-01')
    mat_wdyx = wdyx.as_matrix()
    num_time = date_to_num(mat_wdyx[:,0])
    mat_wdyx[:,0] = num_time
    f = plot(mat_wdyx)
    
    root = Tk()
    
    canvas =FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    toolbar =NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side="top", fill="both", expand=1)
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
    root.mainloop()

if __name__=="__main__":
    main()