
# 复数运算(cmath)

这个模块和math很像,只是面向的操作对象是复数.所以就只写独有的了


```python
from cmath import phase,polar,rect
```

## 极坐标转换

### `phase()`求相(相当于求`atan2(x.imag, x.real)`)


```python
phase(-1.0+0.0j)
```




    3.141592653589793




```python
phase(complex(-1.0,-0.0))
```




    -3.141592653589793



### polar(x) 转换为极坐标

polar(x) 相当于 (abs(x), phase(x)).


```python
polar(complex(-1.0,-0.0))
```




    (1.0, -3.141592653589793)



### rect(r,phi)已知半径和度数求以两边长为值的复数

$$r * (math.cos(phi) + math.sin(phi)*1j)$$


```python
from math import pi
```


```python
rect(1,pi/4)
```




    (0.7071067811865476+0.7071067811865475j)


