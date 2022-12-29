from fastapi import FastAPI
import uvicorn
import logging 
import sys
import os

from typing import Optional
from typing import List

from utils.model_utils import load_catboost_clf, make_prediction
from catboost import CatBoostClassifier

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

from data_params.prediction import PredictionInput, PredictionOutput

app = FastAPI()
model: Optional[CatBoostClassifier] = None

@app.on_event("startup")
def load_model():
    global model
    try:
        model_path = os.getenv("PATH_TO_MODEL")
        model = load_catboost_clf(model_path)
        logger.info(f"Model was sucessfully loaded from {model_path}.")
    except:
        logger.info(f"Model was not loaded from {model_path}")
        raise RuntimeError("Can not load model by this path")

@app.get("/")
def root() -> str:
    return "This is the root page."

@app.get("/health")
def health() -> int:
    logger.info(f"Health request run")
    if model is None:
        raise RuntimeError("Model was not loaded")
    return 200

@app.post("/predict/")
def make_predict(payload: PredictionInput, response_model = List[PredictionOutput]):
    logger.info(f"Predict request run")
    predictions_output = make_prediction(model, payload)
    return predictions_output

if __name__ == "__main__":
    host_ip = os.getenv("IP")
    port = os.getenv("PORT")
    logger.info(f"App is running on {host_ip}:{port}")
    uvicorn.run("main:app", host = host_ip, port = port)
