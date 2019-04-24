FROM ubuntu:16.04
MAINTAINER tjji@nwcdcloud.cn

RUN apt-get update\
&& DEBIN_FRONTEND=noninteractive apt-get install -y python3 python3-pip\
&& pip3 install awscli boto3 --upgrade --user

COPY s3download.py /sbin/s3download.py
RUN chmod 755 /sbin/s3download.py

ENTRYPOINT ["/sbin/s3download.py"]
