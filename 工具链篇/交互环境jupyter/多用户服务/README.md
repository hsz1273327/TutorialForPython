# 多用户服务

jupyter的多用户服务使用`Jupyter hub`.这是一套部署方案,大体上逻辑如下图:

![jupyter hub](../../source/jupyter/jhub-fluxogram.jpeg)

用户在hub层进行分流,分别交给不同的spawner执行.对于每个用户来说jupyter hub都应该是一个沙箱,他们之间数据并不该共通.

`jupyter hub`有多种部署方案,可以支持从100人以内的中小团队到100人以上大团队的需求.本文将介绍在不同规模下个人认为最靠谱的部署方案.

本文仅介绍`Jupyter Lab`作为前端的`jupyter hub`部署方案,需要有如下先验知识:


1. ssh相关知识.可以查看[我的这篇介绍文章](https://blog.hszofficial.site/introduce/2020/10/22/%E5%85%B3%E4%BA%8Essh%E7%9A%84%E6%8A%80%E5%B7%A7/)
2. docker/docker swarm相关知识.可以查看[我的这篇介绍文章](https://blog.hszofficial.site/TutorialForDocker/#/)
3. k8s相关知识.

同时在项目[Basic-Components/base-image-for-jupyterhub](https://github.com/Basic-Components/base-image-for-jupyterhub)中我构造了常用的jupyter相关基镜像.