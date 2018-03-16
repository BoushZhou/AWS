#===================================================#
#This scrips is that how to export IaaS Service(EC2） in AWS
#IaaS Service: EC2
#.NOTE:
#            Author: Luna-Star
#            Last Updated: 03/15/2018
#            Version 1.1
#===================================================#
import boto3
import csv
#Key & ID
aws_access_id = "*****"
aws_secret_key = "*********"
region = "cn-north-1"
#defin session
session = boto3.Session(aws_access_key_id=aws_access_id,
                        aws_secret_access_key=aws_secret_key,
                        region_name=region);
#define resource high level in boto3
ec2 = session.resource('ec2')
#List EC2 and Export CSV
headers = ['EC2_Name','EC2_ID','EBS_Map','EBS_DeleteOnTermination','EBS_Encrypted','EBS_ID','EBS_IOPS',
           'EBS_Size','EBS_Snapshot_id','EBS_Type','EBS_Name','EBS_State','EBS_AZ']
#List EBS and Export CSV
def split_list(liststring):
    while(liststring == None):
        liststring = [{'DeleteOnTermination': '---', 'Value': '===', 'InstanceId': '---', 'Device': '---'}]
    return liststring
#list the info vpc&subnet&network_interface
with open('D:\Aws_EBS.csv','w',encoding='utf-8',newline=') as File:
    File_csv = csv.writer(File)
    File_csv.writerow(headers)
    for ebs in ec2.volumes.all():
        if (ebs.attachments == []):
            attach_info = None
            instance = "---"
        else:    
            attach_info = ebs.attachments
            instance_int=ec2.Instance(ebs.attachments[0].get("InstanceId"))
            instance = split_list(instance_int.tags)[0]["Value"]
        if (ebs.snapshot_id ==''):
            snapshotid = "==="
        else:
            snapshotid = ebs.snapshot_id
        print(instance,split_list(attach_info)[0]["InstanceId"],split_list(attach_info)[0]["Device"],
              split_list(attach_info)[0]["DeleteOnTermination"],ebs.encrypted,ebs.id,ebs.iops,ebs.size,snapshotid,ebs.volume_type,split_list(ebs.tags)[0]["Value"],
              ebs.state,ebs.availability_zone)
        rows=[instance,split_list(attach_info)[0]["InstanceId"],split_list(attach_info)[0]["Device"],
              split_list(attach_info)[0]["DeleteOnTermination"],ebs.encrypted,ebs.id,ebs.iops,ebs.size,snapshotid,ebs.volume_type,split_list(ebs.tags)[0]["Value"],
              ebs.state,ebs.availability_zone]
        File_csv.writerow(rows)
