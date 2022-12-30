from pathlib import Path
from datetime import datetime
import numpy as np
import click
from sklearn.datasets import load_digits

@click.command("generate_data")
@click.option("--k")
@click.option("--save_data_path")
@click.option("--save_target_path")
@click.option("--date")
def generate_data(k: int = 200,
                  save_data_path: str = None,
                  save_target_path: str = None,
                  date: str = datetime.today().strftime('%Y-%m-%d')) -> None:
    
    k = int(k)
    X, y = load_digits(return_X_y=True)
    idx = np.random.randint(X.shape[0], size=k)

    if save_data_path is not None:
        save_data_path = save_data_path.format(date)
        Path(save_data_path[:save_data_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
        np.savetxt(save_data_path, X[idx].astype(int), fmt="%i", delimiter=",")
        
    if save_target_path is not None:
        save_target_path = save_target_path.format(date)
        Path(save_target_path[:save_target_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
        np.savetxt(save_target_path, y[idx].astype(int), fmt="%i", delimiter=",")

if __name__ == '__main__':
    generate_data()
