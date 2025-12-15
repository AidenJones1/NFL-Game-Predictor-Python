import json
from os import makedirs, path
from pandas import DataFrame, read_csv
import pickle

SERVER_DATA_CONFIGS_PATH = "./src/nfl_predictor_package/server/data_configs"
SERVER_DATA_PATH = "./src/nfl_predictor_package/server/data"
MODEL_PATH = "./src/nfl_predictor_package/server/models"

def read_json(file_path: str):
    """Retrieve JSON properties from the specified JSON file.

    Args:
        file_path (str): The file to read."""
    with open(file = file_path) as file:
        configs = json.load(file)

    return configs

def create_directory(directory_path: str):
    if not path.exists(directory_path):
        makedirs(directory_path)

    return directory_path

def get_dataframe(filepath: str) -> DataFrame:
    return read_csv(filepath_or_buffer = filepath, low_memory = False)

def save_model(model, filename: str):
    with open(f"{MODEL_PATH}/{filename}", 'wb') as f:
        pickle.dump(model, f)

def load_model(filename: str):
    with open(f"{MODEL_PATH}/{filename}", 'rb') as f:
        loaded_model = pickle.load(f)
        return loaded_model
    
    return None

def get_prediction_as_json(season: int, week: int):
    try:
        path = f"{SERVER_DATA_PATH}/{season} NFL Season/Predictions/Week {week}.csv"
        res = read_csv(filepath_or_buffer = path, low_memory = False)
        return res.to_json(orient = "records")

    except Exception as e:
        print(f"Error getting prediction file path: {e}")
        return None