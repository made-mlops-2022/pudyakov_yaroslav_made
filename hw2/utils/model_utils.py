from catboost import CatBoostClassifier
import pandas as pd
import numpy as np
from typing import List

from data_params.prediction import PredictionInput, PredictionOutput

def load_catboost_clf(model_path: str) -> CatBoostClassifier:
    clf = CatBoostClassifier()
    clf.load_model(model_path)
    return clf

def make_prediction(model: CatBoostClassifier, input_data: PredictionInput) -> List[PredictionOutput]:
    data = pd.DataFrame(input_data.data, columns = input_data.features)
    data = data.astype(dtype=dict(zip(input_data.features, input_data.data_types)))
    prediction = model.predict(data)
    return [PredictionOutput(id=id_, label=label_) for id_, label_ in zip(np.arange(len(prediction)), prediction)]
