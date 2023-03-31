
# url分析工具(purl)

url是web上指定内容的地址,它基本可以分为几个部分

+ scheme 协议路径,比如http,https等
+ host 主机名,比如`www.baidu.com`这样
+ path 主机下内容具体所在的路劲
+ query_params 在url中作为参数传入路径的内容

[purl](https://github.com/codeinthehole/purl)是一个简单好用的url分解工具,用它可以方便的获取一段url的各部分内容

安装:

    pip install purl
    
    

使用:


```python
url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=newbee&rsv_pq=c87beda3000c6192&rsv_t=69e1zt6mVNzkBbdJDmwMn6Q%2FanmE7t9awTdR05ddZ2dL0Sxnf9BuLA3TB3g&rsv_enter=1&rsv_sug3=8&rsv_sug1=10&rsv_sug7=100"
```


```python
from purl import URL
```


```python
from_str = URL(url)
```


```python
from_str.scheme()
```




    'https'




```python
from_str.host()
```




    'www.baidu.com'




```python
from_str.query()
```




    'ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=newbee&rsv_pq=c87beda3000c6192&rsv_t=69e1zt6mVNzkBbdJDmwMn6Q%2FanmE7t9awTdR05ddZ2dL0Sxnf9BuLA3TB3g&rsv_enter=1&rsv_sug3=8&rsv_sug1=10&rsv_sug7=100'




```python
from_str.query_params()
```




    {'f': ['8'],
     'ie': ['utf-8'],
     'rsv_bp': ['0'],
     'rsv_enter': ['1'],
     'rsv_idx': ['1'],
     'rsv_pq': ['c87beda3000c6192'],
     'rsv_sug1': ['10'],
     'rsv_sug3': ['8'],
     'rsv_sug7': ['100'],
     'rsv_t': ['69e1zt6mVNzkBbdJDmwMn6Q/anmE7t9awTdR05ddZ2dL0Sxnf9BuLA3TB3g'],
     'tn': ['baidu'],
     'wd': ['newbee']}




```python
from_str.query_param("f")
```




    '8'


