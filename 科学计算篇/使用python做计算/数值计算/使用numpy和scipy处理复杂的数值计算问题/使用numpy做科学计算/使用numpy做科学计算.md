
# 使用numpy做科学计算

numpy自带了许多数学工具.scipy则是其补充.通常情况下,这numpy提供的函数已经足够相对复杂的算法来使用了


```python
import numpy as np
import matplotlib.pyplot as plt
```


```python
%matplotlib inline
```

## 精度

科学计算的一个核心点在于精度,numpy的默认精度是64位的浮点数.最高的精度可以用`numpy.longdouble`(f16)表示，复数用`numpy.clongdouble`(c32)，但是这个具体能精确到多少是和你的电脑硬件相关的.

通常我们并不需要最高精度,这时可以使用`numpy.around(a, decimals=0, out=None)`来控制精度,其中a为要固定精度的数组,decimals则是精确到小数点后多少位(四舍五入).


```python
x = np.linspace(-np.pi, np.pi, 6,endpoint=True)
print(x)
```

    [-3.14159265 -1.88495559 -0.62831853  0.62831853  1.88495559  3.14159265]



```python
np.round(x)
```




    array([-3., -2., -1.,  1.,  2.,  3.])




```python
np.round(x,1)
```




    array([-3.1, -1.9, -0.6,  0.6,  1.9,  3.1])




```python
np.round(x,2)
```




    array([-3.14, -1.88, -0.63,  0.63,  1.88,  3.14])



## 数值计算


### 一元运算

函数|说明
---|---
abs/fabs|绝对值
sqrt|平方根
square|平方
exp|指数
log/log10/log2/log1p|分别为自然对数(e为底数)/底数为10的log/底数为2的log/log(1+x)
sign|求符号
ceil|大于等于该值的最小整数
floor|小于等于该值的最大整数
rint|四舍五入到最近的整数,dtype不变
modf|小数整数部分分离
isnan|---
isfinite/isinf|---
sin/sinh/cos/cosh/tan/tanh|三角函数,双曲三角函数
arcsin/arcsinh/arccos/arccosh/arctan/arctanh|反三角函数,反双曲三角函数
logical_not|计算各元素not x的真值


### 二元运算
函数|说明
---|---
add|加
subtract|减
multiply|乘
divide/floor_divide|除
power|乘方
maximun/fmax|最大值
minimum/fmin|最小值
mod|求模
copysign|将后面的符号付给前面


## 统计计算


**统计运算**|说明
---|---
sum|统计求和
mean|均值
average|加权求均值
median|中值
std|标准差
var|方差
min|最小值
argmin|最小值下标
max|最大值
argmax|最大值下标
ptp|最大值和最小值之差
sort|排序
argsort|排序下标
unique|找出所有整数(不会出现重复),并排序,</br>可选参数return_index=True,会额外返回一个记录下标的数组</br>可选return_inverse=True,会额外返回一个下标数组,数组长度为原始数组,表示原始数组中对应的下标
bincount|对整数数组个元素出现次数统计,可选参数weight,可以对各个元素加权


其中很多运算还有个`nanxxx`版本,用来求相应函数去掉nan值得结果

### 统计频数bincount


```python
a = np.random.randint(0,5,10)
a
```




    array([3, 1, 3, 2, 2, 4, 0, 3, 2, 2])




```python
np.bincount(a)
```




    array([1, 1, 4, 3, 1])




```python
np.bincount(a,np.random.rand(10))
```




    array([0.97517791, 0.90012648, 1.13136175, 0.79296358, 0.66850113])



### 相关性

numpy提供了3种算相关性的操作

+ `orrcoef(x, y=None, rowvar=1)` Pearson乘积矩相关系数。

其中rowvar=1表示向量是横置的,即每一列为向量的一个属性,每行是一个向量.为0则说明向量为竖置


```python
np.corrcoef([[1,1,0,1,1],[0,1,0,1,1]])
```




    array([[1.        , 0.61237244],
           [0.61237244, 1.        ]])




```python
np.corrcoef([[1,1,0,1,1],[0,1,0,1,1]],rowvar=0)
```

    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/lib/function_base.py:3183: RuntimeWarning: invalid value encountered in true_divide
      c /= stddev[:, None]
    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/lib/function_base.py:3184: RuntimeWarning: invalid value encountered in true_divide
      c /= stddev[None, :]





    array([[ 1., nan, nan, nan, nan],
           [nan, nan, nan, nan, nan],
           [nan, nan, nan, nan, nan],
           [nan, nan, nan, nan, nan],
           [nan, nan, nan, nan, nan]])



+ `correlate(a, v, mode='valid')`

两个1维序列的互相关。该函数计算信号处理文本中通常定义的相关性

$$ c_{av}[k] = sum_n a[n+k] * conj(v[n]) $$

其中a和v序列在必要时被填零，conj是共轭。mode 可选{‘valid’, ‘same’, ‘full’}


```python
np.correlate([1, 2, 3], [0, 1, 0.5])
```




    array([3.5])




```python
np.correlate([1, 2, 3], [0, 1, 0.5], "same")
```




    array([2. , 3.5, 3. ])




```python
np.correlate([1, 2, 3], [0, 1, 0.5], "full")
```




    array([0.5, 2. , 3.5, 3. , 0. ])



+ `cov(m, y=None, rowvar=True, bias=False, ddof=None, fweights=None, aweights=None)`

估计协方差矩阵,给定数据和权重.协方差表示两个变量一起变化的水平.如果我们检查N维样本,则协方差矩阵元素$C_{ij}$是$x_i$和$x_j$的协方差.$C_{ii}$元素是$x_i$的方差.其中rowvar一样是代表向量的是横置还是竖置
    
    
在概率论和统计学中,协方差Cov(X,Y)用于衡量两个变量的总体误差.而方差是协方差的一种特殊情况,即当两个变量是相同的情况.

期望值分别为$E(X)=\mu$与$E(Y)=\nu$的两个实数随机变量X 与Y 之间的协方差定义为:


$$ Cov(X, Y) = E((X - \mu) (Y - \nu))$$

$$ Cov(X, Y) = E(X \cdot Y) - \mu \nu$$

协方差矩阵是一个矩阵,其每个元素是各个向量元素之间的协方差.是从标量随机变量到高维度随机向量的自然推广.


```python
persontype=np.dtype({'names':['name','height','weight'],'formats':['S32','f','f']},align=True)
a = np.array([("Huang",175,70),("Hao",170,60),("Li",180,75)],dtype=persontype)
data = np.array([a["height"],a["weight"]])
data
```




    array([[175., 170., 180.],
           [ 70.,  60.,  75.]], dtype=float32)




```python
data_cov = np.cov(data)
data_cov #协方差矩阵
```




    array([[25.        , 37.5       ],
           [37.5       , 58.33333333]])




```python
#相关系数矩阵
data_corr = np.corrcoef(data)
data_corr 
```




    array([[1.        , 0.98198051],
           [0.98198051, 1.        ]])



也就是说身高与体重相关系数高达98.19%

### 直方图

通常在统计分析中最常见的是使用直方图观察数据的分布,numpy中有函数直接支持这个操作

+ 直方图统计histogram

    最基础的直方图,计算一组数据各个区间中的数据统计

    用法:

    `histogram(a,bins=10,range=None,normed=False,weights=None)`

    其中

    + bin指定统计区间个数,

    + range是一个长为2的元组,分别表示统计范围的最小值和最大值(None表示由数据决定)

    + normed=False表示返回在每个区间的个数,为True则表示返回一个在各个区间的概率密度

    + weight表示权值和前面一样用法



```python
c = np.random.rand(100)
y,x = np.histogram(c,bins=5,range=(0,1))
xticks = [str(x[i])+'~'+str(x[i+1]) for i in range(len(y))]
plt.axes([0.025,0.025,0.95,0.95])
plt.bar(range(len(y)), y, facecolor='#9999ff', edgecolor='white')
for i,j in zip(range(len(y)), y):
    plt.text(i,j,str(float(y[i])/sum(y)*100)+"%")

plt.xlim(-0.4,5)
plt.xticks(np.arange(5)+0.4,xticks)
plt.show()
```


![png](output_28_0.png)


+ `histogram2d(x, y[, bins, range, normed, weights])`

计算两个数据样本的二维直方图。


```python
xedges = [0, 1, 1.5, 3, 5]
yedges = [0, 2, 3, 4, 6]
x = np.random.normal(3, 1, 100)
y = np.random.normal(1, 1, 100)
H, xedges, yedges = np.histogram2d(y, x, bins=(xedges, yedges))
H = np.ones((4, 4)).cumsum().reshape(4, 4)
print(H[::-1])
fig = plt.figure(figsize=(7, 3))
ax = fig.add_subplot(131)
ax.set_title('imshow: equidistant')
im = plt.imshow(H, interpolation='nearest', origin='low',extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
```

    [[13. 14. 15. 16.]
     [ 9. 10. 11. 12.]
     [ 5.  6.  7.  8.]
     [ 1.  2.  3.  4.]]



![png](output_30_1.png)


+ `histogramdd(sample, bins=10, range=None, normed=False, weights=None)`

计算多维直方图


```python
r = np.random.randn(100,3)
H, edges = np.histogramdd(r, bins = (5, 8, 4))
H.shape, edges[0].size, edges[1].size, edges[2].size
```




    ((5, 8, 4), 6, 9, 5)



+ `digitize(x, bins, right=False)`

返回输入数组中每个值所属的bin的索引


```python
x = np.array([0.2, 6.4, 3.0, 1.6])
bins = np.array([0.0, 1.0, 2.5, 4.0, 10.0])
inds = np.digitize(x, bins)
inds
```




    array([1, 4, 3, 2])




```python
for n in range(x.size):
    print(bins[inds[n]-1], "<=", x[n], "<", bins[inds[n]])
```

    0.0 <= 0.2 < 1.0
    4.0 <= 6.4 < 10.0
    2.5 <= 3.0 < 4.0
    1.0 <= 1.6 < 2.5



```python
x = np.array([1.2, 10.0, 12.4, 15.5, 20.])
bins = np.array([0, 5, 10, 15, 20])
np.digitize(x,bins,right=True)
```




    array([1, 2, 3, 4, 4])




```python
np.digitize(x,bins,right=False)
```




    array([1, 3, 3, 4, 5])



## 多项式计算


多项式函数是变量的整数次幂与系数的乘积之和

$$ f(x)=a_nx^n+a_{n-1}x^{n-1}+...+a_2x^2+a_1x+a_0 $$

在numpy中可以用一个一维数组表示x各项的系数

numpy提供了`polynomial`模块专门处理多项式的

### 基本用法

多项式求值

可以用polynomia.polynomia()将系数转化为一元多项式对象,之后就可以像用函数一样用它了,比如下面的函数:

$$ f(x)=1+2x+3x^2 $$


```python
from numpy.polynomial import Polynomial as P
```


```python
v1 = np.array([1,2,3])
p = P(v1)
p
```




    Polynomial([1., 2., 3.], domain=[-1,  1], window=[-1,  1])



注意,长版本的打印输出有三个部分.

第一个是系数,第二个是域,第三个是窗口:他们分别可以通过访问属性`p.coef`,`p.domain`和`p.window`获得

要求x在某个值时f(x)的值,只要简单的代入就行


```python
p(0)
```




    1.0




```python
p(1)
```




    6.0



多项式是天生的universal function,他的参数可以是一个序列


```python
p(np.array([1,2,3,4]))
```




    array([ 6., 17., 34., 57.])



## 多项式运算

### 初等变换

一个多项式可以通过与一个非字符串的数值序列相加或者乘以一个标量来获得一个新的多项式


```python
p*2 #与标量相乘,多项式系数全部与标量相乘,类似向量与标量乘法 
```




    Polynomial([2., 4., 6.], domain=[-1.,  1.], window=[-1.,  1.])




```python
p+p # 与多项式相加,对应系数相加
```




    Polynomial([2., 4., 6.], domain=[-1.,  1.], window=[-1.,  1.])




```python
p+(2,5) # 与另一个序列相加,相当于把序列作为多项式,对应系数相加
```




    Polynomial([3., 7., 3.], domain=[-1.,  1.], window=[-1.,  1.])




```python
p*p # 与多项式相乘各项一一相乘,然后相同次数的系数相加
```




    Polynomial([ 1.,  4., 10., 12.,  9.], domain=[-1.,  1.], window=[-1.,  1.])




```python
p**2 # 幂,与乘法规则相同
```




    Polynomial([ 1.,  4., 10., 12.,  9.], domain=[-1.,  1.], window=[-1.,  1.])



除法:
    
`//`是多项式类的除法运算符，在这方面，多项式被视为整数.与之对应的是求余%,表示除后余下的项


```python
p//P([-1,1]) #相当于多项式分解
```




    Polynomial([5., 3.], domain=[-1.,  1.], window=[-1.,  1.])




```python
p%P([-1,1])
```




    Polynomial([6.], domain=[-1.,  1.], window=[-1.,  1.])




```python
P([ 5.,  3.])*P([-1,1])+[6]
```




    Polynomial([1., 2., 3.], domain=[-1.,  1.], window=[-1.,  1.])



如果要一次求出,可以使用`divmod`方法


```python
quo, rem = divmod(p, P([-1, 1]))
```


```python
quo
```




    Polynomial([5., 3.], domain=[-1.,  1.], window=[-1.,  1.])




```python
rem
```




    Polynomial([6.], domain=[-1.,  1.], window=[-1.,  1.])



### 多项式因式分解

多项式的根可以使用`np.roots()`方法获得

其意义是令该多项式等于0,则当变量为这些根时满足该等式


```python
r = p.roots()
r
```




    array([-0.33333333-0.47140452j, -0.33333333+0.47140452j])




```python
p(r)
```




    array([0.-2.77555756e-16j, 0.+2.77555756e-16j])




```python
np.poly(r)
```




    array([1.        , 0.66666667, 0.33333333])



### 多项式拟合

多项式的拟合使用`Chebyshev`模块 的fit(x,y,deg),来做

其中deg为最高次数
我们用1000个在${-\pi\over 2} \sim{\pi \over 2}$间的值拟合sin(x)


```python
from numpy.polynomial import Chebyshev as T
```


```python
x = np.linspace(-np.pi/2,np.pi/2,20)
y = np.sin(x)
a = T.fit(x,y,5)
xx,yy=a.linspace()
plt.plot(x,y,'o',color="red")
plt.plot(xx,yy,"--",lw=2,color = "blue")
plt.show()
```


![png](output_67_0.png)



```python
error = np.abs(a(x)-y)#polyval计算多项式的值
plt.plot(x,error)
plt.show()
```


![png](output_68_0.png)


做3,5,7次多项式的拟合,比较结果误差


```python
x = np.linspace(-np.pi/2,np.pi/2,1000)
y = np.sin(x)
for i in (3,5,7):
    a = T.fit(x,y,i)
    if i == 3: color = "red"
    elif i == 5: color = "blue"
    else : color = "yellow"
    error = np.abs(a(x)-y)
    plt.plot(x,error,color = color)
plt.show()
```


![png](output_70_0.png)


## 微积分

用deriv()和integ()可以分别计算多项式的微分和积分

$$ f(x)=3x^2+2x+1 $$

做微分是

$$ f^{'}(x)=6x+2 $$


```python
v1 = np.array([1,2,3])
p = P(v1)
p
```




    Polynomial([1., 2., 3.], domain=[-1,  1], window=[-1,  1])




```python
p.deriv()
```




    Polynomial([2., 6.], domain=[-1.,  1.], window=[-1.,  1.])




```python
p = P(v1)
```

$$ f(x)=3x^2+2x+1 $$

做积分是

$$ F(x)=x^3+x^2+x+N $$

N是无法预测的所以置0


```python
p.integ()
```




    Polynomial([0., 1., 1., 1.], domain=[-1.,  1.], window=[-1.,  1.])



## 傅里叶变换


将时域信号变换至频域加以分析的方法称为频谱分析.频谱分析的目的是把复杂的时间历程波形,经过傅里叶变换分解为若干单一的谐波分量来研究,以获得信号的频率结构以及各谐波和相位信息.

对信号进行频谱分析可以获得更多有用信息,如求得动态信号中的各个频率成分和频率分布范围,求出各个频率成分的幅值分布和能量分布,从而得到主要幅度和能量分布的频率值.

由时间函数求频谱函数的傅里叶变换公式就是将该时间函数乘以以频率为系数的指数函数之后,在负无限大到正无限大的整个区间内,对时间进行积分.这样就得到了与这个时间函数对应的.以频率为自变量的频谱函数.频谱函数是信号的频域表示方式.根据上述傅里叶变换公式,可以求出常数的频谱函数为频域中位于零频率处的一个冲激函数,表示直流信号就是一个频率等于零的信号.与此相反冲激函数的频谱函数等于常数,表示冲激函数含有无限多个、频率无限密集的正弦成分.同样的单个正弦波的频谱函数就是频域中位于该正弦波频率处的一对冲激函数.

np中用`np.fft`模块可以做傅里叶变换

### 傅里叶级数

假设:关于一个变量的任意一个周期函数 $f(x)$ ，不论连续或不连续,且函数 $f(x)$ 必须平方可积的，则 $f(x)$ 都可以近似的展开为正弦函数的级数，而正弦函数的参数为变量的倍数,大约就是:

$$f(x)=\sum_k c_k sin kx$$

#### 最常见的表达形式

周期为T的函数f(x)有：

$$
f(x)=a_0+\sum_{k=1}^\infty{[a_k sin (k{2\pi\over T}x)+b_k cos(k{2\pi\over T}x)]}
$$
$$
f(x)=a_0+\sum_{k=1}^\infty{\sqrt{a_k^2+b_k^2} [sin(k{2\pi\over T}x+\theta)]}
$$

然后因为有欧拉公式:

$$ cos x={ \frac {e^{ix}+e^{-ix}} 2} $$

$$ sin x={\frac {e^{ix}-e^{-ix}} 2i} $$

所以有:

$$ f(x) = \sum_{k=-\infty}^{+\infty}a_k e^{ik({2\pi\over T})t}$$


### 傅里叶变换:

假设一个函数（信号）是周期的，但是它的周期是无穷大,可以得出:

傅里叶正变换:

$$
F(\omega)=\int_{-\infty}^\infty f(t) e^{-i\omega t}dt
$$

傅里叶反变换:

$$
f(t)={1\over {2\pi}}\int_{-\infty}^\infty F(\omega) e^{-i\omega t}d\omega
$$

于是,我们可以利用傅里叶正变换变到分解状态（或者说频域），然后把它的分量分别处理，再利用反变换回去了.



### numpy中的接口

实域变频域后,函数表现形式有了变化,各个分量有了频率,周期.

numpy中获取和处理频率的工具有

+ fftfreq(n[, d])
    获取连续傅里叶变换分量频率
    
+ rfftfreq(n[, d])
    获取离散傅里叶变换分量频率
    
+ fftshift(x[, axes])
    将0频分量移动到中心
+ ifftshift(x[, axes])	The inverse of fftshift.
     上一操作的反操作
     
### 离散时间信号

在时间上依次出现的数值序列,例如，{…，0.5，1，2，-1，0，5，…}。相邻两个数之间的时间间隔可以是相等的，也可以是不等的。在前一情况下，设时间间隔为T秒,则离散信号可用符号x(nT)来表示（图1）。在间隔T归一化为1的条件下,T可以省略,即将x(nT)表示为x(n)。x(n)既可表示整个序列, 也可表示离散信号在nT瞬间的值。

### 离散傅里叶变换

简称DFT,

python的numpy里的fft模块就是用的这种变换

对于N点序列 $\left\{x[n]\right\}_{0\le n <N}$，它的离散傅里叶变换（DFT）为:

$$\hat{x}[k]=\sum_{n=0}^{N-1} e^{-i\frac{2\pi}{N}nk}x[n] \qquad k = 0,1,\ldots,N-1.$$

其中i是虚数单位

其逆变换为:

$$x\left[n\right]={1 \over N}\sum_{k=0}^{N-1} e^{ i\frac{2\pi}{N}nk}\hat{x}[k] \qquad n = 0,1,\ldots,N-1.$$



### numpy中实现的标准快速傅里叶变换

方法|说明
---|---
fft(a[, n, axis, norm])|	一维空间离散傅里叶变换
ifft(a[, n, axis, norm])|	一维空间离散傅里叶反变换
fft2(a[, s, axes, norm])|	二维空间离散傅里叶变换
ifft2(a[, s, axes, norm])|	二维空间离散傅里叶反变换
fftn(a[, s, axes, norm])|	N维空间离散傅里叶变换
ifftn(a[, s, axes, norm])|	N维空间离散傅里叶反变换

fft的参数是一个数组,这个数组可以理解为一个连续函数按一定周期采样的结果.而这个数组一般都是2的整数次幂.比如256,128,64这样

以下是标准傅里叶变换的例子

+ 一维空间

我们以一个矩形波为例子


```python
t = np.linspace(-1, 1, 128,endpoint=True)
tz = list(map(lambda x: 1 if (x > -0.5 and x<0.5) else 0,t))
plt.plot(t,tz)
plt.show()
```


![png](output_78_0.png)



```python
sp = np.fft.fft(tz)
re = np.fft.ifft(sp)#傅里叶逆变换
plt.plot(t,re)
plt.show()
```

    /Users/huangsizhe/anaconda3/lib/python3.6/site-packages/numpy/core/numeric.py:492: ComplexWarning: Casting complex values to real discards the imaginary part
      return array(a, dtype, copy=False, order=order)



![png](output_79_1.png)



```python
freq = np.fft.fftfreq(t.shape[-1])#获取频率
plt.plot(freq, sp.real)
plt.show()
```


![png](output_80_0.png)



```python
plt.plot(freq, sp.imag)
plt.show()
```


![png](output_81_0.png)


+ 二维空间(常用图像处理)


```python
a = np.mgrid[:5, :5][0]
a
```




    array([[0, 0, 0, 0, 0],
           [1, 1, 1, 1, 1],
           [2, 2, 2, 2, 2],
           [3, 3, 3, 3, 3],
           [4, 4, 4, 4, 4]])




```python
np.fft.fft2(a)
```




    array([[ 50.  +0.        j,   0.  +0.        j,   0.  +0.        j,
              0.  +0.        j,   0.  +0.        j],
           [-12.5+17.20477401j,   0.  +0.        j,   0.  +0.        j,
              0.  +0.        j,   0.  +0.        j],
           [-12.5 +4.0614962 j,   0.  +0.        j,   0.  +0.        j,
              0.  +0.        j,   0.  +0.        j],
           [-12.5 -4.0614962 j,   0.  +0.        j,   0.  +0.        j,
              0.  +0.        j,   0.  +0.        j],
           [-12.5-17.20477401j,   0.  +0.        j,   0.  +0.        j,
              0.  +0.        j,   0.  +0.        j]])



+ n维空间


```python
b = np.mgrid[:3, :3, :3][0]
b
```




    array([[[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]],
    
           [[1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]],
    
           [[2, 2, 2],
            [2, 2, 2],
            [2, 2, 2]]])




```python
np.fft.fftn(b, axes=(1, 2))
```




    array([[[ 0.+0.j,  0.+0.j,  0.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j]],
    
           [[ 9.+0.j,  0.+0.j,  0.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j]],
    
           [[18.+0.j,  0.+0.j,  0.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j]]])




```python
np.fft.fftn(b, (2, 2), axes=(0, 1))
```




    array([[[ 2.+0.j,  2.+0.j,  2.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j]],
    
           [[-2.+0.j, -2.+0.j, -2.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j]]])




```python
[X, Y] = np.meshgrid(2 * np.pi * np.arange(200) / 12,
                      2 * np.pi * np.arange(200) / 34)
S = np.sin(X) + np.cos(Y) + np.random.uniform(0, 1, X.shape)
FS = np.fft.fftn(S)
plt.imshow(np.log(np.abs(np.fft.fftshift(FS))**2))
plt.show()
```


![png](output_89_0.png)


numpy中其他的傅里叶变换还有


实数快速傅里叶变换:

方法|说明
---|---
rfft(a[, n, axis, norm])|	实数输入的一维空间离散傅里叶变换
irfft(a[, n, axis, norm])|	实数输入的一维空间离散傅里叶反变换
rfft2(a[, s, axes, norm])|	实数输入的二维空间离散傅里叶变换
irfft2(a[, s, axes, norm])|	实数输入的二维空间离散傅里叶反变换
rfftn(a[, s, axes, norm])|	实数输入的N维空间离散傅里叶变换
irfftn(a[, s, axes, norm])|	实数输入的N维空间离散傅里叶反变换


Hermitian傅里叶变换:

方法|说明
---|---
hfft(a[, n, axis, norm])|	计算实域中埃尔米特对称的信号的快速傅里叶变换
ihfft(a[, n, axis, norm])|	计算实域中埃尔米特对称的信号的快速傅里叶反变换

他们用法与上面的相同就不一一描述了

## 窗口函数

在信号处理中，窗函数(window function)是一种除在给定区间之外取值均为0的实函数。譬如：在给定区间内为常数而在区间外为0的窗函数被形象地称为矩形窗。任何函数与窗函数之积仍为窗函数，所以相乘的结果就像透过窗口“看”其他函数一样。窗函数在频谱分析、滤波器设计、波束形成、以及音频数据压缩（如在Ogg Vorbis音频格式中）等方面有广泛的应用。

numpy中提供了几种常见的窗函数

函数|说明
---|---
bartlett(M)	|Bartlett窗口函数
blackman(M)	|Blackman 窗口函数
hamming(M)	|Hamming窗口函数
hanning(M)	|Hanning窗口函数
kaiser(M, beta)	|Kaiser窗口函数

### bartlett窗

$$ w(n)=\frac{2}{N-1}\cdot\left(\frac{N-1}{2}-\left |n-\frac{N-1}{2}\right |\right)\, $$


```python
window = np.bartlett(51)
plt.plot(window)
plt.title("Bartlett window")
plt.ylabel("Amplitude")
plt.xlabel("Sample")
plt.show()
```


![png](output_93_0.png)


### Blackman窗

$$ 
w(n)=a_0 - a_1 \cos \left ( \frac{2 \pi n}{N-1} \right) + a_2 \cos \left ( \frac{4 \pi n}{N-1} \right)
$$
$$
{\displaystyle a_{0}=0.42;\quad a_{1}=0.5;\quad a_{2}=0.08\,} a_0=0.42;\quad a_1=0.5;\quad a_2=0.08\,
$$


```python
window = np.blackman(51)
plt.plot(window)
plt.title("Blackman window")
plt.ylabel("Amplitude")
plt.xlabel("Sample")
plt.show()
```


![png](output_95_0.png)


### Hamming窗

$$ w(n)=0.53836 - 0.46164\; \cos \left ( \frac{2 \pi n}{N-1} \right) $$


```python
window = np.hamming(51)
plt.plot(window)
plt.title("Hamming window")
plt.ylabel("Amplitude")
plt.xlabel("Sample")
plt.show()
```


![png](output_97_0.png)


### Hanning窗

$$ w(n)= 0.5\; \left(1 - \cos \left ( \frac{2 \pi n}{N-1} \right) \right) $$


```python
window = np.hanning(51)
plt.plot(window)
plt.title("Hanning window")
plt.ylabel("Amplitude")
plt.xlabel("Sample")
plt.show()
```


![png](output_99_0.png)


### Kaiser窗

$$ w(n)=\frac{I_0\Bigg (\pi\alpha \sqrt{1 - (\begin{matrix} \frac{2 n}{N-1} \end{matrix}-1)^2}\Bigg )} {I_0(\pi\alpha)} $$


```python
window = np.kaiser(51, 14)
plt.plot(window)
plt.title("Kaiser window")
plt.ylabel("Amplitude")
plt.xlabel("Sample")
plt.show()
```


![png](output_101_0.png)


## 卷积

卷积运算符经常出现在信号处理中,其中它模拟线性时不变系统对信号的影响.在概率理论中,两个独立随机变量的和根据它们各自的分布的卷积来分布.
**离散**卷积运算定义为:

$$ (a * v)[n] = \sum_{m = -\infty}^{\infty} a[m] v[n - m] $$

numpy提供了通用的卷积操作`convolve(a, v, mode='full')`


其中前两个参数都是一维的输入向量,而mode则提供了可选的三种运算规则,它可以有3种选项

+ full
    默认情况下，模式为“full”。这在每个重叠点处返回卷积，其输出形状为(N M-1,).在卷积的端点，信号不完全重叠，并且可以看到边界效应。
    
+ same
    模式same返回长度max（M，N）的输出。边界效应仍然可见。
    
+ valid
    模式'valid'返回长度为max(M,N)-min(M,N)+1.卷积产物仅针对信号完全重叠的点给出。信号边界外的值没有效果。


```python
np.convolve([1, 2, 3], [0, 1, 0.5])

# a相当于[...0,0,1,2, 3 ,0,0,...]
# v相当于[...0,0,0,1,0.5,0,0,...]
# [0*0.5+0*1+1*0+2*0+3*0,
# 0*0.5+1*1+2*0+3*0,
# 1*0.5+2*1+3*0,
# 1*0+2*0.5+3*1+0*0,
# 1*0+2*0+3*0.5+0*1+0*0]
```




    array([0. , 1. , 2.5, 4. , 1.5])




```python
np.convolve([1,2,3],[0,1,0.5], 'same')
```




    array([1. , 2.5, 4. ])




```python
np.convolve([1,2,3],[0,1,0.5], 'valid')
```




    array([2.5])



## 财务函数

numpy提供了简单的财务分析函数

### `fv(rate, nper, pmt, pv[, when])`求按比率计算n步后的值

例如:现在存100美元,且每月存100美元,假设利率是5%,6%,7%（每月）复利,求10年后的未来价值是多少



```python
a = np.array((0.05, 0.06, 0.07))/12
np.fv(a, 10*12, -100, -100)
```




    array([15692.92889434, 16569.87435405, 17509.44688102])



### `pv(rate, nper, pmt[, fv, when])`求按比率计算n步前的值

其实就是前一函数的反函数


```python
b = np.array([ 15692.92889434,  16569.87435405,  17509.44688102])
np.pv(a, 10*12, -100, b)
```




    array([-100., -100., -100.])



### `npv(rate, values)`净现值

values为现金流量时间序列的价值。
现金流“事件”之间的（固定）时间间隔必须与给出费率的时间间隔相同（即，如果费率是每年，则恰好一年被理解为在每个现金流事件之间流逝）。
按惯例，投资或“存款”是负数，收入或“提款”是正数;
值必须以初始投资开始，因此值[0]通常为负值。

净现值是一项投资所产生的未来现金流的折现值与项目投资成本之间的差值。
净现值指标是反映项目投资获利能力的指标。

+ 决策标准：
    + 净现值≥0 方案可行；
    + 净现值＜0 方案不可行；
    + 净现值均＞0 净现值最大的方案为最优方案。
+ 优点：
    + 考虑了资金时间价值，增强了投资经济性的评价；
    + 考虑了全过程的净现金流量，体现了流动性与收益性的统一；
    + 考虑了投资风险，风险大则采用高折现率，风险小则采用低折现率。
+ 缺点：
    + 净现值的计算较麻烦，难掌握；
    + 净现金流量的测量和折现率较难确定；
    + 不能从动态角度直接反映投资项目的实际收益水平；
    + 项目投资额不等时，无法准确判断方案的优劣。

numpy中的净现值使用这个公式

$$ \sum_{t=0}^{M-1}{\frac{values_t}{(1+rate)^{t}}}$$


```python
np.npv(0.281,[-100, 39, 59, 55, 20])
```




    -0.00847859163845488



### `pmt(rate, nper, pv, fv=0, when='end')`计算贷款本金加利息的付款


+ nper是计算次数
+ pv是本金


```python
np.pmt(0.075/12, 12*15, 200000)
```




    -1854.0247200054619



+ `ppmt(rate, per, nper, pv, fv=0.0, when='end')`
计算贷款本金的付款。


+ `ipmt(rate, per, nper, pv, fv=0.0, when='end')`
计算付款的利息部分。

### `irr(values)`返回内部收益率(IRR)

numpy使用公式

$$ \sum_{t=0}^M{\frac{v_t}{(1+irr)^{t}}} = 0 $$


```python
print(round(np.irr([-100, 39, 59, 55, 20]), 5))

print(round(np.irr([-100, 0, 0, 74]), 5))

print(round(np.irr([-100, 100, 0, -7]), 5))

print(round(np.irr([-100, 100, 0, 7]), 5))

print(round(np.irr([-5, 10.5, 1, -8, 1]), 5))
```

    0.28095
    -0.0955
    -0.0833
    0.06206
    0.0886


### `mirr(values, finance_rate, reinvest_rate)`修改后的内部收益率。

### `nper(rate, pmt, pv, fv=0, when='end')`计算定期付款的数量。

计算公式为:

$$ fv + pv*(1+rate)**nper + pmt*(1+rate*when)/rate*((1+rate)**nper-1) = 0 $$

如果`rate = 0`,那么:

$$ fv + pv + pmt*nper = 0 $$


```python
print(np.nper(0.07/12, -150, 8000))
```

    64.07334877066185


### rate(nper, pmt, pv, fv, when='end', guess=0.1, tol=1e-06, maxiter=100)计算每个周期的利率。

通过迭代求解(非线性)方程来计算利息率:


$$ fv + pv*(1+rate)**nper + pmt*(1+rate*when)/rate * ((1+rate)**nper - 1) = 0 $$

## 向量间计算

向量间计算多数都是对应项操作,这个ufunc可以直接支持.比较特殊的操作是点乘和求夹角

### 求模

向量中模的定义为各个项的平方和开方

$$ |v| = \sqrt {\sum_{i=0}^{N} {v_i^2}} $$

numpy中使用`np.linalg.norm(v)`来计算


```python
v_1 = np.array([3,5])
l_v1 = np.linalg.norm(v_1)
print(l_v1)
```

    5.830951894845301


### 点积(内积)

向量的点积为各项相乘的和,为一个标量.numpy中使用`np.linalg.dot`来计算其值,或者使用python3.6定义的矩阵乘法符号`@`来计算

$$a \cdot b = \sum_{i=0}^{n} a_i\cdot b_i $$


```python
v_1 = np.array([3,5])
v_2 = np.array([4,2])
v_1@v_2
```




    22



### 叉乘(外积)


$$ |C| = | v_1 \times v_2 |= |v_1| |v_2|sin<a,b> $$

或者在二维情况下可以看做:

$$ (x_1,y_1) \times (x_2,y_2)= x_1*y_2 -x_2*y_1 $$


C的方向用右手定则,右手4指从v_1不超过180度转向v_2时大拇指的方向即为C的方向.其值为新向量的模

numpy中没有直接计算的方法,这边需要迂回下,通过计算余弦,再转换为角度计算正弦再求出


```python
v_1 = np.array([3,5])
v_2 = np.array([4,2])

v_1_norm = np.linalg.norm(v_1)
v_2_norm = np.linalg.norm(v_2)
cos_theta = (v_1@v_2)/(v_1_norm * v_2_norm) # 计算余弦
theta = np.arccos(cos_theta)
cross_product = np.sin(theta)* (v_1_norm * v_2_norm)
cross_product
```




    14.000000000000002



## 矩阵计算

通常我们认为向量是一维的矩阵,numpy中通常使用二维数组代表矩阵,概括下矩阵计算的工具包括


> 向量,矩阵运算:

函数|说明
---|---
dot|向量乘法
vdot|向量点乘
inner|向量内积
outer|向量外积
matmul|矩阵乘法
trnsordot|张量乘法
einsum|评估操作数上的爱因斯坦求和约定
linalg.matrix_power|矩阵幂
kron|克罗内克积


> 矩阵分解

函数|说明
---|---
linalg.cholesky(a)|Cholesky 分解
linalg.qr(a[, mode])|QR分解
linalg.svd(a[, full_matrices, compute_uv])|奇异值分解

> 矩阵征值操作

函数|说明
---|---
linalg.norm(x[, ord, axis, keepdims])|矩阵或向量范数
linalg.cond(x[, p])|计算矩阵的条件数
linalg.det(a)|	计算矩阵行列式
linalg.matrix_rank(M[, tol])|使用SVD方法返回阵列的矩阵秩
linalg.slogdet(a)|	计算数组行列式的符号和（自然）对数
trace(a[, offset, axis1, axis2, dtype, out])|	计算对角线元素的和
diag|以一维数组的形式返回方阵的对角线(或非对角线)元素,或将一维数组转换为方阵(非对角线元素为0)
eig|计算方阵的本征值和本征向量


> 求解方程和求逆矩阵

函数|说明
---|---
linalg.solve(a, b)|解线性方程组Ax=b
linalg.tensorsolve(a, b[, axes])|解张量表达式Ax = b
linalg.lstsq(a, b[, rcond])|计算Ax=b的最小二乘解
linalg.inv(a)|计算方阵的逆
linalg.pinv(a[, rcond])|计算矩阵的Moore-Penrose伪逆
linalg.tensorinv(a[, ind])|计算N维数组的“逆”。



```python
A = np.arange(9).reshape(3,3)
print(A)
```

    [[0 1 2]
     [3 4 5]
     [6 7 8]]



```python
B = np.arange(13,22).reshape(3,3)
print(B)
```

    [[13 14 15]
     [16 17 18]
     [19 20 21]]


### 矩阵的秩


线性代数中
$$ \mathbf {A} ={\begin{bmatrix}1&2\\3&4\end{bmatrix}}
$$

一个矩阵A的列秩是A的线性独立的纵列的极大数目.类似地,行秩是A的线性独立的横行的极大数目.

矩阵的列秩和行秩总是相等的，因此它们可以简单地称作矩阵A的秩。通常表示为r(A)，rk(A)或rank A。

矩阵的行秩与列秩相等，是线性代数基本定理的重要组成部分。其基本证明思路是，矩阵可以看作线性映射的变换矩阵，列秩为像空间的维度，行秩为非零原像空间的维度，因此列秩与行秩相等，即像空间的维度与非零原像空间的维度相等（这里的非零原像空间是指约去了零空间后的商空间：原像空间）。这从矩阵的奇异值分解就可以看出来。

给出这一结果的两种证明. 第一个证明是简短的，仅用到向量的线性组合的基本性质. 第二个证明利用了正交性[1]. 第一个证明利用了列空间的基, 第二个证明利用了行向量空间的基. 第一个证明适用于定义在标量域上的矩阵，第二个证明适用于内积空间。二者都适用于实或复的欧氏空间，也都易于修改去证明当A是线性变换的情形.


```python
M_1 = np.matrix(np.arange(1,5).reshape(2,2))
M_1
```




    matrix([[1, 2],
            [3, 4]])




```python
np.linalg.matrix_rank(M_1)
```




    2



### 方阵的迹

迹就是方阵主对角线元素之和


```python
np.trace(M_1)
```




    5



### 转置矩阵(transpose)

将矩阵延对角线翻转


```python
M_1.T
```




    matrix([[1, 3],
            [2, 4]])



### 共轭矩阵(hermitian)(复数为元素)


```python
M_2 = np.matrix([[1+1j,2-4j],[3-1j,2+3j]])
M_2
```




    matrix([[1.+1.j, 2.-4.j],
            [3.-1.j, 2.+3.j]])




```python
M_2.H
```




    matrix([[1.-1.j, 3.+1.j],
            [2.+4.j, 2.-3.j]])



### 逆矩阵(inverse)


在线性代数中,给定一个n阶方阵$\mathbf{A}$，若存在一n阶方阵$ \mathbf {B}$ ，使得 $ \mathbf{AB}=\mathbf{BA}=\mathbf{I}_n$,其中 $ \mathbf{I}_n $为n阶单位矩阵，则称 $\mathbf{A} $是可逆的，且 $\mathbf {B} $是$\mathbf{A}$的逆矩阵，记作$\mathbf {A} ^{-1}$

只有正方形（n×n）的矩阵,即方阵,才可能、但非必然有逆矩阵.若方阵 $\mathbf{A}$的逆矩阵存在,则称 $\mathbf{A}$为非奇异方阵或可逆方阵.


性质有:

+ $ \left (A^{-1}  \right )^{-1}=A $
+ $ (\lambda A)^{-1}=\frac{1}{\lambda}\times A^{-1} $
+ $ (AB)^{-1}=B^{-1}A^{-1} $
+ $ \left (A^\mathrm{T} \right )^{-1}=\left (A^{-1} \right )^{\mathrm{T}}$ ($ A^{\mathrm{T}}$ 为A的转置)
+ $ \det(A^{-1})=\frac{1}{\det(A)} $（det为行列式）


```python
M_1.I
```




    matrix([[-2. ,  1. ],
            [ 1.5, -0.5]])



### 伴随矩阵(adjoint) 

在线性代数中,一个方形矩阵的伴随矩阵是一个类似于逆矩阵的概念.如果矩阵可逆,那么它的逆矩阵和它的伴随矩阵之间只差一个系数.然而伴随矩阵对不可逆的矩阵也有定义，并且不需要用到除法。

对n×n的矩阵A和B，有：

+ $\mathrm{adj}(\mathbf{I}) = \mathbf{I}$

+ $(\mathbf{AB}) = \mathrm{adj}(\mathbf{B})\,\mathrm{adj}(\mathbf{A})$

+ $\mathrm{adj}(\mathbf{A}^T) = \mathrm{adj}(\mathbf{A})^T $

+ $ \det\big(\mathrm{adj}(\mathbf{A})\big) = \det(\mathbf{A})^{n-1}$

+ $ \mathrm{adj}(k \mathbf{A}) = k^{n-1} \ \mathrm{adj}(\mathbf{A}) $

+ 当n>2时， $\mathrm{adj}(\mathrm{adj}(\mathbf{A})) =(\det \mathbf{A})^{n-2} \mathbf{A} $

+ 如果A可逆，那么 $ \mathrm{adj}(\mathbf{A}^{-1}) = \mathrm{adj}(\mathbf{A})^{-1} = \frac{A}{\det A} $

+ 如果A是对称矩阵，那么其伴随矩阵也是对称矩阵；如果A是反对称矩阵，那么当n为偶数时，A的伴随矩阵也是反对称矩阵，n为奇数时则是对称矩阵。

+ 如果A是（半）正定矩阵，那么其伴随矩阵也是（半）正定矩阵。

+ 如果矩阵A和B相似，那么 $\mathrm{adj}(\mathbf{A})$和 $\mathrm{adj}(\mathbf{B})$也相似.

+ 如果n>2，那么非零矩阵A是正交矩阵当且仅当 $ \mathrm{adj}(\mathbf{A}) = \pm A^T $


+ 伴随矩阵的秩

    当矩阵A可逆时,它的伴随矩阵也可逆,因此两者的秩一样,都是n.当矩阵A不可逆时,A的伴随矩阵的秩通常并不与A相同.当A的秩为n-1时,其伴随矩阵的秩为1,当A的秩小于n-1时,其伴随矩阵为零矩阵.

+ 伴随矩阵的特征值

    设矩阵A在复域中的特征值为 $\lambda_1, \lambda_2 \cdots \lambda_n$ (即为特征多项式的n个根),则A的伴随矩阵的特征值为$\lambda_2 \lambda_3 \cdots \lambda_{n}, \ \lambda_1 \lambda_3 \cdots \lambda_{n}, \cdots , \lambda_1 \lambda_2 \cdots \lambda_{n-1} $


```python
np.dot(np.linalg.det(M_1),M_1.I)
```




    matrix([[ 4., -2.],
            [-3.,  1.]])



### 矩阵的范数(matrix norms)


范数(norm),是具有"长度"概念的函数.在线性代数中其为向量空间内的所有向量赋予非零的正长度或大小.半范数反而可以为非零的向量赋予零长度.

举一个简单的例子,一个二维度的欧氏几何空间 $\mathbb {R} ^{2}$就有欧氏范数.在这个向量空间的元素(譬如：(3,7))常常在笛卡儿坐标系统被画成一个从原点出发的箭号.每一个向量的欧氏范数就是箭号的长度.

拥有范数的向量空间就是赋范向量空间.同样,拥有半范数的向量空间就是赋半范向量空间.


```python
np.linalg.norm(M_1)
```




    5.477225575051661



### 和和差

矩阵计算和和差要求两个矩阵形状一致,就是对应下标的各项计算的结果,numpy的ufunc刚好可以满足


```python
A+B
```




    array([[13, 15, 17],
           [19, 21, 23],
           [25, 27, 29]])




```python
A-B
```




    array([[-13, -13, -13],
           [-13, -13, -13],
           [-13, -13, -13]])



### 矩阵与标量的积

矩阵与标量的积就是标量在各项上的积.这也刚好ufunc就可以直接支持.


```python
A*3
```




    array([[ 0,  3,  6],
           [ 9, 12, 15],
           [18, 21, 24]])




```python
3*A
```




    array([[ 0,  3,  6],
           [ 9, 12, 15],
           [18, 21, 24]])



### 矩阵的内积(点积)

矩阵的乘法必须前一个矩阵的行数与后一个举证的列数相同.返回的是一个以前一个矩阵的行数为行数,后一个矩阵的列数为列数的新矩阵.

即形状上 $ (x,n)@ (n,y) -> (x,y) $,n是一致的


```python
C = np.arange(12).reshape(4,3)
C
```




    array([[ 0,  1,  2],
           [ 3,  4,  5],
           [ 6,  7,  8],
           [ 9, 10, 11]])




```python
D = np.arange(1,7).reshape(3,2)
D
```




    array([[1, 2],
           [3, 4],
           [5, 6]])




```python
C@D
```




    array([[ 13,  16],
           [ 40,  52],
           [ 67,  88],
           [ 94, 124]])



###  求特征值特征向量


```python
M_lamida=np.matrix([[3,0,-1],[2,4,2],[-1,0,3]])

np.linalg.eig(M_lamida)
```




    (array([4., 4., 2.]), matrix([[ 0.        ,  0.70710678,  0.40824829],
             [ 1.        ,  0.        , -0.81649658],
             [ 0.        , -0.70710678,  0.40824829]]))



第一项是特征值,第二项是特征向量

### 判断正定矩阵

正定矩阵的定义是:设M是n阶方阵,如果对任何非零向量z,都有$ z^TMz > 0$，其中$z^T$ 表示z的转置,就称M正定矩阵.


```python
M_4=np.arange(16).reshape(4,4)
M_4
```




    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])




```python
M_4 = M_4+M_4.T#将方阵转换成对称阵
M_4
```




    array([[ 0,  5, 10, 15],
           [ 5, 10, 15, 20],
           [10, 15, 20, 25],
           [15, 20, 25, 30]])




```python
lambdas,_ = np.linalg.eig(M_4)
```


```python
lambdas
```




    array([ 6.74165739e+01, -7.41657387e+00,  1.82694656e-15, -1.72637110e-15])




```python
#判断是否所有特征值都大于0
True if np.all(lambdas > 0) else False
```




    False



因此矩阵不是正定矩阵

还有一种方式是使用cholesky分解的方法:

Cholesky 分解是把一个对称正定的矩阵表示成一个下三角矩阵L和其转置的乘积的分解。它要求矩阵的所有特征值必须大于零，故分解的下三角的对角元也是大于零的。


```python
np.linalg.cholesky(np.arange(16).reshape(4,4))
```


    ---------------------------------------------------------------------------

    LinAlgError                               Traceback (most recent call last)

    <ipython-input-103-9d406430339a> in <module>()
    ----> 1 np.linalg.cholesky(np.arange(16).reshape(4,4))
    

    ~/anaconda3/lib/python3.6/site-packages/numpy/linalg/linalg.py in cholesky(a)
        612     t, result_t = _commonType(a)
        613     signature = 'D->D' if isComplexType(t) else 'd->d'
    --> 614     r = gufunc(a, signature=signature, extobj=extobj)
        615     return wrap(r.astype(result_t, copy=False))
        616 


    ~/anaconda3/lib/python3.6/site-packages/numpy/linalg/linalg.py in _raise_linalgerror_nonposdef(err, flag)
         90 
         91 def _raise_linalgerror_nonposdef(err, flag):
    ---> 92     raise LinAlgError("Matrix is not positive definite")
         93 
         94 def _raise_linalgerror_eigenvalues_nonconvergence(err, flag):


    LinAlgError: Matrix is not positive definite



```python
np.linalg.cholesky(M_4)
```


    ---------------------------------------------------------------------------

    LinAlgError                               Traceback (most recent call last)

    <ipython-input-104-d7b2b7d13630> in <module>()
    ----> 1 np.linalg.cholesky(M_4)
    

    ~/anaconda3/lib/python3.6/site-packages/numpy/linalg/linalg.py in cholesky(a)
        612     t, result_t = _commonType(a)
        613     signature = 'D->D' if isComplexType(t) else 'd->d'
    --> 614     r = gufunc(a, signature=signature, extobj=extobj)
        615     return wrap(r.astype(result_t, copy=False))
        616 


    ~/anaconda3/lib/python3.6/site-packages/numpy/linalg/linalg.py in _raise_linalgerror_nonposdef(err, flag)
         90 
         91 def _raise_linalgerror_nonposdef(err, flag):
    ---> 92     raise LinAlgError("Matrix is not positive definite")
         93 
         94 def _raise_linalgerror_eigenvalues_nonconvergence(err, flag):


    LinAlgError: Matrix is not positive definite


报错了,因此可以看出不是正定的

我们试试测试一个单位矩阵


```python
i=np.eye(4)
np.linalg.cholesky(i)
```




    array([[1., 0., 0., 0.],
           [0., 1., 0., 0.],
           [0., 0., 1., 0.],
           [0., 0., 0., 1.]])



### 奇异值分解


```python
arr = np.arange(9).reshape((3, 3)) + np.diag([1, 0, 1])
arr
```




    array([[1, 1, 2],
           [3, 4, 5],
           [6, 7, 9]])




```python
uarr, spec, vharr = np.linalg.svd(arr)
```


```python
uarr
```




    array([[-0.1617463 , -0.98659196,  0.02178164],
           [-0.47456365,  0.09711667,  0.87484724],
           [-0.86523261,  0.13116653, -0.48390895]])




```python
spec
```




    array([14.88982544,  0.45294236,  0.29654967])




```python
vharr
```




    array([[-0.45513179, -0.54511245, -0.70406496],
           [ 0.20258033,  0.70658087, -0.67801525],
           [-0.86707339,  0.45121601,  0.21115836]])



### 矩阵QR分解


```python
X = np.random.randn(5,5)
X
```




    array([[ 0.31973556,  0.53006218,  1.47774619, -0.95530633,  1.14828731],
           [ 0.87549778,  0.62172745,  1.39146104, -2.39668243,  1.72502563],
           [-0.72235292, -1.18862732, -1.28830878,  1.54872527, -1.81707944],
           [-1.16188315, -0.04933121,  1.07940732,  0.32254145, -0.19191908],
           [-0.85629659,  0.30374907, -0.46223666,  0.45378814, -0.90791106]])




```python
mat = X.T.dot(X)
mat
```




    array([[ 3.47373724,  1.36962695,  1.76298915, -4.28579449,  4.19040572],
           [ 1.36962695,  2.17504291,  2.98607347, -3.71538581,  3.57468019],
           [ 1.76298915,  2.98607347,  7.15842002, -6.60343077,  6.65065346],
           [-4.28579449, -3.71538581, -6.60343077,  9.36520347, -8.51936273],
           [ 4.19040572,  3.57468019,  6.65065346, -8.51936273,  8.45719029]])




```python
q,r=np.linalg.qr(mat)
```


```python
q
```




    array([[-0.4772518 ,  0.63087517, -0.02426549, -0.30372681, -0.5304606 ],
           [-0.18817109, -0.43477453,  0.80580342, -0.27151609, -0.22917812],
           [-0.24221456, -0.63754628, -0.57704497, -0.17420213, -0.41417335],
           [ 0.58881918,  0.06843113, -0.09120663, -0.80006093,  0.01389287],
           [-0.57571385, -0.04265619, -0.09376824, -0.40445663,  0.7031048 ]])




```python
r
```




    array([[-7.27862581e+00, -6.03189093e+00, -1.08542560e+01,
             1.47631050e+01, -1.41687010e+01],
           [ 0.00000000e+00, -2.39207993e+00, -5.48543840e+00,
             4.12582150e+00, -4.09439745e+00],
           [ 0.00000000e+00,  0.00000000e+00, -1.78866529e+00,
             8.65279871e-01, -1.07491238e+00],
           [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
            -5.86191244e-01, -6.43715612e-03],
           [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
             0.00000000e+00,  3.13256668e-02]])



## 张量计算

将数据继续扩展,那么矩阵,向量,常数就都是张量的特殊形式了.

张量(tensor)是一个可用来表示在一些矢量、标量和其他张量之间的线性关系的多线性函数,这些线性关系的基本例子有内积、外积、线性映射以及笛卡儿积.其坐标在 n  维空间内,有$ n^r $ 个分量的一种量,其中每个分量都是坐标的函数,而在坐标变换时,这些分量也依照某些规则作线性变换. r称为该张量的秩或阶(与矩阵的秩和阶均无关系)

在同构的意义下,第零阶张量(r=0)即为标量，第一阶张量(r=1)即为矢量或者说向量,第二阶张量(r=2)则成为矩阵.由于变换方式的不同,张量分成"协变张量"(指标在下者)、"逆变张量"(指标在上者)、"混合张量"(指标在上和指标在下两者都有)三类.

一个张量的大小是一个向量,向量的第 n 个元素描述了张量在第 n 维上的大小,在numpy中,张量的大小即为shape


### 张量加减

张量加减依然是ufunc,这边不做复述.

### Hadamard Product

Hadamard Product 要求形状一致,本质上也还是ufunc


```python

A = np.array([
  [[1,2,3],    [4,5,6],    [7,8,9]],
  [[11,12,13], [14,15,16], [17,18,19]],
  [[21,22,23], [24,25,26], [27,28,29]],
  ])
B = np.array([
  [[1,2,3],    [4,5,6],    [7,8,9]],
  [[11,12,13], [14,15,16], [17,18,19]],
  [[21,22,23], [24,25,26], [27,28,29]],
  ])
C = A * B
C
```




    array([[[  1,   4,   9],
            [ 16,  25,  36],
            [ 49,  64,  81]],
    
           [[121, 144, 169],
            [196, 225, 256],
            [289, 324, 361]],
    
           [[441, 484, 529],
            [576, 625, 676],
            [729, 784, 841]]])



### 张量的积算子


张量积算子通常表示为中间带有小x的圆$\otimes $.给定具有q维度的张量A和具有r维度的张量B，这些张量的乘积将是具有q + r的量级的新张量,或者换句话说q + r维度.

需要注意张量的积算子在r为1,2时是区别于向量点乘,矩阵点乘的.它要求形状一致

张量积算子不限于张量,也可以在矩阵和向量上执行，这可以是练习的好地方，以便发展更高维度的直觉.


在向量上:

$$ a = (a_1, a_2)$$

$$b = (b_1, b_2)$$

$$c = a \otimes b $$

$$c = {\begin{bmatrix}
a_1 * b\\
a_2 * b
\end{bmatrix}
}$$

在矩阵上:

$$
A = {\begin{bmatrix} 
a_{1,1}&a_{1,2}\\
a_{2,1}&a_{2,2} 
\end{bmatrix}}
$$

$$   
B = {\begin{bmatrix} b_{1,1}& b_{1,2}\\
b_{2,1} & b_{2,2}
\end{bmatrix}}
$$

$$
C = A \otimes B
$$

$$
C ={\begin{bmatrix}
     a_{1,1} * {\begin{bmatrix}b_{1,1}&b_{1,2}\\b_{2,1}&b_{2,2}\end{bmatrix}}&a_{1,2}*{\begin{bmatrix}b_{1,1}&b_{1,2}\\b_{2,1}&b_{2,2}\end{bmatrix}}\\
     a_{2,1} * {\begin{bmatrix}b_{1,1}&b_{1,2}\\b_{2,1}&b_{2,2}\end{bmatrix}}&a_{2,2}*{\begin{bmatrix}b_{1,1}&b_{1,2}\\b_{2,1}&b_{2,2}\end{bmatrix}}
\end{bmatrix}} 
$$

$$     
C = {\begin{bmatrix} 
a_{1,1} * b_{1,1}&a_{1,1} * b_{1,2}& a_{1,2} * b_{1,1}& a_{1,2} * b_{1,2}\\
a_{1,1} * b_{2,1}&a_{1,1} * b_{2,2}& a_{1,2} * b_{2,1}& a_{1,2} * b_{2,2}\\
a_{2,1} * b_{1,1}&a_{2,1} * b_{1,2}& a_{2,2} * b_{1,1}& a_{2,2} * b_{1,2}\\
a_{2,1} * b_{2,1}&a_{2,1} * b_{2,2}& a_{2,2} * b_{2,1}& a_{2,2} * b_{2,2}
\end{bmatrix}} 
$$

注意上式中的值为压扁为矩阵后的形态,在拆解时每次拆解都是一层


在numpy中张量的积算子需要指定axes为0


```python
np.tensordot(np.arange(4).reshape(2,2),np.arange(4).reshape(2,2),axes=0).shape
```




    (2, 2, 2, 2)


