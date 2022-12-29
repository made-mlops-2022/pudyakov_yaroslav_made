from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from docker.types import Mount
from omegaconf import OmegaConf

cfg = OmegaConf.load(Variable.get('CONFIG_FILE_PATH'))

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["yaapudyakov@edu.hse.ru"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

batch_size = cfg['data']['batch_size']
raw_data_path = cfg['paths']['raw_data_path']
raw_target_path = cfg['paths']['raw_target_path']
source_data_dir = cfg['paths']['source_data_dir']
target_data_dir = cfg['paths']['target_data_dir']

with DAG(
    dag_id="generate_data_batch",
    start_date=datetime.today(),
    schedule_interval="@daily",
) as dag:

    generate_data = DockerOperator(
        image="generate-data",
        command=f"--k {batch_size} --save_data_path {raw_data_path} --save_target_path {raw_target_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="generate_data",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=source_data_dir, target=target_data_dir, type='bind')]
    )
