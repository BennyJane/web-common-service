FROM python:3.6.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirement.txt /usr/src/app/requirement.txt

RUN pip install -r requirement.txt

ADD . /usr/src/app

CMD python main.py

