# `*`自定义WrapperKernel

使用[ipykernel](https://github.com/ipython/ipykernel)来自定义一个WrapperKernel是最简单的一种自建jupyter kernel的方式.这个包是基础,但实话说没有很好用,另一个第三方包[metakernel](https://github.com/Calysto/metakernel)是对它的封装,它自动提供了安装核心的功能.我们只要使用如下项目结构构造项目就可以了.

```bash
|--项目名\
|       |--images\
|       |         |--logo-32x32.png
|       |         |--logo-64x64.png
|       |         |--logg-svg.svg
|       |
|       |--kernel.json
|       |--kernel.py
|       |--__main__.py
|       |--__init__.py
|
|--pyproject.toml
```

其中

+ `images`放置要复制到核心文件夹的图片;
+ `kernel.json`放置要复制到核心文件夹的配置文件
+ `kernel.py`中放置一个继承了`metakernel.MetaKernel`的类,我们需要实现其中如下属性或方法:
    + `magic_prefixes:Dict[str,str]`[可选],默认为`dict(magic='%', shell='!', help='?')`
    + `help_suffix:str`[可选]默认为`?`
    + `language_info:LanguageInfoDictType`[可选]返回语言信息,其中`LanguageInfoDictType`结构为
        ```python
        TypedDict(
            'LanguageInfoDictType',
            {
                'mimetype': str,
                'name': str,
                'file_extension': str,
                'version': str,
                'help_links': List[HelpLinkDictType]
            },
            total=False
        )
        TypedDict(
            'HelpLinkDictType',
            {
                "text": str,
                "url": str
            },
            total=False
        )
        ```
    + `get_usage()`[可选]用法说明信息
    + `handle_plot_settings()`[可选]处理画图设置
    + `get_local_magics_dir()`[可选]返回魔法命令保存路径,默认为`~/.ipython/metakernel/magics`
    + `get_kernel_help_on(info: Mapping[str, str], level: int = 1, none_on_fail: bool = False) -> Optional[str]`,[可选]获取核心帮助信息
    + `do_execute_direct(self, code: str, silent: bool = False) -> Optional[Union[RowsDisplay, ExceptionWrapper]]`,执行指令
    + `do_execute_meta(self, code: str) -> ExceptionWrapper`,[可选]执行元指令
    
   

+ `__main__.py`中固定写上
    ```python
    from .kernel import 你的Kernel类名
    
    if __name__ == '__main__':
        你的Kernel类名.run_as_main()
    ```

使用这种方式构造的核心程序都可以只用`python -m 项目名 install`的方式安装核心.


## 自定义WrapperKernel的魔法命令.

使用`metakernel`定义的自定义WrapperKernel会默认加载[`metakernel`定义的自带魔法命令](https://github.com/Calysto/metakernel/blob/main/metakernel/magics/README.md).这些命令基本和ipython自带的一致.


```sql
!ls
```

    Jupyter的多语言支持.ipynb
    README.md
    __pycache__
    count_file0.txt
    count_file1.txt
    count_file2.txt
    count_file3.txt
    count_file4.txt
    count_file5.txt
    count_file6.txt
    count_file7.txt
    count_file8.txt
    count_file9.txt
    hello.py
    myfib.py
    source
    在Ipython中的魔法命令.ipynb
    在Ipython中使用异步接口.ipynb
    在Ipython中的代码调试与优化.ipynb
    自定义WrapperKernel.ipynb
    多进程并行计算.ipynb
    


除了这些外使用`metakernel`定义的自定义WrapperKernel允许加载`~/.ipython/metakernel/magics`中的所有文件以及项目下`magics`文件夹下的以`_magic.py`为后缀的文件作为魔法命令.激活的方式有两种:

1. 在你的项目中一个必定会被import的文件中(通常是`kernel.py`)加上如下语句
    ```python
    from metakernel import register_ipython_magics
    register_ipython_magics(*maigc_names:str)
    ```
   

2. 在`~/.ipython/你的ipython配置文件夹/ipython_config.py`中最后加上

    ```python
    c = get_config()
    startup = [
       'from metakernel import register_ipython_magics',
       'register_ipython_magics(*maigc_names:str)',
    ]
    c.InteractiveShellApp.exec_lines = startup
    ```

其中`maigc_names`就是本项目中希望加载的魔法命令名
