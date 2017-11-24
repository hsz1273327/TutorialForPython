
# 有理数(fractions)

有理数(fractions)模块提供了一种用来表示有理数的数据类型,它可以用整数,浮点数,高精度数或者数字和除号字符串创建


```python
from fractions import Fraction
Fraction(16, -10)
```




    Fraction(-8, 5)




```python
Fraction(123)
```




    Fraction(123, 1)




```python
Fraction()
```




    Fraction(0, 1)




```python
Fraction('3/7')
```




    Fraction(3, 7)




```python
Fraction('1.414213 \t\n')
```




    Fraction(1414213, 1000000)




```python
Fraction('-.125')
```




    Fraction(-1, 8)




```python
Fraction('7e-6')
```




    Fraction(7, 1000000)




```python
Fraction(2.25)
```




    Fraction(9, 4)




```python
Fraction(1.1)
```




    Fraction(2476979795053773, 2251799813685248)




```python
from decimal import Decimal
Fraction(Decimal('1.1'))
```




    Fraction(11, 10)


