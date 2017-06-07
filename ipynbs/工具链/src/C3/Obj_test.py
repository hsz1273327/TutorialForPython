#encoding=utf-8  
import objgraph  
  
if __name__ == '__main__':  
    x = []  
    y = [x, [x], dict(x=x)]  
    objgraph.show_refs([y], filename='sample-graph.png') #把[y]里面所有对象的引用画出来  
    objgraph.show_backrefs([x], filename='sample-backref-graph.png') #把对x对象的引用全部画出来  
    #objgraph.show_most_common_types() #所有常用类型对象的统计，数据量太大，意义不大  
    objgraph.show_growth(limit=4) #打印从程序开始或者上次show_growth到现在增加的对象（按照增加量的大小排序）  