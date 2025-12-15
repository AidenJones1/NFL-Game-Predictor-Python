from fastapi import FastAPI
from modules.nfl_info import get_nfl_time
from modules.utils.file_utils import get_prediction_as_json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the NFL Predictor API!"}

@app.get("/predictions")
def get_prediction():
    season, week = get_nfl_time()

    return get_prediction_as_json(season, week)