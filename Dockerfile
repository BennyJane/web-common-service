FROM python:3.6.4

MAINTAINER Benny Jane

RUN mkdir -p /usr/src/app \
    && mkdir -p /usr/src/logs/gunicorn \
    && mkdir -p /usr/src/logs/web

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -U setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --no-cache-dir -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8020

ENTRYPOINT ["/bin/bash", "/usr/src/app/deploy.sh"]


