
# 符号计算

符号计算又称计算机代数,通俗地说就是用计算机推导数学公式,如对表达式进行因式分解,化简,微分,积分,解代数方程,求解常微分方程等.

符号计算主要是操作数学对象与表达式.这些数学对象与表达式可以直接表现自己,它们不是估计/近似值.表达式/对象是未经估计的变量只是以符号形式呈现.

## 使用SymPy进行符号计算

[SymPy](https://www.sympy.org/zh/index.html)是python环境下的符号计算库,他可以用于:

+ 简化数学表达式
+ 计算微分,积分与极限
+ 求方程的解
+ 矩阵运算以及各种数学函数.

所有这些功能都通过数学符号完成.
下面是使用SymPy做符号计算与一般计算的对比:

> 一般的计算


```python
import math
math.sqrt(3)
```




    1.7320508075688772




```python
math.sqrt(27)
```




    5.196152422706632



> 使用SymPy进行符号计算


```python
import sympy
sympy.sqrt(3)
```




$\displaystyle \sqrt{3}$




```python
sympy.sqrt(27)
```




$\displaystyle 3 \sqrt{3}$



SymPy程序库由若干核心能力与大量的可选模块构成.SymPy的主要功能:

+ 包括基本算术与公式简化,以及模式匹配函数,如三角函数/双曲函数/指数函数与对数函数等(核心能力)

+ 支持多项式运算,例如基本算术/因式分解以及各种其他运算(核心能力)

+ 微积分功能,包括极限/微分与积分等(核心能力)

+ 各种类型方程式的求解,例如多项式求解/方程组求解/微分方程求解(核心能力)

+ 离散数学(核心能力)

+ 矩阵表示与运算功能(核心能力)

+ 几何函数(核心能力)

+ 借助pyglet外部模块画图

+ 物理学支持

+ 统计学运算，包括概率与分布函数

+ 各种打印功能

+ LaTeX代码生成功能

## 使用SymPy的工作流

使用SymPy做符号计算不同于一般计算,它的流程是:

+ 在构建算式前申明符号,然后利用声明的符号构建算式
+ 利用算式进行推导,计算等符号运算操作
+ 输出结果

下面是一个简单的例子,就当作SymPy的helloworld吧


```python
import sympy as sp
x, y = sp.symbols('x y') #声明符号x,y
expr = x + 2*y # 构造算式
expr
```




$\displaystyle x + 2 y$




```python
expr + 1 # 在算式之上构建新算式
```




$\displaystyle x + 2 y + 1$




```python
expr + x # 新构建的算式可以明显的化简就会自动化简
```




$\displaystyle 2 x + 2 y$




```python
x*(expr) # 新算式不能明显的化简,比如这个例子,就不会自动化简
```




$\displaystyle x \left(x + 2 y\right)$




```python
expand_expr = sp.expand(x*(expr)) # 手动化简新算式
expand_expr
```




$\displaystyle x^{2} + 2 x y$




```python
sp.factor(expand_expr) #  将化简的式子做因式分解
```




$\displaystyle x \left(x + 2 y\right)$




```python
sp.latex(expand_expr) # 输出符号的latex代码
```




    'x^{2} + 2 x y'


