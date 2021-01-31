FROM python:3.7
ENV PATH /usr/local/bin:$PATH
COPY . /usr/src/spider/
WORKDIR /usr/src/spider/

RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple \
    && pip install -r requirements.txt && mkdir logs