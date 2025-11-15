from modules.nfl import get_nfl_time
from modules.nfl_stats_downloader import download_data
from modules.utils.file_utils import SERVER_DATA_PATH, create_directory, save_model
from modules.model import get_features, get_response, create_model, make_predictions
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

        response = get_response(schedule = schedule)
        metrics = get_features(pbp = pbp, schedule = schedule, elo_ratings = elo_ratings)

        dataset = metrics.copy()
        dataset["home_win"] = response
        dataset = dataset.dropna()

        x = dataset.iloc[:, :-1]
        y = dataset.iloc[:, -1]

        model = create_model(X = x, y = y, print_test_results = "--print" in options)

        # Save
        if "--save" in options:
            save_model(model = model)
            print("\nMODEL SAVED!!!")

    elif task == "--predict":
        # Current NFL season/week
        season, week = get_nfl_time()

        # Get data
        pbp, schedule, elo_ratings = get_data(season = season, week = week)
        schedule = schedule[schedule["week"] == week] # Only get current week
        #schedule = schedule[schedule['result'].isna()] # Only get games that haven't been played

        x = get_features(pbp = pbp, schedule = schedule, elo_ratings = elo_ratings)

        make_predictions(schedule, x)

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