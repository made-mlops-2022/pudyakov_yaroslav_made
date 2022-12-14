from typing import List, Union
from pydantic import conlist, BaseModel
import os

NUM_FEATURES = os.getenv("NUM_FEATURES")

class PredictionInput(BaseModel):
    data: List[conlist(item_type = Union[float, str, None], min_items=NUM_FEATURES, max_items=NUM_FEATURES)]
    data_types: conlist(item_type = str, min_items=NUM_FEATURES, max_items=NUM_FEATURES)
    features: conlist(item_type = str, min_items=NUM_FEATURES, max_items=NUM_FEATURES)

class PredictionOutput(BaseModel):
    id: int
    label: str
