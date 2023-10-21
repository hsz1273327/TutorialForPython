# Fortain扩展

Fortain是一门专为计算设计的编译型编程语言.在python中我们可以简单的使用Fortain扩展python要感谢`numpy`.`numpy`许多算法实现是使用`Fortran`,[f2py](https://numpy.org/doc/stable/f2py/)就是`numpy`中用于将`Fortran`代码编译为python可以使用的动态链接库的工具.

## 是否有必要用Fortran写扩展

这个要看应用的领域,Fortran是专为计算设计的编程语言,多维数组是内置的数据类型,可以说在向量计算矩阵计算上它有天然的优势,而且语法相比C语言更加接近python,也没有复杂的语法和底层概念,用它写扩展可以专注于算法.因此如果一个模块完全是做计算的,那它就很适合用这门语言写扩展.

但同时它的劣势也就在于太过小众,如果一个人已经回C/C++,甚至不用是精通,他往往也没有动力再学一门新语言.同时Fortran除了写计算逻辑优秀以外几乎可以说一无是处.也没什么现代的编程技巧,因此除非是用作写算法模块,否则确实不值得专门学个这.

但碰巧科学计算是python最重要的应用领域,几乎没有之一.数学家,物理学家往往都不关心怎么编程,只关心算法本身.如果是年级大点的数学家,物理学家,几乎都学过Fortran,而年轻的可能没学过,但Fortran好上手的特性非常适合作为第一门高性能计算编程语言.因此这个需求和这个用户群体非常契合.

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

更加正式的入门资料推荐<<30分钟快速学习Fortran-95>>这本书.

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

    /Users/mac/micromamba/envs/py3.10/lib/python3.10/site-packages/setuptools/_distutils/cmd.py:66: SetuptoolsDeprecationWarning: setup.py install is deprecated.
    !!
    
            ********************************************************************************
            Please avoid running ``setup.py`` directly.
            Instead, use pypa/build, pypa/installer, pypa/build or
            other standards-based tools.
    
            See https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html for details.
            ********************************************************************************
    
    !!
      self.initialize_options()



```python
from demo import sum_of_square
```


```python
sum_of_square([1,2,3,4])
```




    30.0



## 在python解释器中调用编译工具

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
    INFO: unifing config_cc, config, build_clib, build_ext, build commands --compiler options
    running config_fc
    INFO: unifing config_fc, config, build_clib, build_ext, build commands --fcompiler options
    running build_src
    INFO: build_src
    INFO: building extension "demo1" sources
    INFO: f2py options: []
    INFO: f2py:> /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10/demo1module.c
    creating /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10
    Reading fortran codes...
    	Reading file '/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmp9w3ykm9l.f95' (format:free)
    Post-processing...
    	Block: demo1
    			Block: sum_of_square
    Applying post-processing hooks...
      character_backward_compatibility_hook
    Post-processing (stage 2)...
    Building modules...
        Building module "demo1"...
        Generating possibly empty wrappers"
        Maybe empty "demo1-f2pywrappers.f"
            Constructing wrapper function "sum_of_square"...
              y = sum_of_square(x,[n])
        Wrote C/API module "demo1" to file "/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10/demo1module.c"
    INFO:   adding '/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10/fortranobject.c' to sources.
    INFO:   adding '/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10' to include_dirs.
    copying /Users/mac/micromamba/envs/py3.10/lib/python3.10/site-packages/numpy/f2py/src/fortranobject.c -> /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10
    copying /Users/mac/micromamba/envs/py3.10/lib/python3.10/site-packages/numpy/f2py/src/fortranobject.h -> /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10
    INFO:   adding '/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10/demo1-f2pywrappers.f' to sources.
    INFO: build_src: building npy-pkg config files
    running build_ext
    INFO: customize UnixCCompiler
    INFO: customize UnixCCompiler using build_ext
    INFO: get_default_fcompiler: matching types: '['gnu95', 'nag', 'nagfor', 'absoft', 'ibm', 'intel', 'gnu', 'g95', 'pg']'
    INFO: customize Gnu95FCompiler
    INFO: Found executable /usr/local/bin/gfortran
    INFO: customize Gnu95FCompiler
    INFO: customize Gnu95FCompiler using build_ext
    INFO: building 'demo1' extension
    INFO: compiling C sources
    INFO: C compiler: clang -Wno-unused-result -Wsign-compare -Wunreachable-code -DNDEBUG -fwrapv -O2 -Wall -fPIC -O2 -isystem /Users/mac/micromamba/envs/py3.10/include -fPIC -O2 -isystem /Users/mac/micromamba/envs/py3.10/include -ftrapping-math
    
    creating /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var
    creating /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var/folders
    creating /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var/folders/j_
    creating /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn
    creating /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T
    creating /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc
    creating /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10
    INFO: compile options: '-DNPY_DISABLE_OPTIMIZATION=1 -I/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10 -I/Users/mac/micromamba/envs/py3.10/lib/python3.10/site-packages/numpy/core/include -I/Users/mac/micromamba/envs/py3.10/include/python3.10 -c'
    INFO: clang: /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10/fortranobject.c
    INFO: clang: /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10/demo1module.c
    INFO: compiling Fortran sources
    INFO: Fortran f77 compiler: /usr/local/bin/gfortran -Wall -g -ffixed-form -fno-second-underscore -fPIC -O3 -funroll-loops
    Fortran f90 compiler: /usr/local/bin/gfortran -Wall -g -fno-second-underscore -fPIC -O3 -funroll-loops
    Fortran fix compiler: /usr/local/bin/gfortran -Wall -g -ffixed-form -fno-second-underscore -Wall -g -fno-second-underscore -fPIC -O3 -funroll-loops
    INFO: compile options: '-I/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10 -I/Users/mac/micromamba/envs/py3.10/lib/python3.10/site-packages/numpy/core/include -I/Users/mac/micromamba/envs/py3.10/include/python3.10 -c'
    INFO: gfortran:f90: /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmp9w3ykm9l.f95
    INFO: gfortran:f77: /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10/demo1-f2pywrappers.f
    INFO: /usr/local/bin/gfortran -Wall -g -Wall -g -undefined dynamic_lookup -bundle /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10/demo1module.o /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10/fortranobject.o /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmp9w3ykm9l.o /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc/src.macosx-10.9-x86_64-3.10/demo1-f2pywrappers.o -L/usr/local/Cellar/gcc/13.1.0/bin/../lib/gcc/current/gcc/x86_64-apple-darwin20/13 -L/usr/local/Cellar/gcc/13.1.0/bin/../lib/gcc/current/gcc/x86_64-apple-darwin20/13/../../.. -L/usr/local/Cellar/gcc/13.1.0/bin/../lib/gcc/current/gcc/x86_64-apple-darwin20/13/../../.. -lgfortran -o ./demo1.cpython-310-darwin.so
    Removing build directory /var/folders/j_/p0q1k_mj4cs0dqn0sqnshsrr0000gn/T/tmpb8to7mdc
    





    0




```python
from demo1 import sum_of_square
```


```python
sum_of_square([1,2,3,4])
```




    30.0


