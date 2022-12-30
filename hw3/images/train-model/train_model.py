from pathlib import Path
import numpy as np
import click
from sklearn.linear_model import LogisticRegression
import pickle

@click.command("train_model")
@click.option("--dataset_data_path")
@click.option("--dataset_target_path")
@click.option("--model_path")
@click.option("--date")
def train_model(dataset_data_path: str, 
                dataset_target_path: str,
                model_path: str, 
                date: str) -> None:
    
    dataset_data_path = dataset_data_path.format(date, 'train')
    dataset_target_path = dataset_target_path.format(date, 'train')
    model_path = model_path.format(date)

    try:
        data = np.genfromtxt(dataset_data_path, delimiter=',')
        target = np.genfromtxt(dataset_target_path, delimiter=',').astype(int)
    except:
        raise FileExistsError("Can't load data and target files")

    model = LogisticRegression()
    model.fit(data, target)

    Path(model_path[:model_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
    with open(model_path, 'wb') as model_file:
        pickle.dump(model, model_file)


if __name__ == '__main__':
    train_model()
