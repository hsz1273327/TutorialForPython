
# `*`notebook格式转换工具(nbconvert)

`nbconvert`是`jupyter notebook`的格式转换工具,它支持把`notebook`转化为`markdown,pdf,html`等格式的文件

它依赖`pandoc`,所以先要安装`pandoc`,另外如果要转成pdf格式,还要安装latex和一些依赖

    sudo tlmgr install ucs  
    sudo tlmgr install collectbox
    sudo tlmgr install adjustbox 
    sudo tlmgr install cyrillic
    sudo tlmgr install collection-langcyrillic
    
之后要使用`nbconvert`只需要:
```shell
jupyter nbconvert --to <output format> <input notebook>
```

input notebook 可以使用通配符来指定复数的`.ipynb`文件

常用的格式有:

+ html 通用的网页格式
+ markdown markdown文本格式
+ reStructuredText .rst后缀的文本,sphinx的通用格式
+ script 提取文件中的代码并保存为对应格式

