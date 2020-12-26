# web-common-service
该项目实现了web开发中常用的功能模块，可作为独立项目为其他项目提供方便的接口。

### 项目涉及的核心技术:
  - flask
  - flask-restful
  - apscheduler

### 主要功能  
- 用户管理
    - 注册
    - 登录
    - 修改密码
    - 退出
    - 通过账号获取token
    - token刷新
    - 验证码
- 邮件模块
    - 添加模板
    - 修改模板
    - 获取模板列表
    - 异步发送邮件
- 定时任务
    - 添加定时任务
    - 更新定时任务
    - 获取任务列表
    - 删除定时任务
- 文件上传与下载
    - 上传文件
    - 下载文件
    - 预览文件
    - 更新配置信息

### 项目本地运行
1. 添加数据库连接
项目需要用到Mysql与redis数据库,先在本地项目根目录下创建 .env 文件，内容如下：
需要填写本地mysql、redis数据库以及邮件发送的信息
```shell script
FLASK_ENV=development
FLASK_APP=main:app
SQLALCHEMY_DATABASE_URI=mysql+pymysql://{user}:{password}@{host}:{port}/common_web_service?charset=utf8mb4
FLASK_SECRET=custom_session_key
MAIL_SERVER=邮箱服务器,例如 smtp.qq.com
MAIL_USERNAME=发送邮件的邮箱
MAIL_PASSWORD=发送邮件的密码
```

2.运行项目
```shell script
# 项目根目录运行
pip install -r requirement.txt
flask run
```


### 运行mysql镜像
```shell script
cd ./deploy/mysql
docker-compose build -t 'mysql-db'
docker-compose up -d

docker run --name mysql-home -e MYSQL_ROOT_PASSWORD=password -p 13306:3306 -d db_mysql-db
```

### 运行redis镜像
```shell script
cd ./deploy/redis
docker-compose build
docker-compose up -d

docker run --name mysql-home -e MYSQL_ROOT_PASSWORD=password -p 13306:3306 -d db_mysql-db
```

### Docker 使用
使用docker运行改项目，前提是本地mysql，redis服务已经启动。
```shell script
docker build -t 'common-service:v1.0' .
docker run -it -p 8002:8002 common-service:v1.0
docker run -d -p 8002:8002 common-service:v1.0

# 使用docker-compose 
# 后面不需要跟路径 .
docker-compose build
docker-compose up -d
```


### TDDO

- ## 功能
    - 文件上传
        - 添加在线存储方案
    - 第三方登录授权
        - 微信登录授权
        - QQ登录授权
        - github登录授权
        - 微博
    - 数据统计
        - 添加行为日志
        - 添加接口统计分析任务
    - 项目部署
        - 优化Docker部署
        - 单独添加部署文档 
- ## 代码优化
    - 优化数据格式验证模块
    - 优化jwt模块：修改为使用jwt扩展包 
    - 优化ReqJson类与接口类的使用方法：减少reqJson的引入次数
