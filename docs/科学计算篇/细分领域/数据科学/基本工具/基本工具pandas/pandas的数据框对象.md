
# pandas的数据框对象

所谓数据框(Dataframe)是这一种最常见的数据分析用的数据结构,它针对的是二维数据.数据帧有如下特点:

+ 列是不同的类型
+ 大小可变
+ 标记轴(行和列)
+ 可以对行和列执行算术运算

数据框是数据科学中一种非常的重要的数据结构,几乎所有的工作都建立在其上


```python
import pandas as pd
```

## 数据框的构造


从python对象构造数据框对象可以有如下途径

### 从二维列表转换

pandas可以将二维列表以表格的形式组合


```python
names = ['Bob','Jessica','Mary','John','Mel']
births = [1968, 1955, 1977,1978, 1973]
weight = [69,89,76,90,78]
table_o = list(zip(names,births,weight))
table_o
```




    [('Bob', 1968, 69),
     ('Jessica', 1955, 89),
     ('Mary', 1977, 76),
     ('John', 1978, 90),
     ('Mel', 1973, 78)]




```python
pd.DataFrame(table_o,columns =["name","births","weight"])# columns指定列标签
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
      <th>name</th>
      <th>births</th>
      <th>weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bob</td>
      <td>1968</td>
      <td>69</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Jessica</td>
      <td>1955</td>
      <td>89</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mary</td>
      <td>1977</td>
      <td>76</td>
    </tr>
    <tr>
      <th>3</th>
      <td>John</td>
      <td>1978</td>
      <td>90</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Mel</td>
      <td>1973</td>
      <td>78</td>
    </tr>
  </tbody>
</table>
</div>



### 从字典中直接生成

pandas也允许将数据放在字典内,这样key是每列的标题,value就会按顺序填入


```python
table_dict = {"names":['Bob','Jessica','Mary','John','Mel'],
    "births":[1968, 1955, 1977,1978, 1973],
    "weight":[69,89,76,90,78]
}
table_dict
```




    {'names': ['Bob', 'Jessica', 'Mary', 'John', 'Mel'],
     'births': [1968, 1955, 1977, 1978, 1973],
     'weight': [69, 89, 76, 90, 78]}




```python
pd.DataFrame(table_dict)
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
      <th>names</th>
      <th>births</th>
      <th>weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bob</td>
      <td>1968</td>
      <td>69</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Jessica</td>
      <td>1955</td>
      <td>89</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mary</td>
      <td>1977</td>
      <td>76</td>
    </tr>
    <tr>
      <th>3</th>
      <td>John</td>
      <td>1978</td>
      <td>90</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Mel</td>
      <td>1973</td>
      <td>78</td>
    </tr>
  </tbody>
</table>
</div>



### 从包裹字典的列表中获取

另一种则是按行获取,每个字典是表格中的一行


```python
table_row = [{"names":'Bob',
    "births":1968,
    "weight":69
},
{"names":'Jessica',
    "births":1955,
    "weight":89
},
{"names":'Mary',
    "births":1977,
    "weight":76
},
{"names":'John',
    "births":1978,
    "weight":90
},
{"names":'Mel',
    "births": 1973,
    "weight":78
}]
table_row
```




    [{'names': 'Bob', 'births': 1968, 'weight': 69},
     {'names': 'Jessica', 'births': 1955, 'weight': 89},
     {'names': 'Mary', 'births': 1977, 'weight': 76},
     {'names': 'John', 'births': 1978, 'weight': 90},
     {'names': 'Mel', 'births': 1973, 'weight': 78}]




```python
pd.DataFrame(table_row)
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
      <th>births</th>
      <th>names</th>
      <th>weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1968</td>
      <td>Bob</td>
      <td>69</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1955</td>
      <td>Jessica</td>
      <td>89</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1977</td>
      <td>Mary</td>
      <td>76</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1978</td>
      <td>John</td>
      <td>90</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1973</td>
      <td>Mel</td>
      <td>78</td>
    </tr>
  </tbody>
</table>
</div>



## 数据框的基本操作

我们以常见的数据集[iris]()作为例子,如何读入外部数据可以看[数据获取与保存]部分


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



### 数据过滤

就像透视表一样,我们可以有选择性的查看表格


```python
iris_data[iris_data["class"]=="Iris-virginica"][::10]
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
      <th>100</th>
      <td>6.3</td>
      <td>3.3</td>
      <td>6.0</td>
      <td>2.5</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>110</th>
      <td>6.5</td>
      <td>3.2</td>
      <td>5.1</td>
      <td>2.0</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>120</th>
      <td>6.9</td>
      <td>3.2</td>
      <td>5.7</td>
      <td>2.3</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>130</th>
      <td>7.4</td>
      <td>2.8</td>
      <td>6.1</td>
      <td>1.9</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>140</th>
      <td>6.7</td>
      <td>3.1</td>
      <td>5.6</td>
      <td>2.4</td>
      <td>Iris-virginica</td>
    </tr>
  </tbody>
</table>
</div>




```python
iris_data[iris_data["petal_width"]>iris_data["petal_width"].mean()][::10]
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
      <th>50</th>
      <td>7.0</td>
      <td>3.2</td>
      <td>4.7</td>
      <td>1.4</td>
      <td>Iris-versicolor</td>
    </tr>
    <tr>
      <th>63</th>
      <td>6.1</td>
      <td>2.9</td>
      <td>4.7</td>
      <td>1.4</td>
      <td>Iris-versicolor</td>
    </tr>
    <tr>
      <th>75</th>
      <td>6.6</td>
      <td>3.0</td>
      <td>4.4</td>
      <td>1.4</td>
      <td>Iris-versicolor</td>
    </tr>
    <tr>
      <th>88</th>
      <td>5.6</td>
      <td>3.0</td>
      <td>4.1</td>
      <td>1.3</td>
      <td>Iris-versicolor</td>
    </tr>
    <tr>
      <th>100</th>
      <td>6.3</td>
      <td>3.3</td>
      <td>6.0</td>
      <td>2.5</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>110</th>
      <td>6.5</td>
      <td>3.2</td>
      <td>5.1</td>
      <td>2.0</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>120</th>
      <td>6.9</td>
      <td>3.2</td>
      <td>5.7</td>
      <td>2.3</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>130</th>
      <td>7.4</td>
      <td>2.8</td>
      <td>6.1</td>
      <td>1.9</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>140</th>
      <td>6.7</td>
      <td>3.1</td>
      <td>5.6</td>
      <td>2.4</td>
      <td>Iris-virginica</td>
    </tr>
  </tbody>
</table>
</div>



### 排序sort

比如我们根据sepal_length做降序排列


```python
biggest5_sl_iris = iris_data.sort_values('sepal_length',ascending=False)[:5]
```


```python
biggest5_sl_iris
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
      <th>131</th>
      <td>7.9</td>
      <td>3.8</td>
      <td>6.4</td>
      <td>2.0</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>135</th>
      <td>7.7</td>
      <td>3.0</td>
      <td>6.1</td>
      <td>2.3</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>122</th>
      <td>7.7</td>
      <td>2.8</td>
      <td>6.7</td>
      <td>2.0</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>117</th>
      <td>7.7</td>
      <td>3.8</td>
      <td>6.7</td>
      <td>2.2</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>118</th>
      <td>7.7</td>
      <td>2.6</td>
      <td>6.9</td>
      <td>2.3</td>
      <td>Iris-virginica</td>
    </tr>
  </tbody>
</table>
</div>



再把序号(index)排排序


```python
biggest5_sl_iris.sort_index(ascending=False)
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
      <th>135</th>
      <td>7.7</td>
      <td>3.0</td>
      <td>6.1</td>
      <td>2.3</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>131</th>
      <td>7.9</td>
      <td>3.8</td>
      <td>6.4</td>
      <td>2.0</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>122</th>
      <td>7.7</td>
      <td>2.8</td>
      <td>6.7</td>
      <td>2.0</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>118</th>
      <td>7.7</td>
      <td>2.6</td>
      <td>6.9</td>
      <td>2.3</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>117</th>
      <td>7.7</td>
      <td>3.8</td>
      <td>6.7</td>
      <td>2.2</td>
      <td>Iris-virginica</td>
    </tr>
  </tbody>
</table>
</div>



### 排名rank


```python
biggest5_sl_iris.rank(method="min",numeric_only = True)
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
  </thead>
  <tbody>
    <tr>
      <th>131</th>
      <td>5.0</td>
      <td>4.0</td>
      <td>2.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>135</th>
      <td>1.0</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>122</th>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>117</th>
      <td>1.0</td>
      <td>4.0</td>
      <td>3.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>118</th>
      <td>1.0</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>4.0</td>
    </tr>
  </tbody>
</table>
</div>



### 选择,切片操作

切片可以用来准确的提取需要的数据

pandas支持多种切片方式

#### 间隔切片


```python
iris_data[::20]#每20行取一次
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
      <th>20</th>
      <td>5.4</td>
      <td>3.4</td>
      <td>1.7</td>
      <td>0.2</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>40</th>
      <td>5.0</td>
      <td>3.5</td>
      <td>1.3</td>
      <td>0.3</td>
      <td>Iris-setosa</td>
    </tr>
    <tr>
      <th>60</th>
      <td>5.0</td>
      <td>2.0</td>
      <td>3.5</td>
      <td>1.0</td>
      <td>Iris-versicolor</td>
    </tr>
    <tr>
      <th>80</th>
      <td>5.5</td>
      <td>2.4</td>
      <td>3.8</td>
      <td>1.1</td>
      <td>Iris-versicolor</td>
    </tr>
    <tr>
      <th>100</th>
      <td>6.3</td>
      <td>3.3</td>
      <td>6.0</td>
      <td>2.5</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>120</th>
      <td>6.9</td>
      <td>3.2</td>
      <td>5.7</td>
      <td>2.3</td>
      <td>Iris-virginica</td>
    </tr>
    <tr>
      <th>140</th>
      <td>6.7</td>
      <td>3.1</td>
      <td>5.6</td>
      <td>2.4</td>
      <td>Iris-virginica</td>
    </tr>
  </tbody>
</table>
</div>



#### 连续数据段提取


```python
iris_data[5:10]#取第5到第9行
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



#### 提取某一行


```python
iris_data.loc[5] #取第5行的数据
```




    sepal_length            5.4
    sepal_width             3.9
    petal_length            1.7
    petal_width             0.4
    class           Iris-setosa
    Name: 5, dtype: object



### 投影操作

所谓投影和数据库中差不多,就是取列(取属性),简单的方式就是用`[]`圈住需要的列号或者列名


```python
iris_data["sepal_length"][:5]#取某列
```




    0    5.1
    1    4.9
    2    4.7
    3    4.6
    4    5.0
    Name: sepal_length, dtype: float64




```python
iris_data.sepal_length[:5]#同样地取某列
```




    0    5.1
    1    4.9
    2    4.7
    3    4.6
    4    5.0
    Name: sepal_length, dtype: float64




```python
iris_data[["sepal_length","petal_width"]][:5]#取两列
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
      <th>petal_width</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5.1</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4.9</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4.7</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4.6</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.0</td>
      <td>0.2</td>
    </tr>
  </tbody>
</table>
</div>



### **iloc **位置坐标操作

简单粗暴的直接查看对应坐标,第一位参数是行,第二位是列


```python
iris_data.iloc[5]#取第5行的数据
```




    sepal_length            5.4
    sepal_width             3.9
    petal_length            1.7
    petal_width             0.4
    class           Iris-setosa
    Name: 5, dtype: object




```python
iris_data.iloc[0,2:4]#取第一行第3个数据和第四个数据
```




    petal_length    1.4
    petal_width     0.2
    Name: 0, dtype: object



### 增加一列元素

增加一列只需要在原数据上后面用`[]`填入要新增的元素即可,注意这个操作是对源数据的修改,如果希望源数据不变,先copy再增加


```python
people_fromExcel = pd.read_excel('./source/people.xlsx', u'工作表1', index_col=None, na_values=['NA'])

people_Data = people_fromExcel.append(pd.DataFrame([["Hao",24]],columns = ["name","age"])).reset_index(drop=True)
people_Data
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
      <th>name</th>
      <th>age</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Michael</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Andy</td>
      <td>30.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Justin</td>
      <td>19.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Hao</td>
      <td>24.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
people_Data["nation"] = ["USA","UK","AUS","PRC"]
```


```python
people_Data
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
      <th>name</th>
      <th>age</th>
      <th>nation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Michael</td>
      <td>NaN</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Andy</td>
      <td>30.0</td>
      <td>UK</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Justin</td>
      <td>19.0</td>
      <td>AUS</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Hao</td>
      <td>24.0</td>
      <td>PRC</td>
    </tr>
  </tbody>
</table>
</div>



也可以只输入一个值,这样就全部都是都是它了


```python
people_Data[u"星球"] = u"地球"
people_Data
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
      <th>name</th>
      <th>age</th>
      <th>nation</th>
      <th>星球</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Michael</td>
      <td>NaN</td>
      <td>USA</td>
      <td>地球</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Andy</td>
      <td>30.0</td>
      <td>UK</td>
      <td>地球</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Justin</td>
      <td>19.0</td>
      <td>AUS</td>
      <td>地球</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Hao</td>
      <td>24.0</td>
      <td>PRC</td>
      <td>地球</td>
    </tr>
  </tbody>
</table>
</div>


