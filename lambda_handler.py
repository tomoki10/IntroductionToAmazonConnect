import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    region = event['Details']['Parameters']['Region']
    instances = event['Details']['Parameters']['Instances']
    ec2 = boto3.client('ec2', region_name=region)
    try:
        if event['Details']['Parameters']['Action'] == 'start':
            ec2.start_instances(InstanceIds=[instances])
            responce = "Success"

        elif event['Details']['Parameters']['Action'] == 'stop':
            ec2.stop_instances(InstanceIds=[instances])
            responce = "Success"

        elif event['Details']['Parameters']['Action'] == 'restart':
            dic = ec2.describe_instances()
            ec2_state_responce = dic["Reservations"][0]["Instances"][0]["State"]["Name"]
            if ec2_state_responce == "running":
                out_body = ec2.reboot_instances(InstanceIds=[instances])
                responce = "Success"
            else:
                responce = "Faile"

    except ClientError as e:
        responce = "Faile"

    return {
        'Status': responce
    }
