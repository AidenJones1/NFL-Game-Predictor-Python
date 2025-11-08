from .utils.file_utils import SERVER_DATA_CONFIGS_PATH, read_json

import datetime as dt

def get_nfl_time() -> tuple[int, int]:
    """Retrieve the current season and the current week of said season. 

    Returns:
        tuple(int, int): A tuple containing:
        - int: The current NFL Season.
        - int: The current week of the season. 0 represents offseason relative to the season."""
    path = f"{SERVER_DATA_CONFIGS_PATH}/time_config.json"
    configs = read_json(file_path = path)

    # Current Season
    current_season = int(configs["current_nfl_season"])

    # Loop through each week and compare their starting/ending dates with the current data for current week
    for week in configs["dates"]:
        week_dates = configs["dates"][week]

        start_date = dt.datetime.strptime(week_dates["start_date"], "%Y-%m-%d")
        end_date = dt.datetime.strptime(week_dates["end_date"], "%Y-%m-%d")

        if start_date.date() <= dt.date.today() <= end_date.date():           
            current_week = int(week.split()[1]) # Current Week

            return (current_season, current_week)
            
    return (current_season, 0) # Offseason