# watch list

使用 flask 完成的电影列表项目

参考了[helloflask](https://read.helloflask.com/), 加入了自己的配置

## 项目结构

```bash
├── db/             # 数据库文件
├── models/         # 模型
├── routes/         # 路由
├── static/         # 静态目录
├── tests/          # 测试
├── templates/      # 模板
├── app.py          # 入口文件
├── commands.py     # 命令
├── config.py       # 配置
└── context.py      # 上下文管理
```

## 安装

```bash
$ git clone https://github.com/hacker0limbo/watchlist
$ cd watchlist
$ flask initdb
$ flask forge
$ flask run
* Running on http://localhost:8000/
```

## 关于 flask config 文件配置
- https://pythonise.com/series/learning-flask/flask-configuration-files

## 关于测试
- http://kronosapiens.github.io/blog/2014/08/14/understanding-contexts-in-flask.html
- https://stackoverflow.com/questions/17375340/testing-code-that-requires-a-flask-app-or-request-context

## 关于 api 设计的参考
- https://stackoverflow.com/questions/28795561/support-multiple-api-versions-in-flask

## 关于将 orm 实例转成 dict 对象
- https://stackoverflow.com/a/30280750

## 关于重写 __hash__ 和 __eq__
- https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes

## 关于 flask-login 项目的基本操作
- https://scotch.io/tutorials/authentication-and-authorization-with-flask-login

## 关于 flask-uploads 上传文件的实例
- https://zhuanlan.zhihu.com/p/23731819