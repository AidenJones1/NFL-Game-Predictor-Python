from ..utils.file_utils import read_json, SERVER_DATA_CONFIGS_PATH

from pandas import DataFrame, Series

def clean_pbp_data(downloaded_pbp: DataFrame) -> DataFrame:
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
    home_score_diff: Series = cleaned_pbp["total_home_score"] - cleaned_pbp["total_away_score"]
    cleaned_pbp.insert(loc = 22, column = "home_score_diff", value = home_score_diff)

    return cleaned_pbp

def clean_schedule_data(downloaded_schedule: DataFrame) -> DataFrame:
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