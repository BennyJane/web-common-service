FROM python:3.6.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -U setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --no-cache-dir -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app", "--preload"]

