#!/usr/bin/env python3

import boto3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("fleetcapacity", type=int, default=0)
arg = parser.parse_args()

spotfleetid = 'sfr-41ba26bc-e06b-42a1-8ce8-9c057ee7e9c4'
ECSCluster_name = 'Q6Test'

spotfleet = boto3.client("ec2",region_name='cn-north-1') 

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
    if fleetstat == 'active':
        return currentcapacity
    else: 
        return 'NotAvailiable'

status = check_fleet_status(spotfleet,spotfleetid)
if status == 'NotAvailiable':
    print('fleet not availiable!')
else:
    scale_result = scale(spotfleet,arg.fleetcapacity)
    if scale_result == 'True':
        print('fleet modified')
        exit(0)
    else:
        print("Scale_result: %s , status: %s "%(scale_result,status))
