#!/usr/bin/env python3

import boto3
import time

bucket_name = 'tjji-testbjs'

s3 = boto3.client('s3',region_name='cn-north-1')
dynamodb = boto3.resource('dynamodb',region_name='cn-north-1')
table = dynamodb.Table('q6test1')

list = s3.list_objects(Bucket=bucket_name)['Contents']

for s3file in list:
    if s3file['StorageClass'] == 'STANDARD':
        s3.download_file(bucket_name, s3file['Key'], s3file['Key'])
        with open(s3file['Key']) as f:
            a = f.read()
            #print(a)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        response = table.put_item(
            Item={
                'update_date': current_time,
                'file_name': s3file['Key']
            }
        )
        s3.copy(
            {
            'Bucket': bucket_name,
            'Key': s3file['Key']
            },
            bucket_name,
            s3file['Key'],
            ExtraArgs = {
                'StorageClass': 'GLACIER',
                'MetadataDirective': 'COPY'
            }
        )

