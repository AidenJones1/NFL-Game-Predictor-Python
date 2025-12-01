from pandas import DataFrame
from ..utils.file_utils import SERVER_DATA_CONFIGS_PATH, read_json
from .features_util import calculate_elo_difference, calculate_stat, calculate_stat_difference

def parse_features(pbp: DataFrame, schedule: DataFrame, elo_ratings: DataFrame) -> DataFrame:
    path = f"{SERVER_DATA_CONFIGS_PATH}/learning_model_config.json"
    configs = read_json(file_path = path)
    
    window = int(configs["games_window"])

    metrics = DataFrame({
        "home_field_advantage": [],
        "elo_difference": [],
        "off_epa_difference": [],
        "def_epa_difference": [],
        "off_avg_yards_difference": [],
        "def_avg_yards_difference": [],
        "off_avg_td_difference": [],
        "def_avg_td_difference": [],
        #"off_avg_interception_difference": [],
        #"def_avg_interception_difference": [],
        #"off_avg_fumbles_lost_difference": [],
        #"def_avg_fumbles_lost_difference": [],
        "rest_days_difference": []
    })

    # Home Field Advantage
    metrics["home_field_advantage"] = (schedule["location"] == "Home").astype(int)

    # ELO Difference
    metrics["elo_difference"] = schedule.apply(lambda x: calculate_elo_difference(x, elo_df = elo_ratings), axis = 1)

    # EPA per play / Game (last 5 games)
    rolling_epa = calculate_stat(schedule, pbp, "epa", "mean", window)
    metrics[["off_epa_difference", "def_epa_difference"]] = schedule.apply(lambda x: calculate_stat_difference(rolling_epa, x), axis = 1)

    # Total Yards / Game  (last 5 games)
    rolling_total_yards = calculate_stat(schedule, pbp, "yards_gained", "sum", window)
    metrics[["off_avg_yards_difference", "def_avg_yards_difference"]] = schedule.apply(lambda x: calculate_stat_difference(rolling_total_yards, x), axis = 1)

    # Total Touchdowns / Game (last 5 games)
    rolling_td = calculate_stat(schedule, pbp, "touchdown", "sum", window)
    metrics[["off_avg_td_difference", "def_avg_td_difference"]] = schedule.apply(lambda x: calculate_stat_difference(rolling_td, x), axis = 1)

    #rolling_interception = calculate_stat(schedule, pbp, "interception", "sum", window)
    #metrics[["off_avg_interception_difference", "def_avg_interception_difference"]] = schedule.apply(lambda x: calculate_stat_difference(rolling_interception, x), axis = 1)

    #rolling_fumbles_lost = calculate_stat(schedule, pbp, "fumble_lost", "sum", window)
    #metrics[[ "off_avg_fumbles_lost_difference", "def_avg_fumbles_lost_difference"]] = schedule.apply(lambda x: calculate_stat_difference(rolling_fumbles_lost, x), axis = 1)

    # Rest Days Difference
    metrics["rest_days_difference"] = schedule["home_rest"] - schedule["away_rest"]

    return metrics

def parse_response(schedule: DataFrame):
    # A positive result == home win, negative result == home loss
    return (schedule["result"] > 0).astype(int)