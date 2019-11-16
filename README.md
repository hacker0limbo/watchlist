# watch list

使用 flask 完成的电影列表项目

## 项目截图

![demo](demo/watchlist_demo.gif)

## 项目结构

```bash
├── db/             # 数据库文件
├── models/         # 模型
├── reports/        # 测试覆盖率报告
├── routes/         # 路由
├── static/         # 静态目录
├── tests/          # 测试
├── templates/      # 模板
├── app.py          # 入口文件
├── commands.py     # 命令
├── config.py       # 配置
├── context.py      # 上下文管理
└── .flaskenv       # 开发环境变量
```

## 项目功能

基本功能包括:
- 登录登出, 注册新用户
- 对 watch list 的增删改查
- 用户修改个人信息包括: 密码更新, 头像上传

用户权限:
- `admin 用户`: 用户账号密码均为`admin`(可在`commands.py`里面找到), 可以对 watch list 进行完整的增删改查功能
- `普通用户`: 使用页面注册, 或者`flask new-user`注册的新用户均为普通用户, 只能对 watch list 进行增加, 不得更新和删除

## 项目运行

### 安装依赖与初始化
```bash
$ git clone https://github.com/hacker0limbo/watchlist
$ cd watchlist
$ pip3 install -r requirements.txt
$ flask initdb
$ flask forge
$ flask run
* Running on http://localhost:8000/
```

### 命令行

自定义命令包括: `flask initdb`, `flask forge`, `flask new-user`, `flask test`, `flask coverage`
可以通过 `flask --help` 查看

```bash
$ flask --help # 查看所有命令
...
Commands:
  coverage  输出覆盖率测试
  forge     产生 mock 数据
  initdb    初始化数据库表的 schema
  new-user  手动生成新的用户数据
  routes    Show the routes for the app.
  run       Run a development server.
  shell     Run a shell in the app context.
  test      运行测试
```

#### flask initdb [--drop]
- `flask initdb`: 用于初始化数据库表结构
- `flask initdb`: --drop` drop 已有的表, 重新生成数据库与表结构

#### flask forge
- `flask forge`: 用于生成 mock 数据, 包括 **admin 用户**和**电影信息**

#### flask new-user
- `flask new-user`: 用于生成新普通用户

```bash
$ flask new-user
...
Username: limboer
Password:
Repeat for confirmation:
Creating new user...
Done.
```

#### flask test
- `flask test`: 运行 `tests/` 目录下的所有测试文件

#### flask coverage [--html]
- `flask coverage`: 在终端输出测试报告
- `flask coverage --html`: 在 `reports/coverage` 目录生成 `index.html` 的 html 形式报告

## 参考

### 项目基本
- [helloflask](https://read.helloflask.com/), 基础部分均参考于此

### 问题记录

- 关于 flask config 文件配置
  - https://pythonise.com/series/learning-flask/flask-configuration-files
- 关于测试
  - http://kronosapiens.github.io/blog/2014/08/14/understanding-contexts-in-flask.html
  - https://stackoverflow.com/questions/17375340/testing-code-that-requires-a-flask-app-or-request-context
- 关于 api 设计的参考
  - https://stackoverflow.com/questions/28795561/support-multiple-api-versions-in-flask
- 关于将 orm 实例转成 dict 对象
  - https://stackoverflow.com/a/30280750
- 关于重写 __hash__ 和 __eq__
  - https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes
- 关于 flask-login 项目的基本操作
  - https://scotch.io/tutorials/authentication-and-authorization-with-flask-login
- 关于 flask-uploads 上传文件的实例
  - https://zhuanlan.zhihu.com/p/23731819