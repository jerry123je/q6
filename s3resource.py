#!/usr/bin/env python3

import boto3

#s3 = boto3.resource('s3',region_name='cn-north-1')
s3 = boto3.resource('s3')
bucket = s3.Bucket('tjji-ami')
#for obj in bucket.objects.all():
#    print(obj.key, obj.last_modified)
bucket.upload_file('text1.txt','text1.txt')
