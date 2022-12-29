from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator
from omegaconf import OmegaConf

cfg = OmegaConf.load(Variable.get('CONFIG_FILE_PATH'))

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["yaapudyakov@edu.hse.ru"],
    "retries": 2,
    "retry_delay": timedelta(hours=1),
}

raw_data_path = cfg['paths']['raw_data_path']
processed_data_path = cfg['paths']['processed_data_path']
models_path = Variable.get('MODEL_PATH')
predictions_path = cfg['paths']['predictions_path']
source_data_dir = cfg['paths']['source_data_dir']
target_data_dir = cfg['paths']['target_data_dir']


with DAG(
    dag_id="predict_model_daily",
    start_date=datetime.today(),
    schedule_interval="@daily",
) as dag:

    process_data = DockerOperator(
        image="process-data",
        command=f"--data_path {raw_data_path} --processed_data_path {processed_data_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="process_data",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=source_data_dir, target=target_data_dir, type='bind')]
    )

    predict_model = DockerOperator(
        image="predict-model",
        command=f"--model_path {models_path} --dataset_data_path {processed_data_path} --predictions_path {predictions_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="predict_model",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=source_data_dir, target=target_data_dir, type='bind')]
    )

    process_data >> predict_model
