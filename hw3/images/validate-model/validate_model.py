from pathlib import Path
import numpy as np
import click
import pickle
import json
from sklearn.metrics import accuracy_score, f1_score

@click.command("validate_model")
@click.option("--model_path")
@click.option("--dataset_data_path")
@click.option("--dataset_target_path")
@click.option("--metrics_path")
@click.option("--date")
def validate_model(model_path: str,
                   dataset_data_path: str,
                   dataset_target_path: str,
                   metrics_path: str,
                   date: str) -> None:
    
    model_path = model_path.format(date)
    dataset_data_path = dataset_data_path.format(date, 'val')
    dataset_target_path = dataset_target_path.format(date, 'val')
    metrics_path = metrics_path.format(date)

    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
        
    try:
        data = np.genfromtxt(dataset_data_path, delimiter=',')
        target = np.genfromtxt(dataset_target_path, delimiter=',').astype(int)
    except:
        raise FileExistsError("Can't load data and target files.")

    prediction = model.predict(data)

    acc_val_score = accuracy_score(target, prediction)
    f1_macro_val_score = f1_score(target, prediction, average = 'macro')

    val_metrics = {
        'accuracy' : acc_val_score,
        'f1_macro' : f1_macro_val_score,
    }

    Path(metrics_path[:metrics_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
    with open(metrics_path, 'w') as metrics_file:
        json.dump(val_metrics, metrics_file)

if __name__ == '__main__':
    validate_model()
