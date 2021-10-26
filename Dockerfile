FROM macroldj/python:3.7-slim-django2.2.13
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
RUN sed -i 's/http\:\/\/deb.debian.org/https\:\/\/mirrors.aliyun.com/g' /etc/apt/sources.list \
 && sed -i 's/http\:\/\/security.debian.org/https\:\/\/mirrors.aliyun.com/g' /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y curl \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /home/workspace
RUN pip3 install --upgrade pip --no-cache-dir  -i https://mirrors.aliyun.com/pypi/simple/
ADD ./requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir  -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
                                 -r /tmp/requirements.txt && rm -rf /tmp/requirements.txt
COPY . .
CMD ["/bin/bash"]