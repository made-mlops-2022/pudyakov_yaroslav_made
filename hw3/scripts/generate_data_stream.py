import datetime
from sklearn.datasets import load_digits
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

batch_size = 200
raw_data_path = "data/raw/{}/data.csv"
raw_target_path = "data/raw/{}/target.csv"

def _generate_data(k: int = 200,
                   save_data_path: str = None,
                   save_target_path: str = None,
                   date: str = datetime.today().strftime('%Y-%m-%d')) -> None:
    
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

if __name__ == "__main__":    
    num_days = 10
    start_date = datetime.today() - timedelta(days = num_days)

    for i in range(num_days):
        cur_date = datetime.today() + timedelta(days = i)

        _generate_data(
            batch_size,
            raw_data_path,
            raw_target_path,
            cur_date.strftime('%Y-%m-%d')
        )
