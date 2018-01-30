#===================================================#
#This scrips is that how to export IaaS Service(EC2） in AWS
#IaaS Service: EC2
#.NOTE:
#            Author: Luna-Star
#            Last Updated: 11/15/2017
#            Version 1.1  
#===================================================#
import boto3
import csv
#Key & ID
aws_access_id = "*****"
aws_secret_key = "*******"
region = "cn-north-1"
#defin session
session = boto3.Session(aws_access_key_id=aws_access_id,
                        aws_secret_access_key=aws_secret_key,
                        region_name=region);
#defin resource high level in boto3
ec2 = session.resource('ec2')
#get all ec2 in AWS
instances = ec2.instances.all()
#defin splist_list fuction
def split_list(liststring):
    while(liststring == None):
        liststring = [{'Key': 'Name', 'Value': 'None'}]
    return liststring
#List EC2 and Export CSV
headers = ['EC2_Name','EC2_ID','Type','AZ_Name','Architecture',
           'Virtualization_Type','Hypervisor','Image_Id','OS','PlacementGroup',
           'State','Public_IP_Address','VPC_Id','Subnet_Name','Subnet_Id',
           'Private_IP_Address','Private_DNS_Name','Network_Interfaces_Id',
           'Root_Device_Name','Root_Device_Type','Security_Groups_Id','Launch_Time']
with open('D:\Aws_ec2_list.csv','w',newline='') as File:
    File_csv = csv.writer(File)
    File_csv.writerow(headers)
    for instance in instances:
        if (instance.platform == "windows"):
            platform = "Windows"
        else:
            platform = "Linux"
        if(instance.public_ip_address != None):
            public_ip_address = instance.public_ip_address
        else:
            public_ip_address = "---" 
        rows=[(instance.tags[0].get("Value"),
          instance.id,
          instance.instance_type,
          instance.placement.get("AvailabilityZone"),
          instance.architecture,
          instance.virtualization_type,
          instance.hypervisor,
          instance.image_id,
          platform,
          instance.placement.get("GroupName"),
          instance.state.get("Name"),
          public_ip_address,
          instance.vpc_id,
          split_list(instance.subnet.tags)[0]["Value"],
          instance.subnet_id,
          instance.private_ip_address,
          instance.private_dns_name,
          str(instance.network_interfaces)[22:-3],
          instance.root_device_name,
          instance.root_device_type,
          [key for item in instance.security_groups for key in item.values()][1],
          instance.launch_time)]
        File_csv.writerows(rows)
    

    

