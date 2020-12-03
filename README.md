# web-common-service
There are some common functions of web development

core technology:
  - flask
  - flask-restful
  - celery



core function:  
- login/logout
- download/upload  
- cron  
- mail 


### Docker 使用
运行docker文件
```shell script
docker build -t 'common-service:v1.0' .
docker run -it -p 8002:8002 common-service:v1.0
docker run -d -p 8002:8002 common-service:v1.0


# 使用docker-compose 
# 后面不需要跟路径 .
docker-compose build
docker-compose up -d
```

