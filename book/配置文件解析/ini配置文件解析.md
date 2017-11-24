
# 配置文件解析

项目通常会将一些全部局配置放在配置文件中.常见的配置文件格式有`.ini`,和`.yml`,有时候我们也会使用`.json`来作为配置文件.

python中,json前面已经讲过,而标准库的`ConfigParser`模块可以解析配置`.conf`,文件.`.yml`则需要使用第三方包`pyyaml`

## `.ini`文件解析

`.ini`文件形如下面

```ini
[DEFAULT]
serveraliveinterval = 45
compression = yes
compressionlevel = 9
forwardx11 = yes

[bitbucket.org]
user = hg

[topsecret.server.com]
port = 50022
forwardx11 = no
```

可以分为几个部分:

+ Sections 节,每个节代表一项配置系列

+ Case insensitivity 参数字段,具体要配置的字段对应的值

可以理解成一个两层的字典

### 写

`ConfigParser()`用于初始化一个解析器,这个解析器可以像字典一样使用


```python
import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {'ServerAliveInterval': '45',
                    'Compression': 'yes',
                    'CompressionLevel': '9'}
config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Port'] = '50022'     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'
with open('example.ini', 'w') as configfile:
    config.write(configfile)
```

### 读

初始化一个空的解析器后可以通过`.read`方法来读入一个已有的配置.


```python
config = configparser.ConfigParser()
config.sections()
```




    []




```python
config.read('example.ini')
```




    ['example.ini']



可以通过`sections`方法获取所有节


```python
config.sections()
```




    ['bitbucket.org', 'topsecret.server.com']




```python
'bitbucket.org' in config
```




    True




```python
'bytebong.com' in config
```




    False



获取到节后,就可以像操作字典一样操作这个节内的内容了


```python
for k,v in config['bitbucket.org'].items():
    print(k,v)
```

    user hg
    serveraliveinterval 45
    compression yes
    compressionlevel 9
    forwardx11 yes
    


```python
config['bitbucket.org']['User']
```




    'hg'




```python
config['DEFAULT']['Compression']
```




    'yes'




```python
topsecret = config['topsecret.server.com']
topsecret['ForwardX11']
```




    'no'




```python
topsecret['Port']
```




    '50022'




```python
for key in config['bitbucket.org']: print(key)
```

    user
    serveraliveinterval
    compression
    compressionlevel
    forwardx11
    

## `.yml`文件解析

`.yml`文件需要使用第三方包`pyyaml`来解析,据说效率很高.

`.yml`文件形如:

```yml
name: Silenthand Olleander
race: Human
traits: [ONE_HAND, ONE_EYE]
```

是很多现代项目的标准配置格式.比如gitpage默认的静态页面生成框架`jekyll`就是使用这种格式配置项目

### 写

pyyml可以像json一样直接将字典写成配置文件,甚至可以将pyhton对象写成配置文件


```python
import yaml
```


```python
so = {'name': 'Silenthand Olleander', 
      'race': 'Human',
      'traits': ['ONE_HAND', 'ONE_EYE']
     }
```


```python
so
```




    {'name': 'Silenthand Olleander',
     'race': 'Human',
     'traits': ['ONE_HAND', 'ONE_EYE']}




```python
print(yaml.dump(so))
```

    name: Silenthand Olleander
    race: Human
    traits: [ONE_HAND, ONE_EYE]
    
    


```python
with open("exsample.yml",'w') as f:
    f.write(yaml.dump(so))
```


```python
class Hero:
    def __init__(self, name, hp, sp):
        self.name = name
        self.hp = hp
        self.sp = sp
    def __repr__(self):
        return "%s(name=%r, hp=%r, sp=%r)" % (self.__class__.__name__, self.name, self.hp, self.sp)

```


```python
h= Hero("Galain Ysseleg", hp=-3, sp=2)
```


```python
print(yaml.dump(h))
```

    !!python/object:__main__.Hero {hp: -3, name: Galain Ysseleg, sp: 2}
    
    

### 读


```python
with open("exsample.yml") as f:
    result = yaml.load(f)
```


```python
result
```




    {'name': 'Silenthand Olleander',
     'race': 'Human',
     'traits': ['ONE_HAND', 'ONE_EYE']}


