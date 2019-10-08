
# pandas的函数操作

由于python本身对函数式编程的支持,以及pandas底层依赖的numpy优秀的向量化计算能力,pandas可以使用类似Universal  Function的方式向量化的求值.

本文例子依然使用[iris]()数据集


```python
import pandas as pd
iris_data = pd.read_csv("source/iris.csv")
iris_data[:5]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sepal_length</th>
      <th>sepal_width</th>
      <th>petal_length</th>
      <th>petal_width</th>
      <th>class</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5.1</td>
      <td>3.5</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4.9</td>
      <td>3.0</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4.7</td>
      <td>3.2</td>
      <td>1.3</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4.6</td>
      <td>3.1</td>
      <td>1.5</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.0</td>
      <td>3.6</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
  </tbody>
</table>
</div>



> 例:求出iris三类的信息熵


```python
import scipy as sp
slogs = lambda x:sp.log(x)*x
entropy = lambda x:sp.exp((slogs(x.sum())-x.map(slogs).sum())/x.sum())
iris_data.groupby("class").agg(entropy)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sepal_length</th>
      <th>sepal_width</th>
      <th>petal_length</th>
      <th>petal_width</th>
    </tr>
    <tr>
      <th>class</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Iris-setosa</th>
      <td>49.878745</td>
      <td>49.695242</td>
      <td>49.654909</td>
      <td>45.810069</td>
    </tr>
    <tr>
      <th>Iris-versicolor</th>
      <td>49.815081</td>
      <td>49.680665</td>
      <td>49.694505</td>
      <td>49.452305</td>
    </tr>
    <tr>
      <th>Iris-virginica</th>
      <td>49.772059</td>
      <td>49.714500</td>
      <td>49.761700</td>
      <td>49.545918</td>
    </tr>
  </tbody>
</table>
</div>



### 广播

所谓广播就是一个矢量和一个标量的运算,所有矢量中元素都被同样的操作,pandas可以支持这种操作


```python
data1 = iris_data[:10].copy()
data1
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sepal_length</th>
      <th>sepal_width</th>
      <th>petal_length</th>
      <th>petal_width</th>
      <th>class</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5.1</td>
      <td>3.5</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4.9</td>
      <td>3.0</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4.7</td>
      <td>3.2</td>
      <td>1.3</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4.6</td>
      <td>3.1</td>
      <td>1.5</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.0</td>
      <td>3.6</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5.4</td>
      <td>3.9</td>
      <td>1.7</td>
      <td>0.4</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>6</th>
      <td>4.6</td>
      <td>3.4</td>
      <td>1.4</td>
      <td>0.3</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>7</th>
      <td>5.0</td>
      <td>3.4</td>
      <td>1.5</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>8</th>
      <td>4.4</td>
      <td>2.9</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>9</th>
      <td>4.9</td>
      <td>3.1</td>
      <td>1.5</td>
      <td>0.1</td>
      <td>Iris-setosa</td>
    </tr>
  </tbody>
</table>
</div>




```python
data1*10
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sepal_length</th>
      <th>sepal_width</th>
      <th>petal_length</th>
      <th>petal_width</th>
      <th>class</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>51.0</td>
      <td>35.0</td>
      <td>14.0</td>
      <td>2.0</td>
      <td>Iris-setosaIris-setosaIris-setosaIris-setosaIr...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>49.0</td>
      <td>30.0</td>
      <td>14.0</td>
      <td>2.0</td>
      <td>Iris-setosaIris-setosaIris-setosaIris-setosaIr...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>47.0</td>
      <td>32.0</td>
      <td>13.0</td>
      <td>2.0</td>
      <td>Iris-setosaIris-setosaIris-setosaIris-setosaIr...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>46.0</td>
      <td>31.0</td>
      <td>15.0</td>
      <td>2.0</td>
      <td>Iris-setosaIris-setosaIris-setosaIris-setosaIr...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>50.0</td>
      <td>36.0</td>
      <td>14.0</td>
      <td>2.0</td>
      <td>Iris-setosaIris-setosaIris-setosaIris-setosaIr...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>54.0</td>
      <td>39.0</td>
      <td>17.0</td>
      <td>4.0</td>
      <td>Iris-setosaIris-setosaIris-setosaIris-setosaIr...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>46.0</td>
      <td>34.0</td>
      <td>14.0</td>
      <td>3.0</td>
      <td>Iris-setosaIris-setosaIris-setosaIris-setosaIr...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>50.0</td>
      <td>34.0</td>
      <td>15.0</td>
      <td>2.0</td>
      <td>Iris-setosaIris-setosaIris-setosaIris-setosaIr...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>44.0</td>
      <td>29.0</td>
      <td>14.0</td>
      <td>2.0</td>
      <td>Iris-setosaIris-setosaIris-setosaIris-setosaIr...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>49.0</td>
      <td>31.0</td>
      <td>15.0</td>
      <td>1.0</td>
      <td>Iris-setosaIris-setosaIris-setosaIris-setosaIr...</td>
    </tr>
  </tbody>
</table>
</div>




```python
data1["sepal_length"]*10
```




    0    51.0
    1    49.0
    2    47.0
    3    46.0
    4    50.0
    5    54.0
    6    46.0
    7    50.0
    8    44.0
    9    49.0
    Name: sepal_length, dtype: float64



### 使用numpy的universal functiion


```python
import numpy as np
np.exp(data1["sepal_length"])
f_npexp = np.frompyfunc(lambda x :np.exp(x)+1,1,1)
f_npexp(data1["sepal_length"])
```




    0    165.022
    1     135.29
    2    110.947
    3    100.484
    4    149.413
    5    222.406
    6    100.484
    7    149.413
    8    82.4509
    9     135.29
    Name: sepal_length, dtype: object


