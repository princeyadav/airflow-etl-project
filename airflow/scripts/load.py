from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime

def load_to_s3(**kwargs):
    print('/////////////////// \t Loading started \t///////////////////////////\n')
    bucket_name = kwargs['bucket_name']
    table_name = kwargs['table_name']
    # Pull the transformed data from XCom
    print('/////////////////// \t Pulling data from xcomm \t///////////////////////////\n')
    transformed_data = kwargs['ti'].xcom_pull(task_ids='transform_task', key='transformed_data')
    load_timestamp = datetime.now().strftime('%Y-%m-%d')
    s3_key = f"consumer/{table_name}/{load_timestamp}/data.csv"

    print('/////////////////// \t Making connection to s3 \t///////////////////////////\n')
    s3_hook = S3Hook(aws_conn_id='aws_default')
    s3_hook.load_string(transformed_data, s3_key, bucket_name, replace=True)
    print('/////////////////// \t Data Saved to S3 Bucket\t///////////////////////////\n')
