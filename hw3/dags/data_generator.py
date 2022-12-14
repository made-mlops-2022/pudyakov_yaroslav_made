from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(2),
    "email": ["yaapudyakov@edu.hse.ru"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

batch_size = 200
raw_data_path = "data/raw/{}/data.csv"
raw_target_path = "data/raw/{}/target.csv"

with DAG(
    dag_id = "generate_data_batch",
    start_date = datetime(2022, 12, 4),
    schedule_interval = "@daily",
) as dag:

    generate_data = DockerOperator(
        image="generate-data",
        command=f"--k {batch_size} --save_data_path {raw_data_path} --save_target_path {raw_target_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="generate_data",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/Users/ypudyakov/prog/made/mlops/MADE_mlops/hw3/data", target="/data", type='bind')]
    )
