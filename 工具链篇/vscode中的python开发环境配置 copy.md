# vscode中的python开发环境配置

python自带的idel体验是比较差的,企业里python项目开发通常有两种流派:

+ [PyCharm](https://www.jetbrains.com/pycharm/promo/?source=google&medium=cpc&campaign=14124131751&term=pycharm&content=536947779540&gad=1&gclid=EAIaIQobChMI_br9wbeZ_wIVPjWtBh0XKw2QEAAYASAAEgLf-_D_BwE)派,作为专业的python ide,PyCharm在各个方面都是最好的,非要说缺点也就是比较吃资源,不过现在的多数电脑都是资源过剩的这一般也不是问题.但PyCharm作为一个商业软件,授权价格不便宜.当然了嫌贵是用户的问题不是产品的问题.

+ 文本编辑器,比如`vim`,`notepad++`啥的,通常文本编辑器的优点是免费,缺点通常是缺少对特定语言的支持.

看本文标题就知道本人更加推荐使用vscode来开发python项目.[vscode](https://code.visualstudio.com/)是微软发布的一个免费的文本编辑器.它的本体就是一个基于[electron](https://www.electronjs.org/)的文本编辑器,但进行了非常多的优化,克服了electron的性能问题,同时它提供了可插拔扩展的能力让它可以借助扩展适应几乎任何需求.

vscode方案属于第二种流派,但它比传统文本编辑器好用很多,配置得当使用上堪比PyCharm.而且更可贵的是如果你

具体如何使用可以查看[我的这篇博客](https://blog.hszofficial.site/recommend/2020/10/26/Vscode%E9%85%8D%E7%BD%AE/)