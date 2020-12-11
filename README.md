# web-common-service
该项目实现了web开发中常用的功能模块，可作为独立项目为其他项目提供方便的接口。

### 项目涉及的核心技术:
  - flask
  - flask-restful
  - apscheduler

### 项目主要功能  
- 用户管理
    - 注册
    - 登录
    - 修改密码
    - 退出
    - 通过账号获取token
    - token刷新
- 邮件模块
    - 添加模板
    - 修改模板
    - 获取模板列表
    - 异步发送邮件
- 定时任务
    - 添加定时任务
    - 更新
    - 获取任务列表
    - 删除任务
- 文件上传与下载
    - 上传文件
    - 下载文件
    - 预览文件
    - 更新配置信息

### 项目运行
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


- 文件上传
    - 添加在线存储方案
