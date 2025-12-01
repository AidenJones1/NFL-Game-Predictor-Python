from modules.utils.file_utils import SERVER_DATA_PATH, create_directory
from modules import elo
from .nfl_stats_cleaner import clean_pbp_data, clean_schedule_data

import nfl_data_py as nfl
from pandas import DataFrame

class NFLData():
    def __init__(self, season: int, week: int) -> None:
        self.season = season
        self.week = week

        self.__download_data(save_data = True)

    def __download_data(self, save_data: bool = False):
        """Downloads all necessary data from the nfl-data-py module

        Args:
            save_data (bool, optional): Determine whether the save the downloaded data. Defaults to False."""
        
        # Get data from season
        self.pbp = nfl.import_pbp_data(years = [self.season]) 
        self.pbp = clean_pbp_data(downloaded_pbp = self.pbp)

        self.schedule = nfl.import_schedules(years = [self.season])
        self.schedule = clean_schedule_data(downloaded_schedule = self.schedule)
        
        # Construct ELO Ratings
        self.elo_ratings = elo.get_elo_ratings_df(schedule = self.schedule, current_week = self.week)

        # Save data
        if save_data:
            path = create_directory(directory_path = f"{SERVER_DATA_PATH}/{self.season} NFL Season")

            self.pbp.to_csv(path_or_buf = f"{path}/Play-By-Play Data.csv", index = False)
            self.schedule.to_csv(path_or_buf = f"{path}/Schedule Data.csv", index = False)
            self.elo_ratings.to_csv(path_or_buf = f"{path}/ELO Ratings Data.csv", index = False)