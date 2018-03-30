
# 使用sqlite3共享内存

多进程程序往往碰到一个问题:数据共享问题.这也是本文的主题.

## 简单介绍sqlite3

sqlite3是一个非常伟大的关系型数据库,可能很多人不太熟悉.人言关系型数据库一般都是mysql,MS Sqlserver,Oracle,但其实sqlite同样是非常出色的关系型数据库.

从代码的角度讲,sqlite堪称教科书般的C语言编程示例(一般也是作为学习C语言的参考代码).

从性能角度讲,sqlite因为是基于磁盘io的,所以基于socket的数据库性能与他完全不能相比.它更有内存模式,比起磁盘模式更加快速.

从用途来讲,sqlite3编译后非常小,可以放入资源十分有限的嵌入式设备中,光这一点其他数据库就无法做到.在追求高时效性的任务中可以使用内存模式当作内存数据库使用.

从使用范围来讲,只要是嵌入式设备,包括手机,一些物联网终端在内,都有使用.它不光可以用在服务器上也可以用在客户端作为缓存.连html5都有对其的阉割支持(虽然已经被废弃).

sqlite最大的缺点同样来自于它基于磁盘而非socket.这一特点让它不适合作为数据存储的中心节点.不过sqlite3非常适合微服务架构,因为它是自治的,并且利于迁移(一个文件拷贝走就是了),如果项目的数据增量比较可控,并且对实时性有较高要求完全可以使用sqlite3.

python的标准库中内置了sqlite3支持.基本上只要装了python就可以使用sqlite3.并且,sqlite3使用的是python通用的数据库接口设计,一通百通,会用它就会用其他的数据库接口

### 连接数据库 


```python
import sqlite3
conn = sqlite3.connect('test.db')
```

### 创建表格

数据库的操作使用游标(cursor)实现.游标对象有`execute`方法用来将sql语句输入到连接中,之后再调用连接的`commit`方法将sql语句上传到数据库进行操作.


```python
c = conn.cursor()
c.execute('''CREATE TABLE COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')
conn.commit()
```

### 插入数据


```python
c = conn.cursor()

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )");

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");

conn.commit()
```

### 查询


```python
c = conn.cursor()

cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("ADDRESS = ", row[2])
    print("SALARY = ", row[3], "\n")

```

    ID =  1
    NAME =  Paul
    ADDRESS =  California
    SALARY =  20000.0 
    
    ID =  2
    NAME =  Allen
    ADDRESS =  Texas
    SALARY =  15000.0 
    
    ID =  3
    NAME =  Teddy
    ADDRESS =  Norway
    SALARY =  20000.0 
    
    ID =  4
    NAME =  Mark
    ADDRESS =  Rich-Mond 
    SALARY =  65000.0 
    
    

### 更新


```python
c = conn.cursor()


c.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
conn.commit()
print("Total number of rows updated :", conn.total_changes)

cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("ADDRESS = ", row[2])
    print("SALARY = ", row[3], "\n")

```

    Total number of rows updated : 5
    ID =  1
    NAME =  Paul
    ADDRESS =  California
    SALARY =  25000.0 
    
    ID =  2
    NAME =  Allen
    ADDRESS =  Texas
    SALARY =  15000.0 
    
    ID =  3
    NAME =  Teddy
    ADDRESS =  Norway
    SALARY =  20000.0 
    
    ID =  4
    NAME =  Mark
    ADDRESS =  Rich-Mond 
    SALARY =  65000.0 
    
    

### 替换


```python
c = conn.cursor()

c.execute("REPLACE INTO COMPANY (ID, NAME, AGE, ADDRESS, SALARY) VALUES ('2', 'Allen', 'Texas', '123456@qq.com', 16000.0 );")
conn.commit()
print("Total number of rows updated :", conn.total_changes)

cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("ADDRESS = ", row[2])
    print("SALARY = ", row[3], "\n")
```

    Total number of rows updated : 6
    ID =  1
    NAME =  Paul
    ADDRESS =  California
    SALARY =  25000.0 
    
    ID =  3
    NAME =  Teddy
    ADDRESS =  Norway
    SALARY =  20000.0 
    
    ID =  4
    NAME =  Mark
    ADDRESS =  Rich-Mond 
    SALARY =  65000.0 
    
    ID =  2
    NAME =  Allen
    ADDRESS =  123456@qq.com
    SALARY =  16000.0 
    
    

### 删除


```python
c = conn.cursor()
c.execute("DELETE from COMPANY where ID=2;")
conn.commit()
print("Total number of rows deleted :", conn.total_changes)

cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("ADDRESS = ", row[2])
    print("SALARY = ", row[3], "\n")
```

    Total number of rows deleted : 7
    ID =  1
    NAME =  Paul
    ADDRESS =  California
    SALARY =  25000.0 
    
    ID =  3
    NAME =  Teddy
    ADDRESS =  Norway
    SALARY =  20000.0 
    
    ID =  4
    NAME =  Mark
    ADDRESS =  Rich-Mond 
    SALARY =  65000.0 
    
    

### 断开连接


```python
conn.close()
```

## 内存模式

sqlite可以使用缓存模式,用法很简单,就是把db文件位置的字符串改为`":memory:"`.不过注意这种方式并不能共享内存,它相当于每个连接独立在内存中存储数据.一旦断开数据就被释放了.

## 线程安全问题


sqlite默认是线程安全的,它在同一个时间只会有一次commit在访问数据.而其他的commit则在外面被阻塞着.如果要去掉阻塞,可以在连接时指定`check_same_thread`为`False`.当然了,这样的话线程安全就得手工管理了.

## 缓存模式用于多线程

如果要让内存用于多线程,那么就要共享缓存.python的sqlite3接口没有对应的参数.但3.4新增的参数`uri`可以实现这个功能

### 不同连接使用内存数据库的示例 (来自stack overflow)

可以看到db1和db2连接的是同一个名字的数据库`foobar_database`.他们一个创建表一个插入数据.最终都可以访问到.这就为多个进程访问共同的内存数据提供了支持


```python
import sqlite3

foobar_uri = 'file:foobar_database?mode=memory&cache=shared'
not_really_foobar_uri = 'file:not_really_foobar?mode=memory&cache=shared'

# connect to databases in no particular order
db2 = sqlite3.connect(foobar_uri, uri=True)
db_lol = sqlite3.connect(not_really_foobar_uri, uri=True)
db1 = sqlite3.connect(foobar_uri, uri=True)

# create cursor as db2
cur2 = db2.cursor()
cur1 = db1.cursor()
# create table as db2
db2.execute('CREATE TABLE foo (NUMBER bar)')

# insert values as db1
db1.execute('INSERT INTO foo VALUES (42)')
db1.commit()

# and fetch them from db2 through cur2
cur2.execute('SELECT * FROM foo')
print(cur2.fetchone()[0])  # 42
cur1.execute('SELECT * FROM foo')
print(cur1.fetchone()[0])  # 42
# test that db_lol is not shared with db1 and db2
try:
    db_lol.cursor().execute('SELECT * FROM foo')
except sqlite3.OperationalError as exc:
    print(exc)  # just as expected
    
db2.close()
db1.close()
```

    42
    42
    no such table: foo
    


```python
sqlite3.sqlite_version_info
```




    (3, 14, 2)



### 多线程共享内存数据库 


```python
import os, time
import sqlite3
import threading


def write(name):
    print("write db in",name)
    import sqlite3
    foobar_uri = 'file:foobar_database?mode=memory&cache=shared'
    conn = sqlite3.connect(foobar_uri, uri=True)
    c = conn.cursor()
    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");
    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");
    conn.commit()
    conn.close()
    print("write db done")
    

def main():
    foobar_uri = 'file:foobar_database?mode=memory&cache=shared'
    conn = sqlite3.connect(foobar_uri, uri=True)
    c = conn.cursor()
    c.execute('''CREATE TABLE COMPANY
           (ID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL);''')
    conn.commit()
    c = conn.cursor()
    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (1, 'Paul', 32, 'California', 20000.00 )");
    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");
    conn.commit()
    pr = threading.Thread(target=write,args=("write Thread",))
    pr.start()
    pr.join()
    print("read db")
    c = conn.cursor()
    cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print("ID = ", row[0])
        print("NAME = ", row[1])
        print("ADDRESS = ", row[2])
        print("SALARY = ", row[3], "\n")
    conn.close()
    
main()
```

    write db in write Thread
    write db done
    read db
    ID =  1
    NAME =  Paul
    ADDRESS =  California
    SALARY =  20000.0 
    
    ID =  2
    NAME =  Allen
    ADDRESS =  Texas
    SALARY =  15000.0 
    
    ID =  3
    NAME =  Teddy
    ADDRESS =  Norway
    SALARY =  20000.0 
    
    ID =  4
    NAME =  Mark
    ADDRESS =  Rich-Mond 
    SALARY =  65000.0 
    
    

## sqlite3用于多进程


sqlite3的内存模式并不支持多进程,不过如果使用linux,那么就可以简单的让sqlite3直接使用RAM而不用通过文件io.

这种方式比较鸡贼.不光是sqlite,其他的文件也可以这样使用.

linux中有`/dev/shm`目录,这个目录不在硬盘上而在内存上,所以如果将sqlite3的数据库文件放在这上面,那就可以像正常那样多进程使用内存中的sqlite数据库了.
