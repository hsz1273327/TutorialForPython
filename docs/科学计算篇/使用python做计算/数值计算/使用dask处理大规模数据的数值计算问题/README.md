
# 使用dask做分布式计算

dask是纯python的分布式科学计算框架,其旨在让熟悉python下数据科学工具的数据开发人员可以无痛的从单机版本的numpy,scipy,pandas,sklearn迁移到分布式计算,以适应大数据分析的需求,于此同时不失去python语言的灵活性.

标准的dask集群部署方式(命令行方式)有大致3块结构:

+ 分布式的数据结构接口用于构造计算图
+ 调度器用于分发任务(启动命令`dask-scheduler`)
+ worker运算节点(启动命令`dask-worker tcp://{host}:8786`)

在此基础上还有几个借助已有分布式工具的部署方式:

+ docker方式,其实就是命令行方式,只是借助docker集群提供算力,也是本文使用的方式

+ Kubernetes方式,借助Kubernetes集群提供算力,它提供了docker方式不具备的动态调节资源的能力

+ YARN/Hadoop方式,借助YARN/Hadoop集群提供算力,这种方式相当于把调度器和worker承包给了yarn

+ 借助高性能计算框架作为调度器.这种一般公司没有.

## docker方式部署dask集群


下面是一个简易的docker-compose文件

```yml
version: "3.6"

services:
  scheduler:
    image: daskdev/dask
    hostname: dask-scheduler
    logging:
      options:
          max-size: "10m"
          max-file: "3"
    ports:
      - "8786:8786"
      - "8787:8787"
    command: ["dask-scheduler"]
  worker1:
    image: daskdev/dask
    hostname: dask-worker1
    logging:
      options:
          max-size: "10m"
          max-file: "3"
    command: ["dask-worker", "tcp://scheduler:8786"]
    
  worker2:
    image: daskdev/dask
    hostname: dask-worker2
    logging:
      options:
          max-size: "10m"
          max-file: "3"
    command: ["dask-worker", "tcp://scheduler:8786"]
    
  worker3:
    image: daskdev/dask
    hostname: dask-worker3
    logging:
      options:
          max-size: "10m"
          max-file: "3"
    command: ["dask-worker", "tcp://scheduler:8786"]

```

这个配置方式用来测试绰绰有余,但并不适合生产环境使用,生产环境建议使用`Kubernetes`方式或者`YARN/Hadoop`方式.如果非要用docker方式,那也注意一定不要用warm自带的overlay网络,可以使用host方式pubish端口,所有的网络流量通过宿主机ip走内网流量.

无论是swarm方式还是k8s方式部署dask集群,我们都需要用到dask的环境镜像[daskdev/dask](https://github.com/dask/dask-docker/tree/master/base).我们应该保持集群中每个节点使用的镜像一致,以防止不必要的麻烦

## 命令行方式的helloworld

命令行方式的核心是启动调度器,调度器有一个默认的管理界面在`8787`端口.这个界面上我们可以看到连接着的集群的各个节点信息,以及任务节点的分布情况.



而要使用集群计算我们需要连接到调度器的`8786`端口.这里我把远程机器上的调度器端口映射到了本地.


```python
from dask.distributed import Client
```


```python
client = Client('localhost:8786') 
```


```python
def square(x):
    return x ** 2
```


```python
A = client.map(square, range(10000))
total = client.submit(sum, A)
print(total.result())
```

    333283335000


dask集群任务的工作流基本都是一样:

1. 连接集群,实例化一个客户端对象
2. 利用封装好的分布式数据结构或者底层api构建计算图
3. 提交任务,调度执行

其他部署方式只是连接集群的方式不一样了而已


![dask工作流](source/collections-schedulers.png)

## dask的应用场景

dask是为大数据设计的,因此如果数据规模小实际上并不适合使用它.如果你的数据无法放到单机内存中那就可以使用它,反之,好好使用numpy吧.

dask不会让你的计算更快,它只是解决数据过大单机无法计算的问题,如果是为了让运算更快,建议使用numba或者cython加速,这个就是另一个话题了.
