from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["yaapudyakov@edu.hse.ru"],
    "retries": 2,
    "retry_delay": timedelta(hours = 1),
}

raw_data_path = "data/raw/{}/data.csv"
raw_target_path = "data/raw/{}/target.csv"

processed_data_path = "data/processed/{}/data.csv"
processed_target_path = "data/processed/{}/target.csv"

splitted_data_path = "data/datasets/{}/{}/data.csv"
splitted_target_path = "data/datasets/{}/{}/target.csv"

models_path = "data/models/{}/model.pkl"
metrics_path = "data/metrics/{}/metrics.json"

test_size = 0.2
random_state_splitting = 0


with DAG(
    dag_id = "train_validate_model_pipeline",
    start_date = datetime(2022, 12, 4),
    schedule_interval = "@weekly",
) as dag:

    process_data = DockerOperator(
        image="process-data",
        command=f"--data_path {raw_data_path} --target_path {raw_target_path} --processed_data_path {processed_data_path} --processed_target_path {processed_target_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="process_data",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/Users/ypudyakov/prog/made/mlops/MADE_mlops/hw3/data", target="/data", type='bind')]
    )

    split_data = DockerOperator(
        image="split-data",
        command=f"--data_path {processed_data_path} --target_path {processed_target_path} --splitted_data_path {splitted_data_path} --splitted_target_path {splitted_target_path} " + \
                 "--date {{ ds }}" + f" --test_size {test_size} --random_state {random_state_splitting}",
        network_mode="bridge",
        task_id="split_data",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/Users/ypudyakov/prog/made/mlops/MADE_mlops/hw3/data", target="/data", type='bind')]
    )

    train_model = DockerOperator(
        image="train-model",
        command=f"--dataset_data_path {splitted_data_path} --dataset_target_path {splitted_target_path} --model_path {models_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="train_model",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/Users/ypudyakov/prog/made/mlops/MADE_mlops/hw3/data", target="/data", type='bind')]
    )

    validate_model = DockerOperator(
        image="validate-model",
        command=f"--model_path {models_path} --dataset_data_path {splitted_data_path} --dataset_target_path {splitted_target_path} --metrics_path {metrics_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="validate_model",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/Users/ypudyakov/prog/made/mlops/MADE_mlops/hw3/data", target="/data", type='bind')]
    )

    process_data >> split_data >> train_model >> validate_model
