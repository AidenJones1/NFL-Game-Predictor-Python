from pandas import DataFrame, Series

def calculate_elo_difference(game: Series, elo_df: DataFrame) -> int:
    # Get game data
    week = game["week"]
    home_team = game["home_team"]
    away_team = game["away_team"]

    # Get elo ratings leading up to the game
    home_team_elo = int(elo_df[elo_df["Team"] == home_team][f"Week {week - 1}"].values[0])
    away_team_elo = int(elo_df[elo_df["Team"] == away_team][f"Week {week - 1}"].values[0])

    # Calculate difference
    elo_difference = home_team_elo - away_team_elo

    return elo_difference

def get_rolling_stat(game_data, epa: DataFrame, side: str):
    week = game_data["week"]
    team = game_data["team"]

    if week <= 1:
        return "NaN"

    try:
        res = epa[(epa["week"] == week - 1) & (epa[side] == team)]["rolling_stat"].values[0]

    except:
        # Accounts for BYE week 
        res = epa[(epa["week"] == week - 2) & (epa[side] == team)]["rolling_stat"].values[0]

    return res

def calculate_stat(schedule: DataFrame, pbp: DataFrame, stat: str, func: str, window: int):
    """Examples:\n
        - stat: 'yards_gained', func: 'sum', window: 5 == Averge Total Yards Gained within a 5 game window.
        - stat 'touchdown', func: 'mean', window: 7 == Average Touchdown/Play within a 7 game window."""
    
    new_sched = (schedule.melt(id_vars = ["game_id", "season", "week"], value_vars = ["home_team", "away_team"], value_name = "team")
        .sort_values(["game_id", "variable"])[["season", "week", "game_id", "team"]])

    # Get EPA/play performance for both teams in each game
    off_game_stat: DataFrame = pbp.groupby(["game_id", "posteam", "season", "week"]).agg({stat: func}).reset_index()
    def_game_stat: DataFrame = pbp.groupby(["game_id", "defteam", "season", "week"]).agg({stat: func}).reset_index()

    # Calculate the average statline within an n game window
    off_game_stat[f"rolling_stat"] = (
    off_game_stat.groupby(["posteam", "season"], group_keys = False)[stat]
        .apply(lambda x: x.shift().rolling(window, min_periods = 1).mean()))    

    def_game_stat[f"rolling_stat"] = (
        def_game_stat.groupby(["defteam", "season"], group_keys = False)[stat]
        .apply(lambda x: x.shift().rolling(window, min_periods = 1).mean()))

    new_sched["off_rolling_stat"] = new_sched.apply(lambda x: get_rolling_stat(x, off_game_stat, "posteam"), axis = 1)
    new_sched["def_rolling_stat"] = new_sched.apply(lambda x: get_rolling_stat(x, def_game_stat, "defteam"), axis = 1)

    return new_sched

def calculate_stat_difference(rolling_stats, game) -> Series:
    # Game data
    game_id = game["game_id"]
    home_team = game["home_team"]
    away_team = game["away_team"]

    s: Series = Series(dtype = 'float64')

    home_off_stat: float = float(rolling_stats[(rolling_stats["game_id"] == game_id) & (rolling_stats["team"] == home_team)]["off_rolling_stat"].values[0])
    away_off_stat: float = float(rolling_stats[(rolling_stats["game_id"] == game_id) & (rolling_stats["team"] == away_team)]["off_rolling_stat"].values[0])

    home_def_stat: float = float(rolling_stats[(rolling_stats["game_id"] == game_id) & (rolling_stats["team"] == home_team)]["def_rolling_stat"].values[0])
    away_def_stat: float = float(rolling_stats[(rolling_stats["game_id"] == game_id) & (rolling_stats["team"] == away_team)]["def_rolling_stat"].values[0])

    # Calculate epa difference
    s["off_stat_diff"] = home_off_stat - away_def_stat
    s["def_stat_diff"] = away_off_stat - home_def_stat

    return s