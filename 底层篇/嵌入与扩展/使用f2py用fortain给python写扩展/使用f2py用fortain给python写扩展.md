
# 使用f2py用fortain给python写扩展

`numpy`许多算法实现是使用`Fortran`,`f2py`就是`numpy`中用于将`Fortran`代码编译为python可以使用的动态链接库的工具.

本文主要介绍如何使用`f2py`编译`Fortran`代码,使python可以调用.

## 是否有必要用Fortran写扩展

这个要看应用的领域,Fortran是专为计算设计的编程语言,多维数组是内置的数据类型,可以说在向量计算矩阵计算上它有天然的优势,而且语法相比C语言更加接近python,也没有复杂的语法和底层概念,用它写扩展可以专注于算法.因此如果一个模块完全是做计算的,那它就很适合用这门语言写扩展.

但同时它的劣势也就在于太过小众,如果一个人已经回C/C++,甚至不用是精通,他往往也没有动力再学一门新语言.同时Fortran除了写计算逻辑优秀以外几乎可以说一无是处.也没什么现代的编程技巧,因此除非是用作写算法模块,否则确实不值得专门学个这.

那为啥还要写这一节?

因为科学计算是python最重要的应用领域,几乎没有之一;数学家,物理学家往往都不关心怎么编程,只关心算法本身.如果是年级大点的数学家,物理学家,几乎都学过Fortran,而年轻的可能没学过,但Fortran好上手的特性非常适合作为第一门高性能计算编程语言.因此这个需求和这个用户群体非常契合.这就值得介绍一下了.

## 简单fortain语法

相对比价现代,支持面又比较广的是fortran95标准.其基本特点是:

+ 完整的结构化和模块化
+ 矩阵运算支持
+ 简单的子程序接口,方便传递矩阵 
+ 功能强大而简单的Namelist输入输出 
+ 对并行计算提供特别支持
+ 编译代码执行效率高
+ 内置函数较少



### 基本规则

+ 大小写不敏感
+ 自由格式
+ `&`为换行连写
+ `!`为注释语句
+ 程序中任何地方用`stop`可推出程序
+ 建议每个域(program、module、function、 subrouting)第一行都写`implicit none`


## 使用f2py编译fortran的pyton扩展

此处给出一个简单的求平方和的例子用于演示`demo.f95`:

```fortran
subroutine sum_of_square(x, y, n)  
      implicit none
      integer, intent(in) :: n  
      integer :: i
      real(kind=8), intent(in) :: x(n)  
      real(kind=8), intent(out) :: y  
      y = 0
      do i=1, n  
            y = y + x(i)**2
      end do  
end
```

使用命令`f2py -c -m <module_name> file_path`就可以很简单的将其编译为python模块


```python
!f2py -c -m demo demo.f95 --quiet
```

    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpqavw1pmi/src.macosx-10.7-x86_64-3.6/demomodule.c:16:
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpqavw1pmi/src.macosx-10.7-x86_64-3.6/fortranobject.h:13:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h:4:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarrayobject.h:18:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarraytypes.h:1816:
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: "Using deprecated NumPy API, disable it by "          "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
    #warning "Using deprecated NumPy API, disable it by " \
     ^
    /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpqavw1pmi/src.macosx-10.7-x86_64-3.6/demomodule.c:109:12: warning: unused function 'f2py_size' [-Wunused-function]
    static int f2py_size(PyArrayObject* var, ...)
               ^
    2 warnings generated.
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpqavw1pmi/src.macosx-10.7-x86_64-3.6/fortranobject.c:2:
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpqavw1pmi/src.macosx-10.7-x86_64-3.6/fortranobject.h:13:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h:4:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarrayobject.h:18:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarraytypes.h:1816:
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: "Using deprecated NumPy API, disable it by "          "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
    #warning "Using deprecated NumPy API, disable it by " \
     ^
    /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpqavw1pmi/src.macosx-10.7-x86_64-3.6/fortranobject.c:138:18: warning: comparison of integers of different signs: 'Py_ssize_t' (aka 'long') and 'unsigned long' [-Wsign-compare]
            if (size < sizeof(notalloc)) {
                ~~~~ ^ ~~~~~~~~~~~~~~~~
    2 warnings generated.



```python
from demo import sum_of_square
```


```python
sum_of_square([1,2,3,4])
```




    30.0



## *在python解释器中调用编译工具*

如果有需要在python环境中编译Fortran代码,那需要使用numpy中的`f2py`子模块

编译Fortran代码需要使用`f2py.compile(source, modulename='untitled', extra_args='', verbose=1, source_fn=None,extension=".f")`方法,


```python
from numpy import f2py
```


```python
with open("demo.f95","rb") as f:
    source = f.read()
```


```python
f2py.compile(source, modulename='demo1',extension='.f95')
```

    running build
    running config_cc
    unifing config_cc, config, build_clib, build_ext, build commands --compiler options
    running config_fc
    unifing config_fc, config, build_clib, build_ext, build commands --fcompiler options
    running build_src
    build_src
    building extension "demo1" sources
    f2py options: []
    f2py:> /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.c
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6
    Reading fortran codes...
    	Reading file '/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpwef1g0pz.f95' (format:free)
    Post-processing...
    	Block: demo1
    			Block: sum_of_square
    Post-processing (stage 2)...
    Building modules...
    	Building module "demo1"...
    		Constructing wrapper function "sum_of_square"...
    		  y = sum_of_square(x,[n])
    	Wrote C/API module "demo1" to file "/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.c"
      adding '/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.c' to sources.
      adding '/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6' to include_dirs.
    copying /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/f2py/src/fortranobject.c -> /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6
    copying /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/f2py/src/fortranobject.h -> /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6
    build_src: building npy-pkg config files
    running build_ext
    customize UnixCCompiler
    customize UnixCCompiler using build_ext
    get_default_fcompiler: matching types: '['gnu95', 'nag', 'absoft', 'ibm', 'intel', 'gnu', 'g95', 'pg']'
    customize Gnu95FCompiler
    Found executable /usr/local/bin/gfortran
    customize Gnu95FCompiler
    customize Gnu95FCompiler using build_ext
    building 'demo1' extension
    compiling C sources
    C compiler: gcc -Wno-unused-result -Wsign-compare -Wunreachable-code -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/Users/huangsizhe/anaconda3/include -arch x86_64 -I/Users/huangsizhe/anaconda3/include -arch x86_64
    
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6
    compile options: '-I/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6 -I/Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include -I/Users/huangsizhe/anaconda3/include/python3.6m -c'
    gcc: /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.c
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.c:16:
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.h:13:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h:4:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarrayobject.h:18:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarraytypes.h:1816:
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: "Using deprecated NumPy API, disable it by "          "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
    #warning "Using deprecated NumPy API, disable it by " \
     ^
    /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.c:109:12: warning: unused function 'f2py_size' [-Wunused-function]
    static int f2py_size(PyArrayObject* var, ...)
               ^
    2 warnings generated.
    gcc: /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.c
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.c:2:
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.h:13:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h:4:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarrayobject.h:18:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarraytypes.h:1816:
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: "Using deprecated NumPy API, disable it by "          "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
    #warning "Using deprecated NumPy API, disable it by " \
     ^
    /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.c:138:18: warning: comparison of integers of different signs: 'Py_ssize_t' (aka 'long') and 'unsigned long' [-Wsign-compare]
            if (size < sizeof(notalloc)) {
                ~~~~ ^ ~~~~~~~~~~~~~~~~
    2 warnings generated.
    compiling Fortran sources
    Fortran f77 compiler: /usr/local/bin/gfortran -Wall -g -ffixed-form -fno-second-underscore -m64 -fPIC -O3 -funroll-loops
    Fortran f90 compiler: /usr/local/bin/gfortran -Wall -g -fno-second-underscore -m64 -fPIC -O3 -funroll-loops
    Fortran fix compiler: /usr/local/bin/gfortran -Wall -g -ffixed-form -fno-second-underscore -Wall -g -fno-second-underscore -m64 -fPIC -O3 -funroll-loops
    compile options: '-I/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6 -I/Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include -I/Users/huangsizhe/anaconda3/include/python3.6m -c'
    gfortran:f90: /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpwef1g0pz.f95
    /usr/local/bin/gfortran -Wall -g -m64 -Wall -g -undefined dynamic_lookup -bundle /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.o /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.o /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpwef1g0pz.o -L/usr/local/Cellar/gcc/8.1.0/lib/gcc/8/gcc/x86_64-apple-darwin17.5.0/8.1.0 -L/usr/local/Cellar/gcc/8.1.0/lib/gcc/8/gcc/x86_64-apple-darwin17.5.0/8.1.0/../../.. -L/usr/local/Cellar/gcc/8.1.0/lib/gcc/8/gcc/x86_64-apple-darwin17.5.0/8.1.0/../../.. -lgfortran -o ./demo1.cpython-36m-darwin.so
    Removing build directory /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t
    running build
    running config_cc
    unifing config_cc, config, build_clib, build_ext, build commands --compiler options
    running config_fc
    unifing config_fc, config, build_clib, build_ext, build commands --fcompiler options
    running build_src
    build_src
    building extension "demo1" sources
    f2py options: []
    f2py:> /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.c
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6
    Reading fortran codes...
    	Reading file '/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpwef1g0pz.f95' (format:free)
    Post-processing...
    	Block: demo1
    			Block: sum_of_square
    Post-processing (stage 2)...
    Building modules...
    	Building module "demo1"...
    		Constructing wrapper function "sum_of_square"...
    		  y = sum_of_square(x,[n])
    	Wrote C/API module "demo1" to file "/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.c"
      adding '/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.c' to sources.
      adding '/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6' to include_dirs.
    copying /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/f2py/src/fortranobject.c -> /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6
    copying /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/f2py/src/fortranobject.h -> /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6
    build_src: building npy-pkg config files
    running build_ext
    customize UnixCCompiler
    customize UnixCCompiler using build_ext
    get_default_fcompiler: matching types: '['gnu95', 'nag', 'absoft', 'ibm', 'intel', 'gnu', 'g95', 'pg']'
    customize Gnu95FCompiler
    Found executable /usr/local/bin/gfortran
    customize Gnu95FCompiler
    customize Gnu95FCompiler using build_ext
    building 'demo1' extension
    compiling C sources
    C compiler: gcc -Wno-unused-result -Wsign-compare -Wunreachable-code -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/Users/huangsizhe/anaconda3/include -arch x86_64 -I/Users/huangsizhe/anaconda3/include -arch x86_64
    
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t
    creating /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6
    compile options: '-I/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6 -I/Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include -I/Users/huangsizhe/anaconda3/include/python3.6m -c'
    gcc: /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.c
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.c:16:
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.h:13:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h:4:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarrayobject.h:18:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarraytypes.h:1816:
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: "Using deprecated NumPy API, disable it by "          "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
    #warning "Using deprecated NumPy API, disable it by " \
     ^
    /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.c:109:12: warning: unused function 'f2py_size' [-Wunused-function]
    static int f2py_size(PyArrayObject* var, ...)
               ^
    2 warnings generated.
    gcc: /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.c
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.c:2:
    In file included from /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.h:13:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h:4:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarrayobject.h:18:
    In file included from /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/ndarraytypes.h:1816:
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: "Using deprecated NumPy API, disable it by "          "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
    #warning "Using deprecated NumPy API, disable it by " \
     ^
    /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.c:138:18: warning: comparison of integers of different signs: 'Py_ssize_t' (aka 'long') and 'unsigned long' [-Wsign-compare]
            if (size < sizeof(notalloc)) {
                ~~~~ ^ ~~~~~~~~~~~~~~~~
    2 warnings generated.
    compiling Fortran sources
    Fortran f77 compiler: /usr/local/bin/gfortran -Wall -g -ffixed-form -fno-second-underscore -m64 -fPIC -O3 -funroll-loops
    Fortran f90 compiler: /usr/local/bin/gfortran -Wall -g -fno-second-underscore -m64 -fPIC -O3 -funroll-loops
    Fortran fix compiler: /usr/local/bin/gfortran -Wall -g -ffixed-form -fno-second-underscore -Wall -g -fno-second-underscore -m64 -fPIC -O3 -funroll-loops
    compile options: '-I/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6 -I/Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/include -I/Users/huangsizhe/anaconda3/include/python3.6m -c'
    gfortran:f90: /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpwef1g0pz.f95
    /usr/local/bin/gfortran -Wall -g -m64 -Wall -g -undefined dynamic_lookup -bundle /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/demo1module.o /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/src.macosx-10.7-x86_64-3.6/fortranobject.o /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t/var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpwef1g0pz.o -L/usr/local/Cellar/gcc/8.1.0/lib/gcc/8/gcc/x86_64-apple-darwin17.5.0/8.1.0 -L/usr/local/Cellar/gcc/8.1.0/lib/gcc/8/gcc/x86_64-apple-darwin17.5.0/8.1.0/../../.. -L/usr/local/Cellar/gcc/8.1.0/lib/gcc/8/gcc/x86_64-apple-darwin17.5.0/8.1.0/../../.. -lgfortran -o ./demo1.cpython-36m-darwin.so
    Removing build directory /var/folders/62/pwdyzlx51_j_3_0lr8zxzbx00000gn/T/tmpx4bqux1t





    0




```python
from demo1 import sum_of_square
```


```python
sum_of_square([1,2,3,4])
```




    30.0


