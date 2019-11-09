# watch list

使用 flask 完成的电影列表项目

参考了[helloflask](https://read.helloflask.com/), 加入了自己的配置

## 项目结构

```bash
├── db/             # 数据库文件
├── models/         # 模型
├── routes/         # 路由
├── static/         # 静态文件
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
