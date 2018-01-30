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
import time
#Key & ID
aws_access_id = "***"
aws_secret_key = "****"
region = "cn-north-1"
#defin session
session = boto3.Session(aws_access_key_id=aws_access_id,
                        aws_secret_access_key=aws_secret_key,
                        region_name=region);
#define resource high level in boto3
iam = session.resource('iam')
client = session.client('iam')
#list the info Roles
headers = ['Role_Name','Role_ID','Role_arn']
with open('D:\Aws_roles.csv','w',newline='') as File:
    File_csv = csv.writer(File)
    File_csv.writerow(headers)
    for role in iam.roles.all():
        print(role.name,role.role_id,role.arn)
        rows=[role.name,role.role_id,role.arn]
        File_csv.writerow(rows)
#list the info Policies
headers_p = ['Role_Name','Role_ID','Role_arn','Policy_Name','Role_Document']
with open('D:\Aws_policies.csv','w',newline='') as File:
    File_csv = csv.writer(File)
    File_csv.writerow(headers_p)
    for role in iam.roles.all():
        for policy in role.policies.all():
            print(policy.policy_name,policy.policy_document)
            rows=[role.name,role.role_id,role.arn,policy.policy_name,policy.policy_document]
            File_csv.writerow(rows)
#list the info Credential report
response = client.generate_credential_report()
time.sleep(3)
response = client.get_credential_report()
credential_report_csv = response['Content']
headers_r =[]
with open('D:\Aws_credential_report.csv','w',newline='') as File:
    File_csv = csv.writer(File)
    File_csv.writerow(headers_r)
    for userinfo in credential_report_csv.splitlines():
        print(userinfo.decode('utf-8').strip(',').split(','))
        rows = userinfo.decode('utf-8').strip(',').split(',')
        File_csv.writerow(rows)
