from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import json


def extract_from_s3(**kwargs):
    print('/////////////////// \t Extracting Data from S3 Bucket  \t///////////////////////////\n')
    bucket_name = kwargs['bucket_name']
    key = kwargs['key']
    s3_hook = S3Hook(aws_conn_id='aws_default')
    s3_object = s3_hook.get_key(key, bucket_name)
    print('/////////////////// \t Reading data \t///////////////////////////\n')
    data = s3_object.get()['Body'].read()

    # Push the extracted data to XCom for downstream tasks
    print('/////////////////// \t Pushing data to xcomm \t///////////////////////////\n')
    kwargs['ti'].xcom_push(key='raw_data', value=data)

    print('/////////////////// \t Extract Success \t///////////////////////////\n')    
    
