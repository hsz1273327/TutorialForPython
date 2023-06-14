
# 静态化python模块

Cython提供了一些装饰器和类型用于直接扩展python模块,先看一个例子:


```python
%%writefile logistic.py
#cython: language_level=3
import cython
from math import exp
if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")
    
@cython.boundscheck(False)
@cython.ccall
def logistic(x:cython.double)->cython.double:
    return 1/(1+exp(-x))
```

    Writing logistic.py



```python
import logistic
```

    Just a lowly interpreted script.



```python
logistic.logistic(25)
```




    0.999999999986112




```python
%timeit logistic.logistic(25)
```

    534 ns ± 70 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)



```python
!cythonize -i -3 logistic.py
```

    Compiling /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic.py because it changed.
    [1/1] Cythonizing /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic.py
    running build_ext
    building 'logistic' extension
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog/Docs
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog/Docs/Python
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块
    gcc -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -O2 -pipe -mcpu=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -w -I/Users/huangsizhe/LIB/CONDA/anaconda/include/python3.6m -c /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic.c -o /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic.o
    gcc -bundle -undefined dynamic_lookup -Wl,-rpath,/Users/huangsizhe/LIB/CONDA/anaconda/lib -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -headerpad_max_install_names -Wl,-rpath,/Users/huangsizhe/LIB/CONDA/anaconda/lib -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -headerpad_max_install_names -O2 -pipe -mcpu=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -w -arch x86_64 /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp2i2j3uyu/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic.o -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -o /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic.cpython-36m-darwin.so



```python
import logistic
```

    Yep, I'm compiled.



```python
logistic.logistic(25)
```




    0.999999999986112




```python
%timeit logistic.logistic(25)
```

    329 ns ± 3.74 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)



```python
%%writefile logistic_A.py
#cython: language_level=3
import cython
from math import exp
if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")
    
@cython.boundscheck(False)
@cython.ccall
def logistic(x):
    return 1/(1+exp(-x))
```

    Writing logistic_A.py



```python
!cythonize -i -3 logistic_A.py
```

    Compiling /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_A.py because it changed.
    [1/1] Cythonizing /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_A.py
    running build_ext
    building 'logistic_A' extension
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog/Docs
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog/Docs/Python
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块
    gcc -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -O2 -pipe -mcpu=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -w -I/Users/huangsizhe/LIB/CONDA/anaconda/include/python3.6m -c /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_A.c -o /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_A.o
    gcc -bundle -undefined dynamic_lookup -Wl,-rpath,/Users/huangsizhe/LIB/CONDA/anaconda/lib -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -headerpad_max_install_names -Wl,-rpath,/Users/huangsizhe/LIB/CONDA/anaconda/lib -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -headerpad_max_install_names -O2 -pipe -mcpu=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -w -arch x86_64 /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmp8dxpsjki/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_A.o -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -o /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_A.cpython-36m-darwin.so



```python
import logistic_A
```

    Yep, I'm compiled.



```python
logistic_A.logistic(25)
```




    0.999999999986112




```python
%timeit logistic_A.logistic(25)
```

    364 ns ± 10.4 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)



```python
%%writefile logistic_B.pyx
#cython: language_level=3
from math import exp


cpdef double logistic(double x):
    return 1/(1+exp(-x))
```

    Writing logistic_B.pyx



```python
!cythonize -i -3 logistic_B.pyx
```

    Compiling /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_B.pyx because it changed.
    [1/1] Cythonizing /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_B.pyx
    running build_ext
    building 'logistic_B' extension
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog/Docs
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog/Docs/Python
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块
    gcc -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -O2 -pipe -mcpu=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -w -I/Users/huangsizhe/LIB/CONDA/anaconda/include/python3.6m -c /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_B.c -o /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_B.o
    gcc -bundle -undefined dynamic_lookup -Wl,-rpath,/Users/huangsizhe/LIB/CONDA/anaconda/lib -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -headerpad_max_install_names -Wl,-rpath,/Users/huangsizhe/LIB/CONDA/anaconda/lib -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -headerpad_max_install_names -O2 -pipe -mcpu=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -w -arch x86_64 /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpw9rfvum4/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_B.o -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -o /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_B.cpython-36m-darwin.so



```python
import logistic_B
```


```python
%timeit logistic_B.logistic(25)
```

    299 ns ± 11.3 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)



```python
%%writefile logistic_C.py
#cython: language_level=3
import cython
from math import exp
if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")
    
@cython.boundscheck(False)
@cython.ccall
@cython.returns(cython.double)
@cython.locals(x=cython.double)
def logistic(x):
    return 1/(1+exp(-x))
```

    Overwriting logistic_C.py



```python
!cythonize -i -3 logistic_C.py
```

    Compiling /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_C.py because it changed.
    [1/1] Cythonizing /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_C.py
    running build_ext
    building 'logistic_C' extension
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog/Docs
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog/Docs/Python
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码
    creating /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块
    gcc -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -O2 -pipe -mcpu=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -w -I/Users/huangsizhe/LIB/CONDA/anaconda/include/python3.6m -c /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_C.c -o /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_C.o
    gcc -bundle -undefined dynamic_lookup -Wl,-rpath,/Users/huangsizhe/LIB/CONDA/anaconda/lib -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -headerpad_max_install_names -Wl,-rpath,/Users/huangsizhe/LIB/CONDA/anaconda/lib -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -headerpad_max_install_names -O2 -pipe -mcpu=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -w -arch x86_64 /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/tmpy87kng_s/Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_C.o -L/Users/huangsizhe/LIB/CONDA/anaconda/lib -o /Users/huangsizhe/WORKSPACE/Blog/Docs/Python/TutorialForPython/ipynbs/python性能优化/使用Cython优化python程序的性能/使用cython加速python源码/静态化python模块/logistic_C.cpython-36m-darwin.so



```python
import logistic_C
```

    Yep, I'm compiled.



```python
%timeit logistic_C.logistic(25)
```

    382 ns ± 70.5 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

