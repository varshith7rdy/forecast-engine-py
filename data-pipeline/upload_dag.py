import pendulum
from airflow.models import DAG
from airflow.providers.standard.operators.bash import BashOperator
import os
from dotenv import load_dotenv

load_dotenv()

path = os.getenv("PATH")

with DAG(
    dag_id="logs_db_upload",
    start_date=pendulum.datetime(2025, 10, 16, tz="UTC"),
    schedule=None,
    catchup=False,
) as dag:
    
    run_batch_file = BashOperator(
        task_id="Logs batch upload",
        bash_command=f"python {path}"
    )

    run_batch_file
