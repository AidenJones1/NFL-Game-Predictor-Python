from modules.nfl import get_nfl_time
from modules.nfl_stats_downloader import download_data
from modules.utils.file_utils import SERVER_DATA_PATH, create_directory

import sys
from pandas import DataFrame

def main(task: str):
    if task == "--predict":
        # Get time
        current_season, current_week = get_nfl_time()

        # Get up-to-date data
        pbp, schedule = download_data(season = current_season)

        path = create_directory(directory_path = f"{SERVER_DATA_PATH}/{current_season} NFL Season")
        pbp.to_csv(path_or_buf = f"{path}/Play-By-Play Data.csv", index = False)
        schedule.to_csv(path_or_buf = f"{path}/Schedule Data.csv", index = False)

    # TODO: Create module for ELO Rating System
    # TODO: Create module for creating datasets for the model
    # TODO: Create module for machine learning model
    pass

if __name__ == "__main__":
    # Check if an argument exist
    if len(sys.argv) > 1:

        # Check if the first argument is one of two options
        task = sys.argv[1]
        if task in ["--train/test", "--predict"]:
            main(task = task)
            sys.exit()
    
    # Invalid Argument
    print("ERROR: Invalid argument!")