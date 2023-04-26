from prefect import task
from dotenv import dotenv_values
import boto3
from prefect.blocks.system import Secret

s3_access_key = Secret.load("awsaccesskey")
s3_secret_key = Secret.load("awsscrectkey")
s3_region = Secret.load("awsregion")


@task(name='Get s3 client')
def get_client():
    access_key = s3_access_key.get()
    secret_key = s3_secret_key.get()
    region_key = s3_region.get()

    client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_key
    )
    return client


@task(name='Add object to s3 bucket')
def add_obj_to_s3(bucket_name, key, body, s3_client):
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=body)


def read_s3_bucket_file(bucket_name, key, s3_client):
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    # print(response['Body'].read().decode('utf-8'))
    return response
