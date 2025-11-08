from .nfl_utils.nfl_stats_cleaner import clean_pbp_data, clean_schedule_data

import nfl_data_py as nfl_data
from pandas import DataFrame

def download_data(season: int) -> tuple[DataFrame, DataFrame]:
    """Retrieve the play-by-play data and schedule data for the specified NFL season.

    Args:
        season (int): The year of the NFL season.

    Returns:
        tuple(DataFrame, DataFrame): A tuple containing:
        - DataFrame: The Play-By-Play data.
        - DataFrame: The Schedule data."""
    # Download data from the nfl-data-py module and clean it
    pbp: DataFrame = nfl_data.import_pbp_data(years = [season])
    pbp = clean_pbp_data(downloaded_pbp = pbp)

    schedule: DataFrame = nfl_data.import_schedules(years = [season])
    schedule = clean_schedule_data(downloaded_schedule = schedule)

    return pbp, schedule