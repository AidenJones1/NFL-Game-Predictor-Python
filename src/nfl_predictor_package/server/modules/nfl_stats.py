from modules.utils.file_utils import SERVER_DATA_PATH, SERVER_DATA_CONFIGS_PATH, create_directory, read_json
from modules.elo import ELORatings

import nfl_data_py as nfl
from pandas import DataFrame

class NFLData():
    """This class downloads all necessary data provided by the season and week upon instantiation."""
    def __init__(self, season: int, week: int) -> None:
        self.season = season
        self.week = week

        self.__download_data(save_data = True)

    def __download_data(self, save_data: bool = False):
        """Downloads all necessary data from the nfl-data-py module.

        Args:
            save_data (bool, optional): Determine whether the save the downloaded data. Defaults to False."""
        
        # Get data from season
        self.pbp = nfl.import_pbp_data(years = [self.season]) 
        self.pbp = _clean_pbp_data(downloaded_pbp = self.pbp)

        self.schedule = nfl.import_schedules(years = [self.season])
        self.schedule = _clean_schedule_data(downloaded_schedule = self.schedule)
        
        # Construct ELO Ratings
        elo = ELORatings(self.schedule, self.week)
        self.elo_ratings = elo.ratings_df

        # Save data
        if save_data:
            path = create_directory(directory_path = f"{SERVER_DATA_PATH}/{self.season} NFL Season")

            self.pbp.to_csv(path_or_buf = f"{path}/Play-By-Play Data.csv", index = False)
            self.schedule.to_csv(path_or_buf = f"{path}/Schedule Data.csv", index = False)
            self.elo_ratings.to_csv(path_or_buf = f"{path}/ELO Ratings Data.csv", index = False)

def _clean_pbp_data(downloaded_pbp: DataFrame) -> DataFrame:
    """Converts the downloaded version of nfl-data-py's pbp data into a cleaner version.

    Args:
        downloaded_pbp (DataFrame): The downloaded version of the pbp data.

    Returns:
        DataFrame: The clean version of the pbp data."""
    
    # Get Columns to Keep from JSON file
    path = f"{SERVER_DATA_CONFIGS_PATH}/data_config.json"
    configs = read_json(file_path = path)

    columns_to_keep = configs["pbp_columns_to_keep"]

    # Keep all necessary data
    cleaned_pbp: DataFrame = downloaded_pbp[columns_to_keep]

    # Add extra data
    home_score_diff = cleaned_pbp["total_home_score"] - cleaned_pbp["total_away_score"]
    cleaned_pbp.insert(loc = 22, column = "home_score_diff", value = home_score_diff)

    return cleaned_pbp

def _clean_schedule_data(downloaded_schedule: DataFrame) -> DataFrame:
    """Converts the downloaded version of nfl-data-py's schedule data into a cleaner version.

    Args:
        downloaded_schedule (DataFrame): The downloaded version of the schedule data.

    Returns:
        DataFrame: The clean version of the schedule data."""
    
    # Get Columns to Keep from JSON file
    path = f"{SERVER_DATA_CONFIGS_PATH}/data_config.json"
    configs = read_json(file_path = path)

    columns_to_keep = configs["schedule_columns_to_keep"]

    # Keep all necessary data
    cleaned_schedule = downloaded_schedule[columns_to_keep]

    return cleaned_schedule