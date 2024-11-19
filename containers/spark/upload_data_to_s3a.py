"""
Upload data to S3A
"""
import os
import boto3                                # type: ignore # pylint: disable=import-error
from botocore.exceptions import ClientError # type: ignore # pylint: disable=import-error
from botocore.client import Config          # type: ignore # pylint: disable=import-error

def create_s3_client(access_key, secret_key, endpoint, region):
    """
    Create a boto3 client configured for Minio or any S3-compatible service.

    :param access_key: S3 access key
    :param secret_key: S3 secret key
    :param endpoint: Endpoint URL for the S3 service
    :param region: Region to use, defaults to us-east-1
    :return: Configured S3 client
    """
    return boto3.client(
        's3',
        region_name=region,
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version='s3v4')
    )

def upload_data_to_s3(s3_client, data_directory, bucket_name):
    """
    Upload a data directory to S3A (Minio)

    :param s3_client: S3 client object
    :param data_directory: data directory (absolute)
    :param bucket_name: bucket to upload
    :return:
    """
    try:
        for root, dirs, files in os.walk(data_directory):
            for file in files:
                # Construct the full file path
                local_file_path = os.path.join(root, file)
                # Construct the S3 object key (relative path inside the bucket)
                s3_key = os.path.relpath(local_file_path, data_directory)
                # Upload the file
                s3_client.upload_file(local_file_path, bucket_name, s3_key)
                print(f"uploaded {local_file_path} to {bucket_name}/{s3_key}")
    except ClientError as error:
        print(f"Fail to upload files: {error}")


# Credentials and Connection Info
access_key = 'minio'
secret_key = 'minio123'
endpoint = 'http://minio:9000'
region = 'us-east-1'

# Client upload directory to s3a
try:
    s3_client = create_s3_client(access_key, secret_key, endpoint, region)
    DATA_DIRECTORY = '/opt/spark/work-dir/data/'
    BUCKET_NAME = 'data'
    upload_data_to_s3(s3_client, DATA_DIRECTORY, BUCKET_NAME)
except ClientError:
    print("Full catch, check script at upload_data_to_s3a.py")
