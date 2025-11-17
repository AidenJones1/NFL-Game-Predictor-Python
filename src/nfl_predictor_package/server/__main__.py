from modules.nfl import get_nfl_time
from modules.nfl_stats_downloader import download_data
from modules.utils.file_utils import SERVER_DATA_PATH, create_directory, save_model
from modules.model import NFLPredictionModel
from modules import elo

import sys
from pandas import DataFrame

def get_data(season: int, week: int) -> tuple[DataFrame, DataFrame, DataFrame]:
    # Get data from season
    pbp, schedule = download_data(season = season)

    path = create_directory(directory_path = f"{SERVER_DATA_PATH}/{season} NFL Season")
    pbp.to_csv(path_or_buf = f"{path}/Play-By-Play Data.csv", index = False)
    schedule.to_csv(path_or_buf = f"{path}/Schedule Data.csv", index = False)

    # Construct ELO Ratings
    elo_ratings = elo.get_elo_ratings_df(schedule = schedule, current_week = week)
    elo_ratings.to_csv(path_or_buf = f"{path}/ELO Ratings Data.csv", index = False)

    return pbp, schedule, elo_ratings

def main(task: str, options: list[str]):
    if task == "--train/test":
        season = 2024
        week = 23

        # Get data
        pbp, schedule, elo_ratings = get_data(season = season, week = week)

        model = NFLPredictionModel(schedule, pbp, elo_ratings)
        model.create()

        # Print Testing Results
        if "--print" in options:
            model.print_test()

        # Save
        if "--save" in options:
            model.save("model.pkl")

    elif task == "--predict":
        # Current NFL season/week
        season, week = get_nfl_time()

        # Get data
        pbp, schedule, elo_ratings = get_data(season = season, week = week)
        schedule = schedule[schedule["week"] == week] # Only get current week

        model = NFLPredictionModel(schedule, pbp, elo_ratings)
        model.load("model.pkl")
        model.make_predictions()

if __name__ == "__main__":
    # Check if an argument exist
    if len(sys.argv) > 1:
        task = sys.argv[1]
        options = sys.argv[2:]

        # Check if the first argument is one of two options
        if task == "--train/test":
            main(task = task, options = options)

        elif task == "--predict":
            main(task = task, options = [])
    
    else:
        # Invalid Argument
        print("ERROR: Invalid argument!")