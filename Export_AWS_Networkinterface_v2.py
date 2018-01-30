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
#List EC2 and Export CSV
headers = ['Network_interface.id','Network_interface_Type','Network_interface_State','Private_IP_Address','Private_IP_Address','Network_interface_Mac',
           'Subnet_Name','Subnet_Id','Subnet_AZ','Subnet_State','Subnet_cidr','Subnet_available.ip_count',
           'VPC_Name','VPC_ID','VPC_cidr']
#defin splist_list fuction
def split_list(liststring):
    while(liststring == None):
        liststring = [{'Key': 'Name', 'Value': 'None'}]
    return liststring
#List EC2 and Export CSV
#list the info vpc&subnet&network_interface
with open('D:\Aws_Network_interface.csv','w',newline='') as File:
    File_csv = csv.writer(File)
    File_csv.writerow(headers)
    for network_interface in ec2.network_interfaces.all():
        print(network_interface.id,network_interface.description,network_interface.status,
              network_interface.private_ip_address,network_interface.private_dns_name,
              network_interface.mac_address,
              split_list(network_interface.subnet.tags)[0]['Value'],network_interface.subnet.id,network_interface.subnet.availability_zone,
              network_interface.subnet.state,network_interface.subnet.cidr_block,network_interface.subnet.available_ip_address_count,
              split_list(network_interface.vpc.tags)[0]['Value'],network_interface.vpc.id,network_interface.vpc.cidr_block)
        rows=[network_interface.id,network_interface.description,network_interface.status,
              network_interface.private_ip_address,network_interface.private_dns_name,network_interface.mac_address,
              split_list(network_interface.subnet.tags)[0]['Value'],network_interface.subnet.id,network_interface.subnet.availability_zone,
              network_interface.subnet.state,network_interface.subnet.cidr_block,network_interface.subnet.available_ip_address_count,
              split_list(network_interface.vpc.tags)[0]['Value'],network_interface.vpc.id,network_interface.vpc.cidr_block]
        File_csv.writerow(rows)
    
        
    
                




