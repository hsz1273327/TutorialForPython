
# 基于web的可交互运行环境jupyter

写了这么久还没介绍我写这些的平台,jupyter notebook

Jupyter 是ipython notebook 脱离ipython项目后的一个独立项目.不同于notebook, Jupyter已经不再只是python的交互执行框架,
而是致力于多语言通用的交互执行.

在以前 notebook作为ipython的一个子项目就受到许多人的喜爱和追捧,当时就已经可以通过多种途径利用它执行其他非python语言.
现在Jupyter 与ipython分家后,这一特性得到了更好的支持.

现在的Jupyter只负责交互执行,而执行的是什么语言其实是由其执行核心--kernel 来实现的,而现在的ipython可以自带其执行python版本的python核心.

本文也会顺带介绍几种支持Jupyter的优秀的语言.

至于ipython部分会单独拉出来讲,毕竟很多很实用

## Jupyter的安装:

Jupyter 现在是独立安装.当然,你依然需要装有python 和 pip.


    $pip install jupyter

如果你用brew 安装的python3,那么自然的

    $pip3 install jupyter

## 运行

    $jupyter notebook


当然了,没有kernel是没法运行的

## `*`Jupyter的多语言支持

在[这里](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels)你可以看到目前支持的语言.

下面介绍几个比较值得安装的的kernel安装:

本文中介绍的的kernel只在mac下测试安装成功,在linux下应当都能成功,但windows下未必.
欢迎朋友们写下其他平台的经验,我看到也会进行修改,谢谢

### 通用依赖
几乎所有kernel都需要`zeromq`和`openssl`这两个库,在mac下他们都可以用brew安装

brew install zeromq
brew install openssl

Jupyter 对于各个语言的支持其实都是通过所谓的核(kernel)来实现的,操作核的命令是`jupyter kernelspec <cmd>`

和常规一样,

+ list 查看已有核的状态
+ install 安装一个核,不过一般来说这些核都不是用这个方法装的
+ remove/uninstall 移除一个核 


### python2与python3并存

#### 安装依赖

python的kernel自然依赖于python.

对于新手来说python2和python3并存本身就是件比较纠结蛋碎的事儿,mac下一般会用homebrew安装两个版本
(当然也会有人安装其他比如pypy之类,那个咱不管)

    $brew install python
    $brew install python3


如果是这样安装,那python python2 python3对应的便是不同版本的python如下表(可能版本不同有些许不同)

命令|python来源|pip命令|库位置
---|---|---|---
python|brew 安装的 python|pip|/usr/local/lib/python2.7/site-packages
python2|brew 安装的 python|pip|/usr/local/lib/python2.7/site-packages
python3|brew 安装的 python3|pip3|/usr/local/lib/python3.4/site-packages


#### 安装kernel

**分别安装ipython,在各自环境下执行**

    $pip install ipython[all]
    $ipython kernelspec install-self
    $pip3 install ipython[all]
    $ipython kernelspec install-self

#### 测试下

打开Jupyter:

    jupyter notebook

可以在*new*看到里面出现*Python 2*和*Python 3*两个可选项


### pypy

事实上jupyter并没有专门的pypy核心,但其实要用pypy比其他的都简单,我们通过`ipython kernelspec list`找到自己原本的python核所在的目录,进去这个目录找到核文件夹,我们把它复制一份改名叫`pypy`,然后在pypy环境中pip安装jupyter,这样原本的python的核就会被替换掉,我们只要给这俩核的文件夹名和其中的`kernel.json`中的display_name对掉下就好了

### Golang

Go语言是谷歌几年前推出的一门编译型语言,它以简洁优雅高,高开发效率,高可维护性和善于处理高并发而著称
Go有一套完善的开发流程和语言规范,是开发高性能服务的优秀选择.

#### 安装依赖

+ go语言:

go语言只要用homebrew安装即可

    $brew install go

安装好后要在`~/.bash_profile`内添加以下语句(中你的go项目位置)后resource下激活或者重启计算机

    export GOPATH=你的go项目位置#GOPATH可以有多个,用:隔开,其中第一个回存放 go get 命令下载的库文件会放在第一个位置上
    
如果你希望你的
    export PATH=${GOPATH//://bin:}/bin:$PATH


+ [gophernotes](https://github.com/gopherdata/gophernotes)

这是一个go语言的解释器,可以写一句执行一句,它也自带一个交互命令行工具

安装:

首先它依赖go的一个包叫做goimports,安装的话墙外很简单

    $ go get golang.org/x/tools/cmd/goimports
    
但墙外我们就得用[这个](http://www.golangtc.com/download/package)

它的安装默认是依赖zmq2.2.x,但我想大多数人都装的是zmq4.x吧,所以只要这么安装


    $ go get -tags zmq_4_x github.com/gophergala2016/gophernotes
    

#### 安装kernel

    $mkdir -p ~/.ipython/kernels/gophernotes
    
然后去你的第一个GOPATH下找到/src/github.com/takluyver/igo/kernel/文件夹,之后复制进.ipython/kernels/gophernotes


之后修改其中的`kernel.json`,将其中的`$GOPATH`替换成自己的的gopath


#### 测试下

切换Kernel到Golang 1.5



```python
:import "fmt"
```


```python
word := "world"
```




    "world"





```python
fmt.Sprintf("hello %s",word)
```




    "hello world"




> channels


```python
msg := make(chan string)
```




    (chan string)(0xc820072060)





```python
go func() {msg <- "ping"}()
```


```python
message := <- msg
```




    "ping"




> 例子


```python
:import "fmt"
```


```python
fmt.Print("1")
```




    11
    <nil>




go语言可以看[这篇](https://github.com/astaxie/build-web-application-with-golang/tree/master/zh)来学习

### Javascript(node.js)

#### 安装依赖

+ node.js

    $ brew install node



### 安装kernel

```shell
sudo npm install -g ijavascript
sudo npm install -g --save-dev babel-preset-es2015
```

    
    
### 配套设施--balel

babel是一个将ES6标准的js代码转换为可在浏览器中运行的ES5代码的工具.我们可以安装ibabel来使用它

```shell
sudo npm install -g jp-babel@0.0.6
```
    
注意要用老版本,因为新版的babel有bug

#### 测试下
切换Kernel到JavaScript(Node.js)


```python
var Animal = {
    createNew: function(){
        var animal = {}
        animal.sleep = function(){
          return "Zzzzz"
        }
        return animal
      }
}

var Dog = {
    createNew: function(name){
        var dog = Animal.createNew()//继承
        dog.name = name
        dog.makeSound = function(){
            return "wangwang"
        }
        return dog
    }
}
a=Dog.createNew("doggy")
a.makeSound()
```




    'wangwang'



### R

似乎是很受数据科学家由其统计出身的人欢迎的一种语言.但是语法别扭,个人不喜欢,但是还是得学习

#### 安装依赖

+ R

[下载新版(3.22)R语言安装包](http://mirror.bjtu.edu.cn/cran/bin/macosx/R-3.2.2.pkg)

然后双击安装

#### 安装kernel

    install.packages(c('rzmq','repr','IRkernel','IRdisplay'),
                     repos = c('http://irkernel.github.io/', getOption('repos')))
    IRkernel::installspec()


#### 测试下

写个身高的简单统计计算吧:

先安装`sca`包:

    > install.packages("sca")

切换Kernel到R:


```python
library(sca)
height=c(1.75,1.82,1.78,1.93,1.77)
weight=c(69,80,78,96,65)
age=c(19,21,20,26,17)
group_A=data.frame(height,weight,age)
print(group_A)

sum_h=sum(group_A$height)#身高求和
cat("身高和:",sum_h,"\n")
cat("分布:\n")
cat(percent(group_A$height/sum_h),"\n")
cat("身高均值",mean(group_A$height),"\n")
sum_w=sum(group_A$weight)#体重求和
cat("体重和:",sum_w,"\n")
cat("分布:\n")
cat(percent(group_A$weight/sum_w),"\n")
cat("体重均值",mean(group_A$weight),"\n")
```

      height weight age
    1   1.75     69  19
    2   1.82     80  21
    3   1.78     78  20
    4   1.93     96  26
    5   1.77     65  17
    身高和: 9.05 
    分布:
    19 % 20 % 20 % 21 % 20 % 
    身高均值 1.81 
    体重和: 388 
    分布:
    18 % 21 % 20 % 25 % 17 % 
    体重均值 77.6 


### Scala

Scala应该是后起语言中的新星了,同时支持面向对象编程和函数式编程的特性让它分外耀眼,而拥有类型推断又让它显得十分简洁优雅.
它与Java间的联系又让它因为有衬托对比而显得格外讨喜.

#### 安装依赖
自然要安装scala了

    brew install scala

留意安装的是什么版本

#### 安装kernel
虽然列表中推荐的是iscala 但还有一个更加简单的方式--[jupyter-scala](https://github.com/alexarchambault/jupyter-scala)**

这个方法就是简单无脑的下载下来然后运行脚本

+ 2.10版本的scala[下载这个](https://oss.sonatype.org/content/repositories/snapshots/com/github/alexarchambault/jupyter/jupyter-scala-cli_2.10.5/0.2.0-SNAPSHOT/jupyter-scala_2.10.5-0.2.0-SNAPSHOT.zip)
2.11版本的[下载这个](https://oss.sonatype.org/content/repositories/snapshots/com/github/alexarchambault/jupyter/jupyter-scala-cli_2.11.6/0.2.0-SNAPSHOT/jupyter-scala_2.11.6-0.2.0-SNAPSHOT.zip)

+ 解压到一个安全的位置然后运行其中`bin`文件夹下的的`jupyter-scala`脚本自动完成安装

+ 用

    $ipython kernelspec list

查看是否有`scala211`或者`scala210`这样的输出,有的话之后运行

    $ipython console --kernel scala211

这样再用jupyter notebook进入就能找到Scala 2.11了

当然这样如果以后scala升级了那就无法使用最新版本了,解决方法就是自己本地编译



#### 测试下

写个简单的尾递归求阶乘

切换Kernel到Scala 2.11



```python
def factorial(n:Int):Int = {
    if(n >0) n * factorial(n-1) else 1
}
```


    defined [32mfunction [36mfactorial[0m



```python
factorial(5)
```


    [36mres1[0m: [32mInt[0m = [32m120[0m


学习scala可以去[这里](http://twitter.github.io/scala_school/zh_cn/)

### Spark

#### 安装依赖

+ Spark

这个不必多介绍,大数据的主流工具之一,安装可以看我[以前的帖子]()



#### 安装kernel

+ [github上下载源文件](https://github.com/ibm-et/spark-kernel)

+ cd 进入源文件根目录,然后

      $sbt compile

      $sbt pack

+ 编译好后执行

      $(cd kernel/target/pack && make install)

+ 之后你的`home`文件夹下会多出一个`/local`的文件夹,其中`kernel`文件夹存放jar文件
`bin/sparkkernel`是启动脚本

+ 如果都成功了,那么运行

    ~/local/bin/sparkkernel

应该可以看到kernel运行了

+ 与jupyter链接

    cd ~/.ipython/kernels/
    mkdir spark
    touch spark/kernel.json

改写`kernel.json`为

    {
    "display_name": "Spark 1.2.1 (Scala 2.10.4)",
    "language": "scala",
    "argv": [
        "<absolute>/<path>/<to>/local/bin/sparkkernel",
        "--profile",
        "{connection_file}"
     ],
     "codemirror_mode": "scala"
    }

这样就可以用本地模式测试代码了

#### 测试下
切换Kernel到Spark1.6.0
##### 写一个用mapreduce求pi的函数:



```python
val NUM_SAMPLES = 10000
val count = sc.parallelize(1 to NUM_SAMPLES).map{i =>
    val x = Math.random()
    val y = Math.random()
    if (x*x + y*y < 1) 1 else 0
}.reduce(_ + _)
println("Pi is roughly " + 4.0 * count / NUM_SAMPLES)
```

    Pi is roughly 3.132


##### 写个简单的线性回归:

将[数据](https://github.com/apache/spark/blob/master/data/mllib/ridge-data/lpsa.data)下载到同级目录



```python
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.regression.LinearRegressionModel
import org.apache.spark.mllib.regression.LinearRegressionWithSGD
import org.apache.spark.mllib.linalg.Vectors
val data = sc.textFile("source/lpsa.data")
val parsedData = data.map { line =>
    val parts = line.split(',')
    LabeledPoint(parts(0).toDouble, Vectors.dense(parts(1).split(' ').map(_.toDouble)))
}.cache()
val numIterations = 100
val model = LinearRegressionWithSGD.train(parsedData, numIterations)
// Evaluate model on training examples and compute training error
val valuesAndPreds = parsedData.map { point =>
    val prediction = model.predict(point.features)
    (point.label, prediction)
}
val MSE = valuesAndPreds.map{case(v, p) => math.pow((v - p), 2)}.mean()
println("training Mean Squared Error = " + MSE)

// Save and load model
model.save(sc, "myModelPath")
val sameModel = LinearRegressionModel.load(sc, "myModelPath")
```

    training Mean Squared Error = 6.207597210613578


学习spark可以参考[官方文档](http://spark.apache.org/)

### Itorch(lua)

Itorch这是一个lua的机器学习框架,用的虽然不多但既然是学这个的又蛮喜欢lua那就一并写上吧

#### 安装依赖

+ Torch

**安装:**

    curl -s https://raw.githubusercontent.com/torch/ezinstall/master/install-deps | bash
    git clone https://github.com/torch/distro.git ~/torch --recursive
    cd ~/torch; ./install.sh

这样就可以安装torch到`~/torch`下了

然后在`.bash_profile`中写入

    . /Users/huangsizhe/torch/install/bin/torch-activate

这样就可以使用torch了

**打开torch的交互shell:**

    $th

#### 安装kernel

    git clone https://github.com/facebook/iTorch.git
    cd iTorch
    luarocks make


#### 测试下

切换Kernel到iTorch:



```python
function fib(n)
    if n < 2 then return 1 end
    return fib(n - 2) + fib(n - 1)
end
```


```python
fib(20)
```




    10946	




更多的[lua](http://www.yiibai.com/lua/)和[torch](http://torch.ch/docs/getting-started.html#_)教程可以点击对应链接查看

### C/C++

想象下C++这种竟然可以依靠强大的LLVM和Clang实现脚本化,是不是很激动~~

#### 安装依赖

cling[从这里下载](https://ecsft.cern.ch/dist/cling/current/)对应版本的安装包,解压到希望的位置即可
设定一下环境变量`CLING_EXE=你的cling安装目录下cling的具体位置`

#### 安装

下载<https://github.com/minrk/clingkernel>,cd进去后

    python setup.py install

安装成功后执行

    jupyter kernelspec install cling

#### 测试下
切换Kernel到C++:


```python
#include <stdio.h>
printf("Hello World!\n")
```

    Hello World!
    (int) 13



```python
.rawInput
void test() {//方法
    printf("just a test");
}
.rawInput

```

    



```python
test()
```

    just a test


```python
auto func = [](int a, int b) -> int { return a+b; };//c++11中的匿名函数
```

    


```python
func(2, 3)
```

    (int) 5



```python
.rawInput
class Rectangle {//类
    private:
    double w;
    double h;

    public:

    Rectangle(double w_, double h_) {
        w = w_;
        h = h_;
    }
    double area(void) {
        return w * h;
    }
    double perimiter(void) {
        return 2 * (w + h);
    }
};
.rawInput
```

    


```python
Rectangle r = Rectangle(5, 4);
r.area()
```

    (double) 20.0000


### scheme

安装这个是为了学<计算机程序的构造和解释>这本书,作为Lisp的方言,scheme确实不简单.我安装的是基于ipython的`calysto_scheme`

#### 安装

再github上下载<https://github.com/Calysto/calysto_scheme>然后只要cd到目录

    python3 setup.py install

#### 测试

求斐波那契数列


```python
(begin
 (define (factorial n)
  (define (iter product counter)
    (if (> counter n)
        product
        (iter (* counter product)
              (+ counter 1))))
  (iter 1 1))
 (factorial 10)
 )
```




    3628800




```python
(begin
  (define fib
    (lambda (n)
      (cond
        ((= n 0) 1)
        ((= n 1) 1)
        (else(+ (fib (- n 1))
                 (fib (- n 2))
               )
         )
       )
     )    
   )
   (fib 5)
 )
```




    8



### haskell

传说中的语言,想了解的可以看一本[萌系的书](http://learnyoua.haskell.sg/)

通过它学习函数式编程几乎是业界共识吧(笑)

#### 安装

ihaskell只能在类unix系统上安装,安装也简单,mac下直接

    git clone http://www.github.com/gibiansky/IHaskell
    cd IHaskell
    ./macos-install.sh

然后等就行了

#### 测试下:

Kernel切换到haskell:


```python
import IHaskell.Display
data Color = Red | Green | Blue
instance IHaskellDisplay Color where
  display color = return $ Display [html code]
    where
      code = concat ["<div style='font-weight: bold; color:"
                    , css color
                    , "'>Look!</div>"]
      css Red   = "red"
      css Blue  = "blue"
      css Green = "green"
```


```python
Red
Green
Blue
```


<style>/*
Custom IHaskell CSS.
*/

/* Styles used for the Hoogle display in the pager */
.hoogle-doc {
    display: block;
    padding-bottom: 1.3em;
    padding-left: 0.4em;
}
.hoogle-code {
    display: block;
    font-family: monospace;
    white-space: pre;
}
.hoogle-text {
    display: block;
}
.hoogle-name {
    color: green;
    font-weight: bold;
}
.hoogle-head {
    font-weight: bold;
}
.hoogle-sub {
    display: block;
    margin-left: 0.4em;
}
.hoogle-package {
    font-weight: bold;
    font-style: italic;
}
.hoogle-module {
    font-weight: bold;
}
.hoogle-class {
    font-weight: bold;
}

/* Styles used for basic displays */
.get-type {
    color: green;
    font-weight: bold;
    font-family: monospace;
    display: block;
    white-space: pre-wrap;
}

.show-type {
    color: green;
    font-weight: bold;
    font-family: monospace;
    margin-left: 1em;
}

.mono {
    font-family: monospace;
    display: block;
}

.err-msg {
    color: red;
    font-style: italic;
    font-family: monospace;
    white-space: pre;
    display: block;
}

#unshowable {
    color: red;
    font-weight: bold;
}

.err-msg.in.collapse {
  padding-top: 0.7em;
}

/* Code that will get highlighted before it is highlighted */
.highlight-code {
    white-space: pre;
    font-family: monospace;
}

/* Hlint styles */
.suggestion-warning { 
    font-weight: bold;
    color: rgb(200, 130, 0);
}
.suggestion-error { 
    font-weight: bold;
    color: red;
}
.suggestion-name {
    font-weight: bold;
}
</style><div style='font-weight: bold; color:red'>Look!</div>



<style>/*
Custom IHaskell CSS.
*/

/* Styles used for the Hoogle display in the pager */
.hoogle-doc {
    display: block;
    padding-bottom: 1.3em;
    padding-left: 0.4em;
}
.hoogle-code {
    display: block;
    font-family: monospace;
    white-space: pre;
}
.hoogle-text {
    display: block;
}
.hoogle-name {
    color: green;
    font-weight: bold;
}
.hoogle-head {
    font-weight: bold;
}
.hoogle-sub {
    display: block;
    margin-left: 0.4em;
}
.hoogle-package {
    font-weight: bold;
    font-style: italic;
}
.hoogle-module {
    font-weight: bold;
}
.hoogle-class {
    font-weight: bold;
}

/* Styles used for basic displays */
.get-type {
    color: green;
    font-weight: bold;
    font-family: monospace;
    display: block;
    white-space: pre-wrap;
}

.show-type {
    color: green;
    font-weight: bold;
    font-family: monospace;
    margin-left: 1em;
}

.mono {
    font-family: monospace;
    display: block;
}

.err-msg {
    color: red;
    font-style: italic;
    font-family: monospace;
    white-space: pre;
    display: block;
}

#unshowable {
    color: red;
    font-weight: bold;
}

.err-msg.in.collapse {
  padding-top: 0.7em;
}

/* Code that will get highlighted before it is highlighted */
.highlight-code {
    white-space: pre;
    font-family: monospace;
}

/* Hlint styles */
.suggestion-warning { 
    font-weight: bold;
    color: rgb(200, 130, 0);
}
.suggestion-error { 
    font-weight: bold;
    color: red;
}
.suggestion-name {
    font-weight: bold;
}
</style><div style='font-weight: bold; color:green'>Look!</div>



<style>/*
Custom IHaskell CSS.
*/

/* Styles used for the Hoogle display in the pager */
.hoogle-doc {
    display: block;
    padding-bottom: 1.3em;
    padding-left: 0.4em;
}
.hoogle-code {
    display: block;
    font-family: monospace;
    white-space: pre;
}
.hoogle-text {
    display: block;
}
.hoogle-name {
    color: green;
    font-weight: bold;
}
.hoogle-head {
    font-weight: bold;
}
.hoogle-sub {
    display: block;
    margin-left: 0.4em;
}
.hoogle-package {
    font-weight: bold;
    font-style: italic;
}
.hoogle-module {
    font-weight: bold;
}
.hoogle-class {
    font-weight: bold;
}

/* Styles used for basic displays */
.get-type {
    color: green;
    font-weight: bold;
    font-family: monospace;
    display: block;
    white-space: pre-wrap;
}

.show-type {
    color: green;
    font-weight: bold;
    font-family: monospace;
    margin-left: 1em;
}

.mono {
    font-family: monospace;
    display: block;
}

.err-msg {
    color: red;
    font-style: italic;
    font-family: monospace;
    white-space: pre;
    display: block;
}

#unshowable {
    color: red;
    font-weight: bold;
}

.err-msg.in.collapse {
  padding-top: 0.7em;
}

/* Code that will get highlighted before it is highlighted */
.highlight-code {
    white-space: pre;
    font-family: monospace;
}

/* Hlint styles */
.suggestion-warning { 
    font-weight: bold;
    color: rgb(200, 130, 0);
}
.suggestion-error { 
    font-weight: bold;
    color: red;
}
.suggestion-name {
    font-weight: bold;
}
</style><div style='font-weight: bold; color:blue'>Look!</div>


## 一些技巧

+ `!`用来执行shell命令

比如`!cat a.txt`可以查看a.txt的内容

利用这个技巧配合atom等有命令行工具的文本编辑器可以实现对编译语言的编译和运行

+ 魔法命令`%`(不是所有都有,ipython的一定有)

输入`%magic`可以查看有哪些魔法命令

+ 尽量不要让jupyter打印循环或者递归,如果出错可能会卡死,下次也打不开,处理方法是用文本编辑器打开`ipynb`文件,直接删除对应的cell内容和打印内容

