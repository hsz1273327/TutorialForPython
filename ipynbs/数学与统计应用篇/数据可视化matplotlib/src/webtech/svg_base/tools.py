#coding:utf-8

__all__=["draw_k_svg"]

from db import symbol_dict

import matplotlib.pyplot as plt
from matplotlib.finance import quotes_historical_yahoo_ochl
from matplotlib.finance import candlestick_ochl
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter  ,WeekdayLocator,MONDAY,DayLocator
import datetime
import numpy as np

from io import BytesIO
import json

plt.style.use('chinese_support')

def deal_with_svg(f):
    from pyquery import PyQuery as Q
    # Create XML tree from the SVG file.
    value = f.getvalue()
    # Add attributes to the patch objects.

    # Add a transition effect
    result = Q(value)
    return result.__str__()

    return "".join(f.getvalue().split("/n")[4:])

def draw_k_svg(id_str,from_date_str,to_date_str):
    u"""
    Parameters:
        id_str (str): - 6位数的上证股票编号
        from_date_str (str): - '2016-6-20'形式的日期数据,表示起始日期
        to_date_str (str): - '2016-6-20'形式的日期数据,表示结束日期
    Returns:
        str : - svg的字符串内容
    """

    #设置x轴坐标刻度
    mondays = WeekdayLocator(MONDAY)            # 主要刻度
    alldays = DayLocator()                      # 次要刻度

    mondayFormatter = DateFormatter('%m-%d-%Y') # 如：2-29-2015
    dayFormatter = DateFormatter('%d')

    from_date = tuple((int(i) for i in from_date_str.strip().split("-")))
    to_date = tuple((int(i) for i in to_date_str.strip().split("-")))
    quotes_ochl = quotes_historical_yahoo_ochl(id_str+'.ss', from_date ,to_date)

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)

    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(mondayFormatter)


    candlestick_ochl(ax, quotes_ochl, width=0.6, colorup='r', colordown='g')
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    ax.grid(True)
    plt.title(symbol_dict.get(id_str,u"未知"))

    f = BytesIO()
    plt.savefig("ts_o.svg", format="svg")
    plt.savefig(f, format="svg")
    value = f.getvalue()
    result = deal_with_svg(f)
    f.close()
    return result
