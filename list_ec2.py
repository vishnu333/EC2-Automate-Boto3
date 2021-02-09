import boto3
import json
import datetime
# list regions
client = boto3.client('ec2')
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

print("Listing EC2 instances for each region....\n")

region_vise = []


def datetime_handler(x):
    return x.isoformat()

for Region in regions:
    print()
    print(Region)
    print('---------')
    client = boto3.client('ec2', region_name=Region)
    response = client.describe_instances()
    i = 0
    for reservation in response["Reservations"]:

        for instance in reservation["Instances"]:
            i+=1
            instance_vise = {}
            instance_vise['InstanceId'] = instance['InstanceId']
            instance_vise['InstanceType'] = instance['InstanceType']
            instance_vise['ImageId'] = instance['ImageId']
            instance_vise['Region'] = Region
            instance_vise['AvailabilityZone'] = instance['Placement']['AvailabilityZone']
            instance_vise['State'] = instance['State']['Name']
            instance_vise['LaunchTime'] = datetime_handler(instance['LaunchTime'])
            

            try:
                instance_vise['PublicIpAddress'] = instance['PublicIpAddress']
            except Exception:
                pass
            try:
                instance_vise['PrivateIpAddress'] = instance['PrivateIpAddress']
            except Exception:
                pass
            for tag in instance['Tags']:
                instance_vise[tag['Key']] = tag['Value']
            region_vise.append(instance_vise)

    print("number of instances in region {} : {}".format(Region,i))

with open("EC2_List.json", "w") as outfile:
    json.dump(region_vise, outfile)
