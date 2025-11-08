import json
from os import makedirs, path
from pandas import DataFrame, read_csv

SERVER_DATA_CONFIGS_PATH = "./src/nfl_predictor_package/server/data_configs"
SERVER_DATA_PATH = "./src/nfl_predictor_package/server/data"

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