from pathlib import Path
import numpy as np
import click
import pickle

@click.command("predict_model")
@click.option("--model_path")
@click.option("--dataset_data_path")
@click.option("--predictions_path")
@click.option("--date")
def predict_model(model_path: str,
                  dataset_data_path: str,
                  predictions_path: str,
                  date: str) -> None:
    
    dataset_data_path = dataset_data_path.format(date, 'val')
    predictions_path = predictions_path.format(date)

    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
        
    try:
        data = np.genfromtxt(dataset_data_path, delimiter=',')
    except:
        raise FileExistsError("Can't load data and target files.")

    predictions = model.predict(data)

    Path(predictions_path[:predictions_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
    np.savetxt(predictions_path, predictions, fmt="%i", delimiter=",")


if __name__ == '__main__':
    predict_model()
