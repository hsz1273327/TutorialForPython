
# import_hook

所谓`import hook`就是指直接自定义finder和loader,并将finder放入导入过程,以实现一些特殊的运行时行为的技巧.

利用这个可以做到很多非常神奇的事情,比如

+ import某个特定模块时触发某个回调函数来通知我们
+ import一个远程服务器上的模块
+ 直接import其他语言的模块来使用

本节需要的先验知识包括:

+ [模块的导入方式](/语法篇/模块/模块的加载流程.html)
+ [动态编译](/语法篇/元编程/动态编译.html)
+ [使用f2py为python嵌入fortran代码](/嵌入与扩展篇/使用f2py用fortain给python写扩展.html)

## import hook的基本形式

import hook通常是以一个单文件模块的形式出现的,其中的过程说白了就是自定义finder和loader,因此自定义这两个类都是必须的,然后就是将定义的finder实例化,并将这个实例加入`sys.meta_path`.下面是模板代码.

```python
import importlib
from importlib.abc import (
    MetaPathFinder, 
    PathEntryFinder,
    Loader
)
from importlib.machinery import ModuleSpec
import sys
from collections import defaultdict


class ClientImportLoader(Loader):
    @classmethod
    def create_module(clz,spec):
        """用于创建模块的."""
        module = __create_module_from_spec(spec)
        return module or None

    @classmethod
    def exec_module (clz, module):
        """每次执行引入模块或者重载模块时会执行的操作"""
        pass

loader= ClientImportLoader()
    

class ClientImportFinder(MetaPathFinder):

    @classmethod
    def find_spec (klass, full_name, paths=None, target=None):
        """查找模块的逻辑"""
        pass
        return ModuleSpec(full_name, loader, origin=module_full_path)
    

sys.meta_path.insert(0, ClientImportFinder())

```


当这个定义import hook的模块被加载后,他就可以正常的执行自己的功能了,因此通常这个import hook的模块需要优先加载.


## import某个特定模块时触发某个回调函数来通知我们

这个例子来自python cookbook,不过上面的代码已经比较过时了,这边给出python3.5+推荐的写法


```python
import importlib
from importlib.abc import (
    MetaPathFinder, 
    PathEntryFinder,
    Loader
)
from importlib.machinery import ModuleSpec
import sys
from collections import defaultdict

_post_import_hooks = defaultdict(list)

class ClientImportLoader(Loader):
    def __init__(self, finder):
        self._finder = finder
        

    def create_module(self,spec):
        """这边只要调用父类的实现即可."""
        return super().create_module(spec)

    def exec_module (self, module):
        """在_post_import_hooks中查找对应模块中的回调函数并执行."""
        for func in _post_import_hooks[module.__name__]:
            func(module)
        self._finder._skip.remove(module.__name__)
        
class ClientImportFinder(MetaPathFinder):
    
    def __init__(self):
        self._skip = set()

    def find_spec(self, full_name, paths=None, target=None):
        if full_name in self._skip:
            return None
        self._skip.add(full_name)
        loader = ClientImportLoader(self)
        return ModuleSpec(full_name, loader, origin=paths)
        
        
def when_imported(fullname):
    def decorate(func):
        if fullname in sys.modules:
            func(sys.modules[fullname])
        else:
            _post_import_hooks[fullname].append(func)
        return func
    return decorate

finder = ClientImportFinder()
sys.meta_path.insert(0, finder)
```


```python
@when_imported('numpy')
def warn_numpy(mod):
    print('numpy? Are you crazy?')

```


```python
import numpy
```

    ********None
    ['__abstractmethods__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_abc_cache', '_abc_negative_cache', '_abc_negative_cache_version', '_abc_registry', '_finder', 'create_module', 'exec_module', 'load_module', 'module_repr']



```python
import a
```

    ********None



```python
finder._skip
```




    set()



为了避免陷入无线循环,ClientImportFinder维护了一个所有被加载过的模块集合`_skip`,如果一个模块在加载过程中又有另一个地方来加载,那么就会跳过这个加载器

## import一个远程服务器上的模块


这个例子主要是复写finder以可以查找到目标服务器上的模块文件.同时复写loader的create_module方法用远端的代码生成服务.

我们的远程代码以http服务的形式放在静态服务器上
```shell
testcode-|
         |-spam.py
         |-fib.py
         |-grok-|
                |-__init__.py
                |-blah.py
```

`spam.py`
```python
print("I'm spam")

def hello(name):
    print('Hello %s' % name)
```

`fib.py`
```python
print("I'm fib")

def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)
```

`grok/__init__.py`

```python
print("I'm grok.__init__")
```
`grok/blah.py`

```python
print("I'm grok.blah")
```
使用python自带的http服务启动:

```shell
cd source/testcode
python3 -m http.server 15000
```


```python
import requests
n = requests.get("http://localhost:15000/fib.py")
print(n.content.decode("utf-8"))
```

    print("I'm fib")
    
    def fib(n):
        if n < 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)


### 最简单的方法

这个流程也描述了最通用的模块导入流程.我们可以使用`imp.new_module`新建一个空的模块对象,再使用内置方法`compile()`将源码编译到一个代码对象中,然后在模块对象的字典中来执行它.


这种方式没有嵌入到通常的import语句中,如果要支持更高级的结构比如包就需要更多的工作了.

下面是使用这个函数的方式:


```python
import imp
import urllib.request
import sys

def load_module(url):
    u = urllib.request.urlopen(url)
    source = u.read().decode('utf-8')
    mod = sys.modules.setdefault(url, imp.new_module(url))
    code = compile(source, url, 'exec')
    mod.__file__ = url
    mod.__package__ = ''
    exec(code, mod.__dict__)
    return mod
```


```python
fib = load_module('http://localhost:15000/fib.py')
```

    I'm fib



```python
fib.fib(10)
```




    89




```python
fib
```




    <module 'http://localhost:15000/fib.py' from 'http://localhost:15000/fib.py'>



### 使用 import hook实现隐式调用远端模块

如果我们想要导入文件系统中某个文件作为模块,我们会这样写以确保文件目录Python解释器可以找到.

```python
import sys

sys.path.append('<path>')
```

我们希望远端的也可以实现这种与标准流程统一的方式,这时候就需要使用import hook了.

因为访问的地址和文件系统不同,因此可以使用`sys.path_hooks`为这个特定的地址设置一个finder

此处我们需要

+ 定义finder
+ 定义loader
+ 定义handle_url()函数作为钩子

    `sys.path_hooks.append(handle_url)`变量中注册着查找`sys.path`的钩子,当`sys.path`的实体被处理时会调用`sys.path_hooks`中的函数.如果任何一个函数返回了一个finder,那么这个对象就被用来为`sys.path`实体加载模块.
    
    
这个例子完全使用标准库实现



```python
%%writefile urlimport.py
import warnings
import sys
import importlib.abc
from importlib.machinery import ModuleSpec
import imp
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser

# Get links from a given URL
def _get_links(url):
    """在指定url查找包含的其他url"""
    class LinkParser(HTMLParser):
        """解析html文件,从中获取a标签中的url"""
        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                attrs = dict(attrs)
                links.add(attrs.get('href').rstrip('/'))
    links = set()
    try:
        warnings.warn(f'Getting links from {url}',UserWarning)
        u = urlopen(url)
        parser = LinkParser()
        parser.feed(u.read().decode('utf-8'))
    except Exception as e:
        warnings.warn(f'Could not get links. {e}',UserWarning)
    warnings.warn(f'links: {links}',UserWarning)
    return links

class UrlPathFinder(importlib.abc.PathEntryFinder):
    """查找url及其中a标签中指向的url中的模块."""
    def __init__(self, baseurl):
        self._links = None # 保存一个baseurl中指定的可用url路径
        #self._loader = UrlModuleLoader(baseurl) # 指定默认的loader
        self._baseurl = baseurl # 
    def find_spec(self, fullname, paths=None, target=None):
        warnings.warn(f'find_loader: {fullname}', UserWarning)
        parts = fullname.split('.')
        basename = parts[-1]
        # 查看links和初始化links
        if self._links is None:
            self._links = [] 
            self._links = _get_links(self._baseurl)
        spec = None
        
        # 检查links是不是package,判断的标准是有没有.py
        if basename in self._links:
            warnings.warn(f'find_loader: trying package {fullname}', UserWarning)
            fullurl = self._baseurl + '/' + basename
            try:
                loader = UrlPackageLoader(fullurl)
                loader.load_module(fullname)#
                warnings.warn(f'find_loader: package {fullname} loaded', UserWarning)
                spec = ModuleSpec(fullname, loader, origin=paths)
            except ImportError as ie:
                warnings.warn(f'find_loader: {fullname} is a namespace package', UserWarning)
                spec = None
            except Exception as e:
                raise e
            

        elif (basename + '.py') in self._links:
            # 正常module的处理
            warnings.warn(f'find_loader: module {fullname} found', UserWarning)
            loader = UrlModuleLoader(self._baseurl)
            spec = ModuleSpec(fullname, loader, origin=paths)
        else:
            warnings.warn(f'find_loader: module {fullname} not found', UserWarning)
            
        return spec

    def invalidate_caches(self):
        warnings.warn("invalidating link cache", UserWarning)
        self._links = None


# Module Loader for a URL
class UrlModuleLoader(importlib.abc.SourceLoader):
    def __init__(self, baseurl):
        self._baseurl = baseurl
        self._source_cache = {}

    def create_module(self,spec):
        """这边只要调用父类的实现即可."""
        
        mod = sys.modules.setdefault(spec.name, imp.new_module(spec.name))
        mod.__file__ = self.get_filename(spec.name)
        mod.__loader__ = self
        mod.__package__ = spec.name.rpartition('.')[0]
        return mod
        

    def exec_module (self, module):
        """在_post_import_hooks中查找对应模块中的回调函数并执行."""
        code = self.get_code(module.__name__)
        exec(code, module.__dict__)

    # Optional extensions
    def get_code(self, fullname):
        src = self.get_source(fullname)
        return compile(src, self.get_filename(fullname), 'exec')

    def get_data(self, path):
        pass

    def get_filename(self, fullname):
        return self._baseurl + '/' + fullname.split('.')[-1] + '.py'

    def get_source(self, fullname):
        filename = self.get_filename(fullname)
        warnings.warn(f'loader: reading {filename}', UserWarning)
        if filename in self._source_cache:
            warnings.warn(f'loader: cached {fullname} not found', UserWarning)
            return self._source_cache[filename]
        try:
            u = urlopen(filename)
            source = u.read().decode('utf-8')
            warnings.warn(f'loader: {filename} loaded', UserWarning)
            self._source_cache[filename] = source
            return source
        except (HTTPError, URLError) as e:
            warnings.warn(f'loader: {filename} failed. {e}', UserWarning)
            raise ImportError("Can't load %s" % filename)

    def is_package(self, fullname):
        return False

# Package loader for a URL
class UrlPackageLoader(UrlModuleLoader):
    def create_module(self, spec):
        mod = super().create_module(spec)
        mod.__path__ = [ self._baseurl ]
        mod.__package__ = spec.name
        return mod

    def get_filename(self, fullname):
        return self._baseurl + '/' + '__init__.py'

    def is_package(self, fullname):
        return True

        


# Check path to see if it looks like a URL
_url_path_cache = {}
def handle_url(path):
    if path.startswith(('http://', 'https://')):
        warnings.warn(f'Handle path? {path}. [Yes]', UserWarning)
        if path in _url_path_cache:
            finder = _url_path_cache[path]
        else:
            finder = UrlPathFinder(path)
            _url_path_cache[path] = finder
        return finder
    else:
        warnings.warn(f'Handle path? {path}. [No]', UserWarning)

def install_path_hook():
    sys.path_hooks.append(handle_url)
    sys.path_importer_cache.clear()
    warnings.warn('Installing handle_url', UserWarning)

def remove_path_hook():
    sys.path_hooks.remove(handle_url)
    sys.path_importer_cache.clear()
    warnings.warn('Removing handle_url', UserWarning)
    
install_path_hook()
```

    Overwriting urlimport.py



```python
import fib
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-2-7d018bf75fbf> in <module>()
    ----> 1 import fib
    

    ModuleNotFoundError: No module named 'fib'



```python
import urlimport
```

    /Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/urlimport.py:162: UserWarning: Installing handle_url
      warnings.warn('Installing handle_url', UserWarning)



```python
import fib
```

    /Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/urlimport.py:157: UserWarning: Handle path? /Users/huangsizhe/anaconda3/lib/python36.zip. [No]
      warnings.warn(f'Handle path? {path}. [No]', UserWarning)



    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-4-7d018bf75fbf> in <module>()
    ----> 1 import fib
    

    ModuleNotFoundError: No module named 'fib'



```python
import sys
sys.path.append('http://localhost:15000')
```


```python
import fib
```


```python
fib.fib(5)
```




    8



## 直接import其他语言的模块来使用

一个更加酷的用法是直接导入别的语言的代码成为模块.这有两种途径

+ 通过一个自定义的编译器将源码编译为python可以直接import的动态链接库,之后再导入这个动态链接库
+ 通过一个自定义的语法解释器将特定源码转化为python对象

### 导入Fortran代码作为模块

这个例子我们来尝试第一种方法,其基本流程是:

1. 定义一个finder用于找到以`.f`,`.f90`或者`.f95`位后缀的文件作为源文件
    
    需要注意的这个需求依然会用到文件系统,Fortran的源码很大的可能性与python的原生源文件共存,因此不适合使用`sys.path_hook`.

2. 使用numpy中自带的工具`f2py`来实现Fortran代码的编译工作
    
    `f2py`无法指定输出的动态链接库位置,需要进一步的文件系统操作.这边可以利用标准库`Pathlib`和`shutil`


3. 将编译成功后的动态链接库导入到程序中.

    需要注意引入动态链接库时不能使用`import`或者`__import__`或者`importlib.import_module`这些直接生成完整模块对象的方式,否则会递归调用.
    此处应该使用如下的方式借由生成spec来生成模块.
    ```python
    wrap_spec = importlib.util.spec_from_file_location(
            spec.name,
            str(target_path)
        )
    mod = importlib.util.module_from_spec(wrap_spec)
    ```
    再借由这个spec的loader来执行模块
    ```python
    wrap_spec.loader.exec_module(mod)
    ```




当然了这个例子并没有考虑fortain本身的语法和多文件编译的问题,可能还会有些问题.


```python
import sys
```


```python
sys.path_hooks
```




    [zipimport.zipimporter,
     <function _frozen_importlib_external.FileFinder.path_hook.<locals>.path_hook_for_FileFinder>]




```python
%%writefile fortranimport.py
import os
import sys
import hashlib
import shutil
import warnings
from pathlib import Path
import importlib
from importlib.abc import (
    MetaPathFinder,
    PathEntryFinder,
    Loader
)
from importlib.machinery import ModuleSpec

from numpy import f2py


class FortranImportLoader(Loader):
    def __init__(self, source_path):
        self._source_path = source_path
        with open(str(self._source_path), "rb") as f:
            self.source = f.read()
        self.source_hash = hashlib.md5(self.source)
        self.wrap_spec = None

    def _check_source(self):
        with open(str(self._source_path), "rb") as f:
            source = f.read()
        source_hash = hashlib.md5(source)
        if self.source_hash == source_hash:
            return False
        else:
            self.source_hash = source_hash
            self.source = source
            return True

    def _compile(self):
        modulename = self._source_path.stem
        suffix = self._source_path.suffix
        complie_result = f2py.compile(
            self.source,
            modulename=modulename,
            verbose=False,
            extra_args="--quiet", 
            extension=suffix
        )
        if complie_result != 0:
            raise ImportError("complie failed")
        else:
            root = Path(".").resolve()
            find_files = [
                i for i in root.iterdir() if i.match(f"{modulename}*.pyd") or i.match(f"{modulename}*.so")
            ]
            if len(find_files) != 1:
                raise ImportError(f"find {len(find_files)} Dynamic Link Library")
            file = find_files[0]
            target_path = self._source_path.with_name(file.name)
            if file != target_path:
                try:
                    shutil.move(str(file), str(target_path))
                except shutil.SameFileError as sfe:
                    pass
                except Exception as e:
                    raise e
            del_target = [i for i in root.iterdir() if i.match(str(file)+".*")]
            for i in del_target:
                try:
                    i.chmod(0o777)
                    i.unlink()
                except Exception as e:
                    warnings.warn(f'can not delete file {i}:{type(e)}--{e}', UserWarning)
            return target_path

    def create_module(self, spec):
        self._check_source()
        target_path = self._compile()
        self.wrap_spec = importlib.util.spec_from_file_location(
            spec.name,
            str(target_path)
        )
        mod = importlib.util.module_from_spec(self.wrap_spec)
        mod = sys.modules.setdefault(spec.name, mod)
        return mod

    def exec_module(self, module):
        """在_post_import_hooks中查找对应模块中的回调函数并执行."""
        self.wrap_spec.loader.exec_module(module)
        


class FortranImportFinder(MetaPathFinder):

    def find_spec(self, fullname, paths=None, target=None):
        relative_path = fullname.replace(".", "/")
        base_path = None
        full_path = None

        for path in sys.path:
            base_path = Path(path).resolve()
            abs_path = base_path.joinpath(relative_path)
            if abs_path.with_suffix(".f").exists():
                full_path = abs_path.with_suffix(".f")
                break
            elif abs_path.with_suffix(".f90").exists():
                full_path = abs_path.with_suffix(".f90")
                break
            elif abs_path.with_suffix(".f95").exists():
                full_path = abs_path.with_suffix(".f95")
                break
        else:
            return None
        warnings.warn(f'FortranImportFinder find_spec: {fullname}', UserWarning)
        loader = FortranImportLoader(full_path)
        spec = ModuleSpec(fullname, loader, origin=paths)
        return spec


finder = FortranImportFinder()
sys.meta_path.insert(0, finder)
warnings.warn('now you can import a fortain file', UserWarning)

```

    Overwriting fortranimport.py



```python
import fortranimport
```

    /Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/fortranimport.py:122: UserWarning: now you can import a fortain file
      warnings.warn('now you can import a fortain file', UserWarning)



```python
import demo
```

    /Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/fortranimport.py:114: UserWarning: FortranImportFinder find_spec: demo
      warnings.warn(f'FortranImportFinder find_spec: {fullname}', UserWarning)


    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpg1hdbzxv/src.macosx-10.7-x86_64-3.6/demomodule.c:16:
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpg1hdbzxv/src.macosx-10.7-x86_64-3.6/fortranobject.h:13:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h:4:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarrayobject.h:18:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarraytypes.h:1816:
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: "Using deprecated NumPy API, disable it by "          "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
    #warning "Using deprecated NumPy API, disable it by " \
     ^
    /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpg1hdbzxv/src.macosx-10.7-x86_64-3.6/demomodule.c:109:12: warning: unused function 'f2py_size' [-Wunused-function]
    static int f2py_size(PyArrayObject* var, ...)
               ^
    2 warnings generated.
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpg1hdbzxv/src.macosx-10.7-x86_64-3.6/fortranobject.c:2:
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpg1hdbzxv/src.macosx-10.7-x86_64-3.6/fortranobject.h:13:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h:4:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarrayobject.h:18:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarraytypes.h:1816:
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: "Using deprecated NumPy API, disable it by "          "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
    #warning "Using deprecated NumPy API, disable it by " \
     ^
    /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpg1hdbzxv/src.macosx-10.7-x86_64-3.6/fortranobject.c:138:18: warning: comparison of integers of different signs: 'Py_ssize_t' (aka 'long') and 'unsigned long' [-Wsign-compare]
            if (size < sizeof(notalloc)) {
                ~~~~ ^ ~~~~~~~~~~~~~~~~
    2 warnings generated.


    /Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/fortranimport.py:71: UserWarning: can not delete file /Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/demo.cpython-36m-darwin.so.dSYM:<class 'PermissionError'>--[Errno 1] Operation not permitted: '/Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/demo.cpython-36m-darwin.so.dSYM'
      warnings.warn(f'can not delete file {i}:{type(e)}--{e}', UserWarning)



```python
demo.sum_of_square([1,2,3,4,5])
```




    55.0




```python
import demopackage.demo1
```

    /Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/fortranimport.py:114: UserWarning: FortranImportFinder find_spec: demopackage.demo1
      warnings.warn(f'FortranImportFinder find_spec: {fullname}', UserWarning)


    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmponoxb1eb/src.macosx-10.7-x86_64-3.6/demo1module.c:16:
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmponoxb1eb/src.macosx-10.7-x86_64-3.6/fortranobject.h:13:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h:4:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarrayobject.h:18:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarraytypes.h:1816:
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: "Using deprecated NumPy API, disable it by "          "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
    #warning "Using deprecated NumPy API, disable it by " \
     ^
    /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmponoxb1eb/src.macosx-10.7-x86_64-3.6/demo1module.c:109:12: warning: unused function 'f2py_size' [-Wunused-function]
    static int f2py_size(PyArrayObject* var, ...)
               ^
    2 warnings generated.
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmponoxb1eb/src.macosx-10.7-x86_64-3.6/fortranobject.c:2:
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmponoxb1eb/src.macosx-10.7-x86_64-3.6/fortranobject.h:13:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h:4:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarrayobject.h:18:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarraytypes.h:1816:
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: "Using deprecated NumPy API, disable it by "          "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
    #warning "Using deprecated NumPy API, disable it by " \
     ^
    /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmponoxb1eb/src.macosx-10.7-x86_64-3.6/fortranobject.c:138:18: warning: comparison of integers of different signs: 'Py_ssize_t' (aka 'long') and 'unsigned long' [-Wsign-compare]
            if (size < sizeof(notalloc)) {
                ~~~~ ^ ~~~~~~~~~~~~~~~~
    2 warnings generated.


    /Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/fortranimport.py:71: UserWarning: can not delete file /Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/demo1.cpython-36m-darwin.so.dSYM:<class 'PermissionError'>--[Errno 1] Operation not permitted: '/Users/huangsizhe/WORKSPACE/github/hsz1273327/TutorialForPython/ipynbs/语法篇/元编程/demo1.cpython-36m-darwin.so.dSYM'
      warnings.warn(f'can not delete file {i}:{type(e)}--{e}', UserWarning)



```python
demopackage.demo1.sum_of_square([1,2,3,4,5])
```




    55.0



## 使用警告

import hook是python中非常高级的语言技巧,并不提倡用户使用,如果非要使用,请使用`warnning`在导入时提醒用户
