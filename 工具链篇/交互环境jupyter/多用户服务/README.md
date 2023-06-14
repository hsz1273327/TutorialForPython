# 多用户服务

jupyter的多用户服务使用`Jupyter hub`.这是一套部署方案,大体上逻辑如下图:

![jupyter hub](../../source/jupyter/jhub-fluxogram.jpeg)

用户在hub层进行分流,分别交给不同的spawner执行.对于每个用户来说jupyter hub都应该是一个沙箱,他们之间数据并不该共通.

`jupyter hub`有多种部署方案,可以支持从100人以内的小团队到100人以上大团队的需求.本文将介绍在不同规模下个人认为最靠谱的部署方案.

本文仅介绍`Jupyter Lab`作为前端的`jupyter hub`部署方案.