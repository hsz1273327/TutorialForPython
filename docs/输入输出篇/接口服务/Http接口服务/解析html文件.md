
# html的jQuery式解析(pyquery)

python上也有类似jQuery的html解析包,就是题目的名字了[官网在这边](https://github.com/gawel/pyquery)

安装:

    pip install pyquery
    
注意:pypy上安装需要下载下来然后修改依赖,把lxml改成lxml-cffi,然后再用

    pypy setup.py install 
    
    
安装.并且html内容必须把unicode转码成str才可以


```python
from pyquery import PyQuery as pq
```


```python
from requests import get
```


```python
d = pq("<html><div id='1'><p>hello</p></div></html>")
```


```python
print(d("#1").text())
```

    hello



```python
s = get("http://pyquery.readthedocs.org/en/latest/").text
```


```python
html=pq(s.encode("utf-8"))
```

## 获取html内容
除了上面的方式通过requests获取html内容外,pyquery也内置了直接获取html文本的方法

+ 构造函数添加关键字参数url就可以从web上获取html文本
+ 构造函数添加关键字参数filename就可以从本地文件系统上获取html文本


```python
html = pq(url="http://pyquery.readthedocs.org/en/latest/")
```


```python
html.html()[:100]
```




    '\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n    \n    <title>'



## 选择器

pyQuery与jquery的选择器规则相同,假设我们的pyquery实例名与jquery一致为`$`,这样给他一个参数他就可以进行查找工作

所有的查找返回的都是一个pyQuery对象,pyQuery对象类似数组，它的每个元素都是一个引用了DOM节点的对象,如果一个都没找到,那就返回一个空的jQuery对象

表达式|说明
---|---
`$('#a')`|找到id是a的节点,并返回一个jQuery对象
`$('.a')`|找到class是a的节点
`$('a')`|找到<a>节点
`$('[name=a]')`|找到有属性name是a的节点,当属性中包含特殊字符时则用双引号引起来
`$('[name^=a]')`|找到有属性name是以a开头的节点
`$('[name$=a]')`|找到有属性name是以a结尾的节点

### 选择器可以组合,

比如:

    $('p[name=a]')
    
是说要找name属性是a的`<p>`标签.各种组合可以随意搭配

### 选择器可以用`,`表示或的关系,从而把符合多种选择条件的都放进去,

比如

    $('p[name^=a],p[name$=a]')
    
表示name属性是以a开头或以a结尾的`<p>`标签

### 选择器可以固定层级

如果两个DOM元素具有层级关系，就可以用`$('ancestor descendant')`来选择，层级之间用空格隔开。

比如:

    $('div[name=a1] p[name$=a]')
    
表示在name属性是a1的div标签中的所有name属性是以a结尾的p标签


也可以用自选择器`$('parent>child')`来做选择

自选择器固定了层级关系是父子关系,也就是一个节点必须是拎一个的直属子节点

    $('div[name=a1]>p[name$=a]')

## 过滤器

过滤器用来过滤由选择器选出来的节点,用`:`表示过滤器


常用的普通标签的过滤器:


过滤器|说明
---|---
`$('ul.lang li:first-child')`|仅选出第一个
`$('ul.lang li:last-child')`| 仅选出最后一个
`$('ul.lang li:nth-child(2)')`| 选出第N个元素，N从1开始
`$('ul.lang li:nth-child(even)')`| 选出序号为偶数的元素
`$('ul.lang li:nth-child(odd)')`| 选出序号为奇数的元素
`$('div:visible')`| 所有可见的div
`$('div:hidden')`| 所有隐藏的div


常用的表单的过滤器:

过滤器|说明
---|---
input|可以选择`<input>，<textarea>，<select>和<button>`
file|可以选择`<input type="file">`，和`input[type=file]`一样
checkbox|可以选择复选框，和`input[type=checkbox]`一样
radio|可以选择单选框，和`input[type=radio]`一样
focus|可以选择当前输入焦点的元素，例如把光标放到一个`<input>`上，用`$('input:focus')`就可以选出
checked|选择当前勾上的单选框和复选框，用这个选择器可以立刻获得用户选择的项目
enabled|可以选择可以正常输入的`<input>、<select>`等，也就是没有灰掉的输入
disabled|和:enabled正好相反，选择那些不能输入的


```python
for i in html("a"):
    print((i.text if i.text else "") + ":" +i.get("href"))
```

    index:genindex.html
    modules:py-modindex.html
    next:attributes.html
    pyquery 1.2.10.dev0 documentation:#
    Â¶:#pyquery-a-jquery-like-library-for-python
    project:https://github.com/gawel/pyquery/
    github:https://github.com/gawel/pyquery/issues
    Â¶:#quickstart
    Â¶:#full-documentation
    Attributes:attributes.html
    CSS:css.html
    Using pseudo classes:pseudo_classes.html
    Manipulating:manipulating.html
    Traversing:traversing.html
    :api.html
    Scraping:scrap.html
    :ajax.html
    Tips:tips.html
    Testing:testing.html
    Future:future.html
    News:changes.html
    Â¶:#more-documentation
    here:http://pyquery.rtfd.org/
    jquery website:http://docs.jquery.com/
    color cheat sheet:http://colorcharge.com/wp-content/uploads/2007/12/jquery12_colorcharge.png
    code:https://github.com/gawel/pyquery
    Â¶:#indices-and-tables
    :genindex.html
    :py-modindex.html
    :search.html
    Table Of Contents:#
    pyquery: a jquery-like library for python:#
    Quickstart:#quickstart
    Full documentation:#full-documentation
    More documentation:#more-documentation
    Indices and tables:#indices-and-tables
    Attributes:attributes.html
    Show Source:_sources/index.txt
    index:genindex.html
    modules:py-modindex.html
    next:attributes.html
    pyquery 1.2.10.dev0 documentation:#
    Sphinx:http://sphinx-doc.org/



```python
html("a.internal").map(lambda i,e : print(pq(e).text()))
```

    Attributes
    CSS
    Using pseudo classes
    Manipulating
    Traversing
    pyquery – PyQuery complete API
    Scraping
    pyquery.ajax – PyQuery AJAX extension
    Tips
    Testing
    Future
    News
    Index
    Module Index
    Search Page
    pyquery: a jquery-like library for python
    Quickstart
    Full documentation
    More documentation
    Indices and tables





    []


