# `*`Jupyter的多语言支持

在[这里](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels)你可以看到目前支持的语言.

下面介绍几个比较值得安装的的kernel安装:

本文中介绍的的kernel只在mac下测试安装成功,在linux下应当都能成功,但windows下未必.
欢迎朋友们写下其他平台的经验,我看到也会进行修改,谢谢

## 通用依赖

几乎所有kernel都需要`zeromq`和`openssl`这两个库,在mac下他们都可以用brew安装

```bash
brew install zeromq
brew install openssl
```

通常我们装jupyter就会先装这两个库

## pypy

事实上jupyter并没有专门的pypy核心,但其实要用pypy比其他的都简单,我们通过`ipython kernelspec list`找到自己原本的python核所在的目录,进去这个目录找到核文件夹,我们把它复制一份改名叫`pypy3`,然后在pypy环境中pip安装`ipykernel`,然后修改`kernel.json`中的`display_name`为`PyPy 3 (ipykernel)`,`argv`为` [
  <pypy位置>,
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ]`
 
 当然如果讲究点也可以替换下里面的图标.

### 测试一下


```sql
import sys
sys.copyright
```




    '\nCopyright 2003-2021 PyPy development team.\nAll Rights Reserved.\nFor further information, see <http://pypy.org>\n\nPortions Copyright (c) 2001-2021 Python Software Foundation.\nAll Rights Reserved.\n\nPortions Copyright (c) 2000 BeOpen.com.\nAll Rights Reserved.\n\nPortions Copyright (c) 1995-2001 Corporation for National Research Initiatives.\nAll Rights Reserved.\n\nPortions Copyright (c) 1991-1995 Stichting Mathematisch Centrum, Amsterdam.\nAll Rights Reserved.\n'



## [SparkMagic](https://github.com/jupyter-incubator/sparkmagic)

sparkmagic是一个可以用于连接远端spark,让我们通过jupyternotebook来使用spark的工具.

### 安装核心程序

sparkmagic依赖于[Livy](https://github.com/cloudera/livy)服务.livy是一个用于为spark提供restful接口的服务,sparkmagic依赖它.安装需要java8,下载解压后

+ 检查环境变量

    ```bash
    export SPARK_HOME=/usr/lib/spark

    export HADOOP_CONF_DIR=/etc/hadoop/conf
    ```

+ 启动

    ```bash
    ./bin/livy-server start
    ```
    
通常livy服务并不是我们自己搭建,而是由开放spark集群的人搭建.在确认好有livy服务后我们可以使用如下命令安装核心程序[sparkmagic](https://github.com/jupyter-incubator/sparkmagic)

```bash
pip install sparkmagic
```


### 安装kernel

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

### 测试下

切换Kernel到Pyspark

#### 写一个用mapreduce求pi的函数:



```sql
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

## postgresql

最先进最全能的开源关系数据库postgresql也有对应的内核[postgres_kernel](https://github.com/Python-Tools/postgresql_kernel).


### 安装

```bash
pip install postgresql_kernel
```

### 测试


```sql
-- connection: postgres://postgres:postgres@localhost:5432/test
```


```sql
-- autocommit: true
```

    switched autocommit mode to True


```sql
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


## Golang

Go语言是谷歌几年前推出的一门编译型语言,它以简洁优雅高,高开发效率,高可维护性和善于处理高并发而著称
Go有一套完善的开发流程和语言规范,是开发高性能服务的优秀选择.

### 安装核心程序

我们当然先要安装golang,本文就不做介绍了,感兴趣的可以看[我的对应文章](https://blog.hszofficial.site/TutorialForGoLang/#/%E5%B7%A5%E5%85%B7%E9%93%BE/go%E8%AF%AD%E8%A8%80%E7%9A%84%E7%BC%96%E8%AF%91%E5%99%A8%E5%92%8C%E7%BC%96%E8%AF%91%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA)


核心程序[gonb](https://github.com/janpfeifer/gonb)通过一下命令安装

```bash
go install github.com/janpfeifer/gonb@latest
go install golang.org/x/tools/cmd/goimports@latest
go install golang.org/x/tools/gopls@latest
```

这个核心程序目前只能在macos和linux中使用,且必须有`mian`入口函数才能使用,不过官方提供了`%%`标识来简化`main`入口函数的写法

### 安装kernel

```bash
gonb --install
```

### 测试下

切换Kernel到Go (gonb)



```sql
import "fmt"
%%
word := "world"
fmt.Printf("hello %s",word)
```

    hello world

> channels


```sql
%%
msg := make(chan string)
go func() {msg <- "ping"}()
message := <- msg
fmt.Printf("hello %s",message)
```

    hello ping

## C语言

[jupyter-c-kernel](https://github.com/XaverKlemenschits/jupyter-c-kernel)是一个简单的C语言内核,它的外部依赖只有gcc.

### 安装核心程序

```bash
pip install git+https://github.com/XaverKlemenschits/jupyter-c-kernel.git
```

这个核心程序提供了使用`//cflag:`来设置编译参数的功能.

### 安装核心

```bash
install_c_kernel --user
```

### 测试一下


```sql
//cflag:-lm
#include <stdio.h>
#include <math.h>

int main() {
    printf("sqrt(67)=%f",sqrt(67));
    return 0;
}
```

    sqrt(67)=8.185353

## Rust

Rust也是一门很有潜力的系统级编程语言.在看重安全性的系统编程领域已经初露头角.

### 安装核心程序

在已经安装了rust的前提下我们可以执行如下命令安装支持rust的核心程序[evcxr_jupyter](https://github.com/evcxr/evcxr/tree/main/evcxr_jupyter)

```bash
cargo install evcxr_jupyter
```

### 安装核心

在核心程序安装完成后执行

```bash
evcxr_jupyter --install
```

就可以将核心配置安装到jupyter中了

### 测试


```sql
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


```sql
let m = Matrix {values: vec![1,2,3,4,5,6,7,8,9], row_size: 3};
m
```




<table><tr><td>1</td><td>2</td><td>3</td></tr><tr><td>4</td><td>5</td><td>6</td></tr><tr><td>7</td><td>8</td><td>9</td></tr></table>



## Javascript

使用[ijavascript](https://github.com/n-riesco/ijavascript)可以为jupyter提供javascript支持,当然我们得先装node.js

### 安装核心程序

```shell
npm install -g ijavascript
```
### 安装核心

```shell
ijsinstall
```

### 测试下
切换Kernel到JavaScript(Node.js)


```sql
let Animal = {
    createNew: function(){
        var animal = {}
        animal.sleep = function(){
          return "Zzzzz"
        }
        return animal
      }
}

let Dog = {
    createNew: function(name){
        var dog = Animal.createNew()//继承
        dog.name = name
        dog.makeSound = function(){
            return "wangwang"
        }
        return dog
    }
}
let a=Dog.createNew("doggy")
a.makeSound()
```




    'wangwang'



## TypeScript

使用[itypescript](https://github.com/nearbydelta/itypescript)可以为jupyter提供ts支持,当然我们得先装`node.js`.

### 安装核心程序

```shell
npm install -g itypescript
```
### 安装核心

```shell
its --install=local
```

当然了也可以使用`its --install=global`来安装到系统级环境

### 测试下

切换Kernel到JavaScript(Node.js)


```sql
class Animal {
    constructor(private name: string) { }
    move(distanceInMeters: number) {
        console.log(`${this.name} moved ${distanceInMeters}m.`)
    }
}
let a = new Animal("monkey")
a.move(12)
```




<div style='background:#ffecb3;padding:1em;border-left:2px solid #ff6d00'><b>Configuration is not found!</b> Default configuration will be used: <pre>{"module":1,"target":1,"moduleResolution":2,"esModuleInterop":true}</pre></div>



    monkey moved 12m.

