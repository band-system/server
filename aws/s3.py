import boto3
from dotenv import load_dotenv
import os

load_dotenv('.env')

region = os.getenv('S3_REGION')
bucket_name = os.getenv('S3_BUCKET_NAME')
role_arn = os.getenv('S3_ROLE_ARN')
role_session_name = os.getenv('S3_ROLE_SESSION_NAME')
profile_name = os.getenv('PROFILE_NAME')

sts_session = boto3.Session(profile_name=profile_name)

sts = sts_session.client('sts')

response = sts.assume_role(
    RoleArn= role_arn,
    RoleSessionName=role_session_name
)


s3_session = boto3.Session(
    aws_access_key_id=response['Credentials']['AccessKeyId'],
    aws_secret_access_key=response['Credentials']['SecretAccessKey'],
    aws_session_token=response['Credentials']['SessionToken']
)

s3 = s3_session.client(
    's3',
    region_name=region,
)

method_parameters = {
    "Bucket": bucket_name
}

def generateAccessURL(client_method, object_key=None, expiration=600):
    if object_key != None :
        method_parameters["Key"] = object_key

    accessURL = s3.generate_presigned_url(
        ClientMethod = client_method,
        Params = method_parameters,
        ExpiresIn=expiration
    )['url']
    return accessURL