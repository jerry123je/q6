FROM ubuntu:16.04
MAINTAINER tjji@nwcdcloud.cn

RUN apt-get update\
&& DEBIN_FRONTEND=noninteractive apt-get install -y python3 python3-pip\
&& pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com  awscli boto3 --upgrade --user

COPY q6script.py /sbin/q6script.py
RUN chmod 755 /sbin/q6script.py

ENTRYPOINT ["/sbin/q6script.py", "0"]
