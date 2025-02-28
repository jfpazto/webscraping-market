import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Añadir al path la carpeta makro para poder importar scraper y parser
sys.path.append('/home/ubuntu/airflow/dags/makro')

# Importar las funciones del scraper
from scraper import run_scraper

# Argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definimos el DAG
with DAG(
    dag_id='dag_scraper_makro',
    default_args=default_args,
    description='DAG que ejecuta el scraper de Makro y procesa los datos',
    schedule_interval='@daily',
    start_date=datetime(2025, 2, 28),
    catchup=False,
) as dag:

    run_scraper_task = PythonOperator(
        task_id='run_scraper_task',
        python_callable=run_scraper
    )
