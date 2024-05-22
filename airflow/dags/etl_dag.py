import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime

sys.path.insert(1, '/home/prince/airflow-workspace/airflow/')

# Import the necessary functions
from scripts.extract import extract_from_s3
from scripts.transform import transform_data
from scripts.load import load_to_s3


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 21),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'email': ['prince.yadav@tothenew.com']
}

with DAG('etl_dag',
         default_args=default_args,
         description='A simple ETL DAG to extract, transform, and load data using S3',
         schedule_interval='@daily',
         catchup=False) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_from_s3,
        op_kwargs={
            'bucket_name': 'airflow-demo-bucket1',
            'key': 'source/netflix_titles.csv'
        },
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_to_s3,
        op_kwargs={
            'bucket_name': 'airflow-demo-bucket1',
            'table_name': 'netflix'
        },
        provide_context=True
    )

    email_notify = EmailOperator(
        task_id='email_notify',
        to='prince.yadav@tothenew.com',
        subject='ETL DAG Completed',
        html_content='The ETL DAG has been completed successfully.'
    )

    extract_task >> transform_task >> load_task >> email_notify
