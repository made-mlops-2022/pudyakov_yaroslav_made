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
    "retries": 2,
    "retry_delay": timedelta(hours=1),
}

raw_data_path = cfg['paths']['raw_data_path']
raw_target_path = cfg['paths']['raw_target_path']
processed_data_path = cfg['paths']['processed_data_path']
processed_target_path = cfg['paths']['processed_target_path']
splitted_data_path = cfg['paths']['splitted_data_path']
splitted_target_path = cfg['paths']['splitted_target_path']
models_path = Variable.get('MODEL_PATH')
metrics_path = cfg['paths']['metrics_path']
test_size = cfg['data']['test_size']
random_state_splitting = cfg['data']['random_state_splitting']
source_data_dir = cfg['paths']['source_data_dir']
target_data_dir = cfg['paths']['target_data_dir']

with DAG(
    dag_id="train_validate_model_pipeline",
    start_date=datetime.today(),
    schedule_interval="@weekly",
) as dag:

    process_data = DockerOperator(
        image="process-data",
        command=f"--data_path {raw_data_path} --target_path {raw_target_path} --processed_data_path {processed_data_path} --processed_target_path {processed_target_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="process_data",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=source_data_dir, target=target_data_dir, type='bind')]
    )

    split_data = DockerOperator(
        image="split-data",
        command=f"--data_path {processed_data_path} --target_path {processed_target_path} --splitted_data_path {splitted_data_path} --splitted_target_path {splitted_target_path} " +
                "--date {{ ds }}" + f" --test_size {test_size} --random_state {random_state_splitting}",
        network_mode="bridge",
        task_id="split_data",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=source_data_dir, target=target_data_dir, type='bind')]
    )

    train_model = DockerOperator(
        image="train-model",
        command=f"--dataset_data_path {splitted_data_path} --dataset_target_path {splitted_target_path} --model_path {models_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="train_model",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=source_data_dir, target=target_data_dir, type='bind')]
    )

    validate_model = DockerOperator(
        image="validate-model",
        command=f"--model_path {models_path} --dataset_data_path {splitted_data_path} --dataset_target_path {splitted_target_path} --metrics_path {metrics_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="validate_model",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=source_data_dir, target=target_data_dir, type='bind')]
    )

    process_data >> split_data >> train_model >> validate_model
