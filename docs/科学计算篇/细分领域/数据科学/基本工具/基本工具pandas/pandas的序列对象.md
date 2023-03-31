
# pandas的序列对象

pandas的序列对象[Series](https://pandas.pydata.org/pandas-docs/stable/reference/series.html)是numpy1维数组的封装,带index

## 创建`Series`

创建Series有两种方式

+ 通过序列创建,这个序列可以是迭代器,list,dict,也可以是numpy的一维数组,dict创建后key就是它的index,其他序列index默认则是序列的位数
+ 通过固定值创建,创建后每一位都是这个固定值,但这就必须指定index(第二位)参数了

我们也可以用参数`index`为序列手动指定index


```python
import pandas as pd
import numpy as np
```


```python
a = pd.Series([1,2,3])
a
```




    0    1
    1    2
    2    3
    dtype: int64




```python
b = pd.Series(np.array([1,2,3]))
b
```




    0    1
    1    2
    2    3
    dtype: int64




```python
c = pd.Series({"a":1,"b":2,"c":3})
c
```




    a    1
    b    2
    c    3
    dtype: int64




```python
d = pd.Series(4,range(5))
d
```




    0    4
    1    4
    2    4
    3    4
    4    4
    dtype: int64



## 序列命名

Series对象可以使用`name`参数设置名字


```python
s = pd.Series(np.random.randn(5), name='取名字真难')
s
```




    0   -0.360848
    1    1.470764
    2    0.588654
    3   -0.055047
    4    0.411094
    Name: 取名字真难, dtype: float64



## 元素类型

和numpy的数组一样,`Series`是同构定长的可迭代数据结构,它可以使用元素`dtype`查看


```python
a.dtype
```




    dtype('int64')



要设置类型,需要使用接口`astype(dtype, copy=True, errors='raise', **kwargs)`

+ 参数`dtype`的取值范围是numpy的数组中的dtype和python对象类型的并集,另外额外多一种`category`类型,标明是分类数据(有限类别)
+ 参数`copy`标明是在原来对象上修改还是在原来对象内容基础上创建一个新的对象返回
+ 参数`errors`标明类型转化过程中遇到错误后的处理方式, `raise`会抛出错误,`ignore`则会跳过错误,返回原始数据


```python
e = pd.Series(["a","1","3"])
```


```python
e.astype("int64")
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-9-d8a1419271ef> in <module>
    ----> 1 e.astype("int64")
    

    ~/Lib/conda/anaconda3/lib/python3.7/site-packages/pandas/core/generic.py in astype(self, dtype, copy, errors, **kwargs)
       5689             # else, only a single dtype is given
       5690             new_data = self._data.astype(dtype=dtype, copy=copy, errors=errors,
    -> 5691                                          **kwargs)
       5692             return self._constructor(new_data).__finalize__(self)
       5693 


    ~/Lib/conda/anaconda3/lib/python3.7/site-packages/pandas/core/internals/managers.py in astype(self, dtype, **kwargs)
        529 
        530     def astype(self, dtype, **kwargs):
    --> 531         return self.apply('astype', dtype=dtype, **kwargs)
        532 
        533     def convert(self, **kwargs):


    ~/Lib/conda/anaconda3/lib/python3.7/site-packages/pandas/core/internals/managers.py in apply(self, f, axes, filter, do_integrity_check, consolidate, **kwargs)
        393                                             copy=align_copy)
        394 
    --> 395             applied = getattr(b, f)(**kwargs)
        396             result_blocks = _extend_blocks(applied, result_blocks)
        397 


    ~/Lib/conda/anaconda3/lib/python3.7/site-packages/pandas/core/internals/blocks.py in astype(self, dtype, copy, errors, values, **kwargs)
        532     def astype(self, dtype, copy=False, errors='raise', values=None, **kwargs):
        533         return self._astype(dtype, copy=copy, errors=errors, values=values,
    --> 534                             **kwargs)
        535 
        536     def _astype(self, dtype, copy=False, errors='raise', values=None,


    ~/Lib/conda/anaconda3/lib/python3.7/site-packages/pandas/core/internals/blocks.py in _astype(self, dtype, copy, errors, values, **kwargs)
        631 
        632                     # _astype_nansafe works fine with 1-d only
    --> 633                     values = astype_nansafe(values.ravel(), dtype, copy=True)
        634 
        635                 # TODO(extension)


    ~/Lib/conda/anaconda3/lib/python3.7/site-packages/pandas/core/dtypes/cast.py in astype_nansafe(arr, dtype, copy, skipna)
        681         # work around NumPy brokenness, #1987
        682         if np.issubdtype(dtype.type, np.integer):
    --> 683             return lib.astype_intsafe(arr.ravel(), dtype).reshape(arr.shape)
        684 
        685         # if we have a datetime/timedelta array of objects


    pandas/_libs/lib.pyx in pandas._libs.lib.astype_intsafe()


    ValueError: invalid literal for int() with base 10: 'a'



```python
e.astype("int64",errors="ignore")
```




    0    a
    1    1
    2    3
    dtype: object



### 元素类型推断

`pandas.api.types.infer_dtype()`提供了推断数据类型的能力,其返回值可以有

```
string
unicode
bytes
floating
integer
mixed-integer
mixed-integer-float
decimal
complex
categorical
boolean
datetime64
datetime
date
timedelta64
timedelta
time
period
mixed
```

另外还有专门针对不同类型的判断函数,包括:

+ `pandas.api.types.is_bool_dtype()`
+ `pandas.api.types.is_categorical_dtype()`
+ `pandas.api.types.is_complex_dtype()`
+ `pandas.api.types.is_datetime64_any_dtype()`
+ `pandas.api.types.is_datetime64_dtype()`
+ `pandas.api.types.is_datetime64_ns_dtype()`
+ `pandas.api.types.is_datetime64tz_dtype()`
+ `pandas.api.types.is_extension_array_dtype()`
+ `pandas.api.types.is_float_dtype()`
+ `pandas.api.types.is_int64_dtype()`
+ `pandas.api.types.is_integer_dtype()`
+ `pandas.api.types.is_interval_dtype()`
+ `pandas.api.types.is_numeric_dtype()`
+ `pandas.api.types.is_object_dtype()`
+ `pandas.api.types.is_period_dtype()`
+ `pandas.api.types.is_signed_integer_dtype()`
+ `pandas.api.types.is_string_dtype()`
+ `pandas.api.types.is_timedelta64_dtype()`
+ `pandas.api.types.is_timedelta64_ns_dtype()`
+ `pandas.api.types.is_unsigned_integer_dtype()`

## 迭代

类似list,`Series`是可迭代对象,直接迭代时抛出的是每一位的值,使用`items()`接口则会抛出和字典一样的index,value对


```python
for i in enumerate(s):
    print(i)
```

    (0, -0.3608478521120298)
    (1, 1.4707644792136825)
    (2, 0.5886541766129135)
    (3, -0.05504658364902078)
    (4, 0.41109401352028685)



```python
for k,v in c.items():
    print(f"{k}:{v}")
```

    a:1
    b:2
    c:3


## 取值

`Series`取值可以类似字典一样用index取,也可以类似list一样


```python
c["a"]
```




    1




```python
c[1]
```




    2



## 矢量化操作和标签对齐Series

使用原始numpy数组时通常不需要循环,在pandas中使用Series时也是如此.Series可以使用多数numpy的Universal Functions.


```python
b+2
```




    0    3
    1    4
    2    5
    dtype: int64


