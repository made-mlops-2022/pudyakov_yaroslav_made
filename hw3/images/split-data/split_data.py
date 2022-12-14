from pathlib import Path
import numpy as np
import click
from sklearn.model_selection import train_test_split

@click.command("split_data")
@click.option("--data_path")
@click.option("--target_path")
@click.option("--splitted_data_path")
@click.option("--splitted_target_path")
@click.option("--date")
@click.option("--test_size")
@click.option("--random_state")
def split_data(data_path: str,
               target_path: str,
               splitted_data_path: str,
               splitted_target_path: str,
               date: str,
               test_size: float = 0.2,
               random_state: int = 0) -> None:
    
    test_size = float(test_size)
    random_state = int(random_state)
    
    data_path = data_path.format(date)
    target_path = target_path.format(date)

    try:
        data = np.genfromtxt(data_path, delimiter=',').astype(int)
        target = np.genfromtxt(target_path, delimiter=',').astype(int)
    except:
        raise FileExistsError("Can't load data and target files")


    X_train, X_val, y_train, y_val = train_test_split(data,
                                                      target,
                                                      test_size = test_size,
                                                      random_state = random_state)
    

    x_train_path = splitted_data_path.format(date, 'train')
    x_val_path = splitted_data_path.format(date, 'val')
    y_train_path = splitted_target_path.format(date, 'train')
    y_val_path = splitted_target_path.format(date, 'val')

    Path(x_train_path[:x_train_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
    np.savetxt(x_train_path, X_train, delimiter=",")

    Path(x_val_path[:x_val_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
    np.savetxt(x_val_path, X_val, delimiter=",")

    Path(y_train_path[:y_train_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
    np.savetxt(y_train_path, y_train, fmt="%i", delimiter=",")

    Path(y_val_path[:y_val_path.rfind('/')]).mkdir(parents=True, exist_ok=True)
    np.savetxt(y_val_path, y_val, fmt="%i", delimiter=",")

if __name__ == '__main__':
    split_data()
