
# `*`jupyter notebook作为服务器

jupyter notebook本来就是一个基于浏览器的服务,它默认在`localhost:8888`启动.我们可以通过修改一些启动参数来将它对外.这种方式并不推荐,因为每次都得手动输入参数很繁琐. jupyter 提供了一个命令为我们生成一份配置文件放在`~/.jupyter`目录下.

```shell
jupyter notebook --generate-config
```

我们可以修改其中的
```python
c.NotebookApp.ip = '*'#或者'0.0.0.0'
c.NotebookApp.open_browser = False# 服务启动不打开浏览器
c.NotebookApp.port = <你指定的端口>
```
就可以使用了



# 安全措施

jupyter notebook直接暴露在外显然是不安全的,解决安全问题有两个思路:

1. 加密

2. 使用私有通道

## 加密

### 访问密码

jupyter notebook可以使用`jupyter notebook password`命令创建密码,创建完成后他会保存在`~/.jupyter`目录下.形如:

```json
{
  "NotebookApp": {
    "password": "sha1:xxxxxxxxx"
  }
}

```
将其中的`password`内容复制到上面的配置文件中的`c.NotebookApp.password = u'xxxx'`中,那么访问的时候如果浏览器没有cookie保存着这个信息就会要求输入密码了

### ssl密文通信

启动的时候加上参数`jupyter notebook --certfile=mycert.pem --keyfile mykey.key`就可以使用ssl加密通信了(https).当然更好的方式是修改配置文件

```python
c.NotebookApp.certfile = u'/absolute/path/to/your/certificate/mycert.pem'
c.NotebookApp.keyfile = u'/absolute/path/to/your/certificate/mykey.key'
```

## 使用ssh私有通道

ssh隧道技术简单说就是将一个远端端口映射到本地一个端口,这样信息就都是通过ssh来传递了.在linux或者mac中这样启动:

```bash
ssh -N -f -L [remote port]:localhost:[local port] -p [ssh port] -l [username] [公网IP]

```

在windows中ssh工具使用很作孽,我们可以使用xshell来代替:

![xshell建立ssh隧道](source/Xshell建立ssh隧道.png)

我们架设要将7777端口映射到本地7777端口,那么在yu远端启动的时候配置文件中这样写
```python
c.NotebookApp.ip = 'localhost'
c.NotebookApp.open_browser = False# 服务启动不打开浏览器
c.NotebookApp.port = 7777

```
然后使用`jupyter notebook`启动服务即可.我们就可以使用本地的浏览器访问本地的7777端口来访问远端的notebook了

后台启动可以使用nohup 或者使用supervisor统一管理都可以.

## 使用jupyterhub解决多用户访问问题

使用ssh私有通道的方式可能更加安全些,但这没有改变一个问题:

多用户下的文件修改冲突问题.

官方的解决方案是使用`jupyterhub`

[jupyterhub](https://github.com/jupyterhub/jupyterhub)是notebook的衍生,专门用来管理多用户.它默认使用服务器机器上的用户作为用户,并且启动时需要`sudo`权限.

JupyterHub需要python3.4+和node.js的`configurable-http-proxy`库

安装使用以下步骤:

+ python3 -m pip install jupyterhub
+ npm install -g configurable-http-proxy

安装完毕后,类似jupyter notebook,jupyterhub也可以创建一个配置文件模板

```bash
jupyterhub --generate-config
```

这样就会在运行命令的当前目录下创建一个配置文件`jupyterhub_config.py`.要使用这个配置文件只需要使用`-f`指定即可

```bash
sudo jupyterhub -f jupyterhub_config.py
```

要正常的运行需要修改配置文件如下:

```python
c.JupyterHub.admin_access = True # 让admin账号可以控制或者进入非admin账户
c.Authenticator.whitelist = {<你当前的系统账号>} #将当前的系统账号设为白名单
c.Authenticator.admin_users={<你当前的系统账号>}#将当前的系统账号设为admin账号
c.JupyterHub.ip = '0.0.0.0'#设置外网可以访问
c.JupyterHub.port = 5888#设置端口
c.Spawner.cmd = ['/path/to/jupyterhub-singleuser']#将`jupyterhub-singleuser`写死
c.JupyterHub.ssl_cert = ''#设置ssl的证书文件地址,不用https可以不设置
c.JupyterHub.ssl_key = ''#设置ssl的证书的key文件地址,不用https可以不设置
```

之后运行即可.登录账号即为你当前的系统账号,密码为当前系统的登录密码
