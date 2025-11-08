import json

SERVER_DATA_CONFIGS = "./src/nfl_predictor_package/server/data_configs"

def read_json(file_path: str):
    with open(file = file_path) as file:
        configs = json.load(file)

    return configs