
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

```bash
pip install jupyter
```

如果你用brew 安装的python3,那么自然的

```bash
pip3 install jupyter
```

## 运行

```bash
jupyter notebook
```

当然了,没有kernel是没法运行的

## `*`Jupyter的多语言支持

在[这里](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels)你可以看到目前支持的语言.

下面介绍几个比较值得安装的的kernel安装:

本文中介绍的的kernel只在mac下测试安装成功,在linux下应当都能成功,但windows下未必.
欢迎朋友们写下其他平台的经验,我看到也会进行修改,谢谢

### 通用依赖
几乎所有kernel都需要`zeromq`和`openssl`这两个库,在mac下他们都可以用brew安装

```bash
brew install zeromq
brew install openssl
```

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

```bash
brew install python
brew install python3
```

如果是这样安装,那python python2 python3对应的便是不同版本的python如下表(可能版本不同有些许不同)

命令|python来源|pip命令|库位置
---|---|---|---
python|brew 安装的 python|pip|/usr/local/lib/python2.7/site-packages
python2|brew 安装的 python|pip|/usr/local/lib/python2.7/site-packages
python3|brew 安装的 python3|pip3|/usr/local/lib/python3.4/site-packages


#### 安装kernel

**分别安装ipython,在各自环境下执行**

```bash
pip install ipython[all]
ipython kernelspec install-self
pip3 install ipython[all]
ipython kernelspec install-self
```

#### 测试下

打开Jupyter:
```bash
jupyter notebook
```

可以在*new*看到里面出现*Python 2*和*Python 3*两个可选项


### pypy

事实上jupyter并没有专门的pypy核心,但其实要用pypy比其他的都简单,我们通过`ipython kernelspec list`找到自己原本的python核所在的目录,进去这个目录找到核文件夹,我们把它复制一份改名叫`pypy`,然后在pypy环境中pip安装jupyter,这样原本的python的核就会被替换掉,我们只要给这俩核的文件夹名和其中的`kernel.json`中的display_name对掉下就好了

### [SparkMagic](https://github.com/jupyter-incubator/sparkmagic)

sparkmagic是一个可以用于连接远端spark,让我们通过jupyternotebook来使用spark的工具.

#### 安装依赖

[Livy](https://github.com/cloudera/livy)是一个用于为spark提供restful接口的服务,sparkmagic依赖它.安装需要java8,下载解压后

+ 检查环境变量

    ```bash
    export SPARK_HOME=/usr/lib/spark

    export HADOOP_CONF_DIR=/etc/hadoop/conf
    ```

+ 启动

    ```bash
    ./bin/livy-server start
    ```

#### 安装kernel

+ 安装python模块

```bash
pip install sparkmagic
```

+ 确认是否开启控件功能

```bash
jupyter nbextension enable --py --sys-prefix widgetsnbextension 
```

+ 找到sparkmagic的安装路径,之后cd到那个路径,执行`jupyter-kernelspec install sparkmagic/kernels/sparkkernel`或者
`jupyter-kernelspec install sparkmagic/kernels/pysparkkernel`或者`jupyter-kernelspec install sparkmagic/kernels/sparkrkernel`将对应语言的kernel添加到路径.

+ 设置`~/.sparkmagic/config.json`,一般默认就行,如果需要改,可以参考下面的例子

    ```json
    {
      "kernel_python_credentials" : {
        "username": "",
        "password": "",
        "url": "http://localhost:8998",
        "auth": "None"
      },

      "kernel_scala_credentials" : {
        "username": "",
        "password": "",
        "url": "http://localhost:8998",
        "auth": "None"
      },
      "kernel_r_credentials": {
        "username": "",
        "password": "",
        "url": "http://localhost:8998"
      },

      "logging_config": {
        "version": 1,
        "formatters": {
          "magicsFormatter": { 
            "format": "%(asctime)s\t%(levelname)s\t%(message)s",
            "datefmt": ""
          }
        },
        "handlers": {
          "magicsHandler": { 
            "class": "hdijupyterutils.filehandler.MagicsFileHandler",
            "formatter": "magicsFormatter",
            "home_path": "~/.sparkmagic"
          }
        },
        "loggers": {
          "magicsLogger": { 
            "handlers": ["magicsHandler"],
            "level": "DEBUG",
            "propagate": 0
          }
        }
      },

      "wait_for_idle_timeout_seconds": 15,
      "livy_session_startup_timeout_seconds": 60,

      "fatal_error_suggestion": "The code failed because of a fatal error:\n\t{}.\n\nSome things to try:\na) Make sure Spark has enough available resources for Jupyter to create a Spark context.\nb) Contact your Jupyter administrator to make sure the Spark magics library is configured correctly.\nc) Restart the kernel.",

      "ignore_ssl_errors": false,

      "session_configs": {
        "driverMemory": "1000M",
        "executorCores": 2
      },

      "use_auto_viz": true,
      "coerce_dataframe": true,
      "max_results_sql": 2500,
      "pyspark_dataframe_encoding": "utf-8",

      "heartbeat_refresh_seconds": 30,
      "livy_server_heartbeat_timeout_seconds": 0,
      "heartbeat_retry_seconds": 10,

      "server_extension_default_kernel_name": "pysparkkernel",
      "custom_headers": {},

      "retry_policy": "configurable",
      "retry_seconds_to_sleep_list": [0.2, 0.5, 1, 3, 5],
      "configurable_retry_policy_max_retries": 8
    }
    ```

#### 测试下

切换Kernel到Pyspark

##### 写一个用mapreduce求pi的函数:



```Rust
val NUM_SAMPLES = 10000
val count = sc.parallelize(1 to NUM_SAMPLES).map{i =>
    val x = Math.random()
    val y = Math.random()
    if (x*x + y*y < 1) 1 else 0
}.reduce(_ + _)
println("Pi is roughly " + 4.0 * count / NUM_SAMPLES)
```

    Starting Spark application



<table>
<tr><th>ID</th><th>YARN Application ID</th><th>Kind</th><th>State</th><th>Spark UI</th><th>Driver log</th><th>Current session?</th></tr><tr><td>13</td><td>None</td><td>spark</td><td>idle</td><td></td><td></td><td>✔</td></tr></table>


    SparkSession available as 'spark'.
    NUM_SAMPLES: Int = 10000
    count: Int = 7746
    Pi is roughly 3.0984


学习spark可以参考[官方文档](http://spark.apache.org/)

### scheme

安装这个是为了学<计算机程序的构造和解释>这本书,作为Lisp的方言,scheme确实不简单.我安装的是基于ipython的`calysto_scheme`,它本质上是用python解析执行scheme语句.

#### 安装

再github上下载<https://github.com/Calysto/calysto_scheme>然后只要cd到目录

    python3 setup.py install

#### 测试

求斐波那契数列


```Rust
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




```Rust
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



### postgresql

最先进最全能的开源关系数据库postgresql也有对应的内核[postgres_kernel](https://github.com/bgschiller/postgres_kernel).


#### 安装

```bash
pip install psycopg2-binary
pip install git+https://github.com/data-science-tools/postgres_kernel.git@master
```

注意原版依赖psycopg2,很多时候不好安装.

#### 测试


```Rust
-- connection: postgres://postgres:postgres@localhost:5432/test
```


```Rust
-- autocommit: true
```

    switched autocommit mode to True


```Rust
SELECT * FROM Person limit 5
```

    5 row(s) returned.



<table>
<thead>
<tr><th style="text-align: right;">  id</th><th>name  </th><th>birthday  </th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;">   1</td><td>千万  </td><td>2019-03-04</td></tr>
<tr><td style="text-align: right;">   2</td><td>十万  </td><td>2018-03-04</td></tr>
<tr><td style="text-align: right;">   3</td><td>百万  </td><td>2017-03-04</td></tr>
<tr><td style="text-align: right;">   4</td><td>千万  </td><td>2019-03-04</td></tr>
<tr><td style="text-align: right;">   5</td><td>十万  </td><td>2018-03-04</td></tr>
</tbody>
</table>


### C语言

[jupyter-c-kernel](https://github.com/brendan-rius/jupyter-c-kernel)是一个简单的C语言内核,它的外部依赖只有gcc.

#### 安装

```bash
pip install jupyter-c-kernel
install_c_kernel
```

#### 测试一下


```Rust
//cflag:-lm
#include <stdio.h>
#include <math.h>

int main() {
    printf("sqrt(67)=%f",sqrt(67));
    return 0;
}
```

    sqrt(67)=8.185353

### C++语言

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


```Rust
#include <stdio.h>
printf("Hello World!\n")
```

    Hello World!
    (int) 13



```Rust
.rawInput
void test() {//方法
    printf("just a test");
}
.rawInput

```

    



```Rust
test()
```

    just a test


```Rust
auto func = [](int a, int b) -> int { return a+b; };//c++11中的匿名函数
```

    


```Rust
func(2, 3)
```

    (int) 5



```Rust
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

    


```Rust
Rectangle r = Rectangle(5, 4);
r.area()
```

    (double) 20.0000


### Golang

Go语言是谷歌几年前推出的一门编译型语言,它以简洁优雅高,高开发效率,高可维护性和善于处理高并发而著称
Go有一套完善的开发流程和语言规范,是开发高性能服务的优秀选择.

#### 安装依赖

+ go语言:

go语言只要用homebrew安装即可

```bash
brew install go
```

安装好后要在`~/.bash_profile`内添加以下语句(中你的go项目位置)后resource下激活或者重启计算机
```bash
export GOPATH=你的go项目位置#GOPATH可以有多个,用:隔开,其中第一个回存放 go get 命令下载的库文件会放在第一个位置上
```
如果你希望你的
```bash
export PATH=${GOPATH//://bin:}/bin:$PATH
```

+ [gophernotes](https://github.com/gopherdata/gophernotes)

这是一个go语言的解释器,可以写一句执行一句,它也自带一个交互命令行工具

安装:

首先它依赖go的一个包叫做goimports,安装的话墙外很简单

```bash
go get golang.org/x/tools/cmd/goimports
```

但墙外我们就得用[这个](http://www.golangtc.com/download/package)

它的安装默认是依赖zmq2.2.x,但我想大多数人都装的是zmq4.x吧,所以只要这么安装

```bash
go get -tags zmq_4_x github.com/gophergala2016/gophernotes
```   

#### 安装kernel

```bash
mkdir -p ~/.ipython/kernels/gophernotes
```

然后去你的第一个GOPATH下找到/src/github.com/takluyver/igo/kernel/文件夹,之后复制进.ipython/kernels/gophernotes


之后修改其中的`kernel.json`,将其中的`GOPATH`替换成自己的的gopath


#### 测试下

切换Kernel到Golang 1.5



```Rust
import "fmt"
```


```Rust
word := "world"
```


```Rust
fmt.Sprintf("hello %s",word)
```




    hello world



> channels


```Rust
msg := make(chan string)
```


```Rust
go func() {msg <- "ping"}()
```


```Rust
message := <- msg
```

> 例子


```Rust
import "fmt"
```


```Rust
fmt.Print("1")
```

    1




    1 <nil>



go语言可以看[这篇](https://github.com/astaxie/build-web-application-with-golang/tree/master/zh)来学习

### Rust

Rust也是一门很有潜力的编程语言.

#### 安装

```bash
cargo install evcxr_jupyter
evcxr_jupyter --install
```

#### 测试


```Rust
use std::fmt::Debug;
pub struct Matrix<T> {
    pub values: Vec<T>, 
    pub row_size: usize
}

impl<T: Debug> Matrix<T> {
    pub fn evcxr_display(&self) {
        let mut html = String::new();
        html.push_str("<table>");
        for r in 0..(self.values.len() / self.row_size) {
            html.push_str("<tr>");
            for c in 0..self.row_size {
                html.push_str("<td>");
                html.push_str(&format!("{:?}", self.values[r * self.row_size + c]));
                html.push_str("</td>");
            }
            html.push_str("</tr>");            
        }
        html.push_str("</table>");
        println!("EVCXR_BEGIN_CONTENT text/html\n{}\nEVCXR_END_CONTENT", html);
    }
}
```


```Rust
let m = Matrix {values: vec![1,2,3,4,5,6,7,8,9], row_size: 3};
m
```




<table><tr><td>1</td><td>2</td><td>3</td></tr><tr><td>4</td><td>5</td><td>6</td></tr><tr><td>7</td><td>8</td><td>9</td></tr></table>



### Javascript(jp-babel)

### 安装kernel

```shell
sudo apt-get install nodejs-legacy npm ipython ipython-notebook
sudo npm install -g jp-babel
```
#### 安装kernel

```shell
jp-babel-install
jp-babel-notebook
```

#### 测试下
切换Kernel到JavaScript(Node.js)


```Rust
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

```R
install.packages(c('rzmq','repr','IRkernel','IRdisplay'),
                 repos = c('http://irkernel.github.io/', getOption('repos')))
IRkernel::installspec()
```

#### 测试下

写个身高的简单统计计算吧:

先安装`sca`包:
```R
> install.packages("sca")
```
切换Kernel到R:


```Rust
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
```bash
ipython kernelspec list
```
查看是否有`scala211`或者`scala210`这样的输出,有的话之后运行
```bash
ipython console --kernel scala211
```
这样再用jupyter notebook进入就能找到Scala 2.11了

当然这样如果以后scala升级了那就无法使用最新版本了,解决方法就是自己本地编译



#### 测试下

写个简单的尾递归求阶乘

切换Kernel到Scala 2.11



```Rust
def factorial(n:Int):Int = {
    if(n >0) n * factorial(n-1) else 1
}
```


    defined [32mfunction [36mfactorial[0m



```Rust
factorial(5)
```


    [36mres1[0m: [32mInt[0m = [32m120[0m


学习scala可以去[这里](http://twitter.github.io/scala_school/zh_cn/)

## 一些技巧

+ `!`用来执行shell命令

比如`!cat a.txt`可以查看a.txt的内容

利用这个技巧配合atom等有命令行工具的文本编辑器可以实现对编译语言的编译和运行

+ 魔法命令`%`(不是所有都有,ipython的一定有)

输入`%magic`可以查看有哪些魔法命令

+ 尽量不要让jupyter打印循环或者递归,如果出错可能会卡死,下次也打不开,处理方法是用文本编辑器打开`ipynb`文件,直接删除对应的cell内容和打印内容

