from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
import subprocess
import asyncio
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['juliobarizon@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'end_date': datetime(2024, 1, 1), # Se você quiser agendar um fim para a execução do DAG.
}

# Definindo a DAG e configurando-a para rodar uma vez por dia.
dag = DAG(
    'immo_eliza_scraping',
    default_args=default_args,
    description='A simple DAG to scrape immo data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

clean = BashOperator(
    task_id='clean',
    bash_command='python /opt/airflow/dags/immo-eliza-scraper/clean.py',
    dag=dag,
)


scrape_task2 = BashOperator(
    task_id='scrape_task2',
    bash_command='python /opt/airflow/dags/immo-eliza-scraper/main.py',
    dag=dag,
)

train_model = BashOperator(
    task_id='train_model',
    bash_command='python /opt/airflow/plugins/model/train.py',
    dag=dag,

)

scrape_task2 >> clean >> train_model
