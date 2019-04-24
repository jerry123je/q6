#!/usr/bin/env python3

import boto3
import time

s3 = boto3.client('s3',region_name='cn-north-1')
#s3.download_file('tjji-test', 'haha.txt', 'haha.txt')
dynamodb = boto3.resource('dynamodb',region_name='cn-north-1')
table = dynamodb.Table('q6test1')

list=s3.list_objects(Bucket='tjji-test')['Contents']
#for key in list:
#    print(key)
#    s3.download_file('tjji-test', key['Key'], key['Key'])

for s3file in list:
#    print(s3file['Key'])
    if s3file['StorageClass'] == 'STANDARD':
        s3.download_file('tjji-test', s3file['Key'], s3file['Key'])
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
            'Bucket':'tjji-test',
            'Key': s3file['Key']
            },
            'tjji-test',
            s3file['Key'],
            ExtraArgs = {
                'StorageClass': 'GLACIER',
                'MetadataDirective': 'COPY'
            }
        )

