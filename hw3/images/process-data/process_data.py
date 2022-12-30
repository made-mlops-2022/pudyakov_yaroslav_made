from pathlib import Path
import numpy as np
import click
from sklearn.preprocessing import StandardScaler

@click.command("process_data")
@click.option("--data_path")
@click.option("--target_path")
@click.option("--processed_data_path")
@click.option("--processed_target_path")
@click.option("--date")
def process_data(data_path: str,
                 target_path: str,
                 processed_data_path: str,
                 processed_target_path: str,
                 date: str) -> None:

    data_path = data_path.format(date) if (data_path is not None) else None
    target_path = target_path.format(date) if (target_path is not None) else None
    processed_data_path = processed_data_path.format(date) if (processed_data_path is not None) else None
    processed_target_path = processed_target_path.format(date) if (processed_target_path is not None) else None

    if (data_path is None) and (target_path is None):
        raise ValueError("Data and target pathes can't be None both")

    try:
        if data_path is not None:
            data = np.genfromtxt(data_path, delimiter=',').astype(int)
        if target_path is not None:
            target = np.genfromtxt(target_path, delimiter=',').astype(int)
    except:
        raise FileExistsError("Can't load data and target files")


    scaler = StandardScaler()
    data_processed = scaler.fit_transform(data)
    
    if target_path is not None:
        target_processed = target

    if (data_path is not None) and (processed_data_path is not None):
        Path(processed_data_path[:processed_data_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
        np.savetxt(processed_data_path, data_processed, delimiter=",")

    if (target_path is not None) and (processed_target_path is not None):
        Path(processed_target_path[:processed_target_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
        np.savetxt(processed_target_path, target_processed.astype(int), fmt="%i", delimiter=",")

if __name__ == '__main__':
    process_data()
