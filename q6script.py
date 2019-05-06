#!/usr/bin/env python3

import boto3
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("fleetcapacity", type=int, default=0)
arg = parser.parse_args()

region_spec = 'cn-north-1'
spotfleetid = 'sfr-41ba26bc-e06b-42a1-8ce8-9c057ee7e9c4'
ECSCluster_name = 'Q6Test'
spotfleet = boto3.client("ec2",region_name=region_spec) 
bucket_name = 'tjji-testbjs'
dynamodb_table = 'q6test1'

def s3download(region_spec,bucket_name,dynamodb_table):
    s3 = boto3.client('s3',region_name=region_spec)
    list = s3.list_objects(Bucket=bucket_name)['Contents']
    
    dynamodb = boto3.resource('dynamodb',region_name=region_spec)
    table = dynamodb.Table(dynamodb_table)

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

def scale(spotfleet, capacity):
    response = spotfleet.modify_spot_fleet_request(
        ExcessCapacityTerminationPolicy = 'default',
        SpotFleetRequestId = spotfleetid,
        TargetCapacity = capacity
    )
    return response['Return']

def check_fleet_status(spotfleet,spotfleetid):
    response = spotfleet.describe_spot_fleet_requests(
        SpotFleetRequestIds = [ spotfleetid, ]
    )
    fleetstat = response['SpotFleetRequestConfigs'][0]['SpotFleetRequestState']
    currentcapacity = int(response['SpotFleetRequestConfigs'][0]['SpotFleetRequestConfig']['FulfilledCapacity'])
    targetcapacity = int(response['SpotFleetRequestConfigs'][0]['SpotFleetRequestConfig']['TargetCapacity'])
    print("Fleet status: %s"%fleetstat)
    print("Current capacity: %d"%currentcapacity)
    print("Target capacity: %d"%targetcapacity)
    return targetcapacity

s3download(region_spec,bucket_name,dynamodb_table)    
scale_result = scale(spotfleet,arg.fleetcapacity)
time.sleep(30)
status = check_fleet_status(spotfleet,spotfleetid)
if status == arg.fleetcapacity:
    print('fleet modified')
else:
    print("Scale_result: %s"%scale_result)
