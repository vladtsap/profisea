import boto3

client = boto3.client(
	'ec2',
	aws_access_key_id='aws_access_key_id',
	aws_secret_access_key='aws_secret_access_key',
	region_name='eu-central-1'
)

response = client.describe_vpcs()
print(response)
