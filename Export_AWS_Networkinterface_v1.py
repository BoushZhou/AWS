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
aws_access_id = "***"
aws_secret_key = "****"
region = "cn-north-1"
#defin session
session = boto3.Session(aws_access_key_id=aws_access_id,
                        aws_secret_access_key=aws_secret_key,
                        region_name=region);
#define resource high level in boto3
ec2 = session.resource('ec2')
#defin splist_list fuction
def split_list(liststring):
    while(liststring == None):
        liststring = [{'Key': 'Name', 'Value': 'None'}]
    return liststring
#List EC2 and Export CSV
headers = ['VPC_Name','VPC_ID','VPC_cidr','Subnet_Name','Subnet_Id','Subnet_AZ',
           'Subnet_State','Subnet_cidr','Subnet_available.ip_count','Network_interface.id','Network_interface_Type',
           'Network_interface_State','Private_IP_Address','Private_IP_Address','Network_interface_Mac']
#list the info vpc&subnet&network_interface
with open('C:\Aws_Network_interface.csv','w',newline='') as File:
    File_csv = csv.writer(File)
    File_csv.writerow(headers)
    for vpc in ec2.vpcs.all():
        print(split_list(vpc.tags)[0]['Value'],vpc.id,vpc.cidr_block)
        for subnet in vpc.subnets.all():
            print(split_list(subnet.tags)[0]['Value'],subnet.id,subnet.availability_zone,
              subnet.state,subnet.cidr_block,subnet.available_ip_address_count)
            for network_interface in subnet.network_interfaces.all():
                print(network_interface.id,network_interface.description,network_interface.status,
                  network_interface.private_ip_address,network_interface.private_dns_name,
                  network_interface.mac_address)
                rows=[split_list(vpc.tags)[0]['Value'],vpc.id,vpc.cidr_block,split_list(subnet.tags)[0]['Value'],
                      subnet.id,subnet.availability_zone,subnet.state,subnet.cidr_block,
                      subnet.available_ip_address_count,network_interface.id,network_interface.description,network_interface.status,
                      network_interface.private_ip_address,network_interface.private_dns_name,network_interface.mac_address]
                File_csv.writerow(rows)
