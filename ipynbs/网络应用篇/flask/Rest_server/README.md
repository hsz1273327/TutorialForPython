# REST服务

最近几年,Web 程序有种趋势,那就是业务逻辑被越来越多地移到了客户端一侧,开创出 了一种称为富互联网应用(Rich Internet Application,RIA)的架构。在 RIA 中,服务器的 主要功能(有时是唯一功能)是为客户端提供数据存取服务。在这种模式中,服务器变成 了 Web 服务或应用编程接口(Application Programming Interface,API)。
RIA 可采用多种协议与 Web 服务通信。最近,表现层状态转移 (Representational State Transfer,REST)架构崭 露头角,成为 Web 程序的新宠, 因为这种架构建立在大家熟识的万维网基础之上。
Flask 是开发 REST 架构 Web 服务的理想框架,因为 Flask 天生轻量。 接下来我们会学习如何使用 Flask 实现符合 REST 架构的 API。
Roy Fielding 在其博士论文(http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style. htm)中介绍了 Web 服务的 REST 架构方式,并列出了 6 个符合这一架构定义的特征。
客户端-服务器
客户端和服务器之间必须有明确的界线。
无状态
客户端发出的请求中必须包含所有必要的信息。服务器不能在两次请求之间保存客户端的任何状态。
缓存
服务器发出的响应可以标记为可缓存或不可缓存,这样出于优化目的,客户端(或客户端和服务器之间的中间服务)可以使用缓存。
接口统一
客户端访问服务器资源时使用的协议必须一致,定义良好,且已经标准化。REST Web 服务最常使用的统一接口是 HTTP 协议。
系统分层
在客户端和服务器之间可以按需插入代理服务器、缓存或网关,以提高性能、稳定性和伸缩性。
按需代码
客户端可以选择从服务器上下载代码,在客户端的环境中执行。

## 资源

**资源**是 REST 架构方式的核心概念。在 REST 架构中,资源是程序中你要着重关注的事物。
例如,在博客程序中,用户、博客文章和评论都是资源。有的甚至直接允许调用数据库.


## http请求方法

请求方法 |目 标|说明|举例 |HTTP状态码
---|---|---|---|---
GET |单个资源的 URL |获取目标资源|http://example.com/api/orders| 200
GET |资源集合的 URL|获取资源的集合(如果服务器实现了分页,就是一页中的资源)| http://example.com/api/orders/123 |200  
POST |资源集合的 URL |创建新资源,并将其加入目标集合。服务器为新资源指 201 派 URL,并在响应的 Location 首部中返回|http://example.com/api/orders|200
PUT |单个资源的 URL|修改一个现有资源。如果客户端能为资源指派 URL,还可用来创建新资源|http://example.com/api/orders/123| 200
DELETE |单个资源的 URL |删除一个资源|http://example.com/api/orders/123 |200
DELETE |资源集合的 URL|删除目标集合中的所有资源|http://example.com/api/orders| 200

一般的返回的数据也是Json数据,python标准库提供了解析工具,但更好的选择是使用flask自带的jsonify方法,但我们用flask-Restful可以都不用,他会自动转成json


本篇分为以下几个部分

1. 路由控制
+ request和response处理
+ 异常抛出
+ 中间件flask-restful
+ 中间件flask-restaction
+ 数据库
+ 安全与验证
