import pandas as pd
import io
from datetime import datetime

def transform_data(**kwargs):
    # Pull the extracted data from XCom
    print('/////////////////// \t Pulling Data from xcomm \t///////////////////////////\n')
    raw_data = kwargs['ti'].xcom_pull(task_ids='extract_task', key='raw_data')
    print('/////////////////// \t Reading Data\t///////////////////////////\n')
    df = pd.read_csv(io.BytesIO(raw_data))
    load_timestamp = datetime.now().strftime('%Y-%m-%d')
    df['load_timestamp'] = load_timestamp # Sample transformation
    transformed_data = df.to_csv(index=False)

    print('/////////////////// \t Pushing data to xcomm \t///////////////////////////\n')
    # Push the transformed data to XCom for downstream tasks
    kwargs['ti'].xcom_push(key='transformed_data', value=transformed_data)

    print('/////////////////// \t Transform completed \t///////////////////////////\n')  

