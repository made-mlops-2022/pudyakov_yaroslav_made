from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["yaapudyakov@edu.hse.ru"],
    "retries": 2,
    "retry_delay": timedelta(hours = 1),
}

splitted_data_path = "data/datasets/{}/{}/data.csv"
models_path = "data/models/{}/model.pkl"
predictions_path = "data/predictions/{}/predictions.csv"

with DAG(
    dag_id = "predict_model_daily",
    start_date = datetime(2022, 12, 4),
    schedule_interval = "@daily",
) as dag:
    
    predict_model = DockerOperator(
        image="predict-model",
        command=f"--model_path {Variable.get('MODEL_PATH')} --dataset_data_path {splitted_data_path} --predictions_path {predictions_path} " + "--date {{ ds }}",
        network_mode="bridge",
        task_id="predict_model",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/Users/ypudyakov/prog/made/mlops/MADE_mlops/hw3/data", target="/data", type='bind')]
    )
