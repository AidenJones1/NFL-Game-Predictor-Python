from .utils.file_utils import read_json, SERVER_DATA_CONFIGS_PATH
from .nfl_info import get_teams_names

from pandas import DataFrame, isna
from numpy import log

class ELORatings():
    """This class handles ELO Rating processing."""

    def __init__(self, schedule: DataFrame, current_week: int) -> None:
        path = f"{SERVER_DATA_CONFIGS_PATH}/elo_config.json"
        configs = read_json(file_path = path)

        # Get ELO Ratings Properties
        starting_elo = int(configs["base_elo"])
        k = int(configs["k"])
        hfa_bonus = int(configs["home_field_advantage_bonus"])

        # Instantiate new DataFrame
        elo_df = DataFrame({"Team": get_teams_names(abbreviated = True), "Week 0": starting_elo})
        
        # Loop through each week
        for week in range(1, current_week):
            week_schedule = schedule[schedule["week"] == week]

            # Loop through each game in the week
            for _, game in week_schedule.iterrows():
                # Skip games that haven't played yet
                if isna(game["result"]):
                    continue

                # Get game data
                away_team = game["away_team"]
                home_team = game["home_team"]
                result = game["result"]
                location = game["location"]

                # Get previous week elo rating
                away_team_elo = int(elo_df[elo_df["Team"] == away_team][f"Week {week - 1}"].values[0])
                home_team_elo = int(elo_df[elo_df["Team"] == home_team][f"Week {week - 1}"].values[0])
                base_home_team_elo = home_team_elo

                # Apply Home Field Advantage bonus if needed
                if location == "Home":
                    home_team_elo += hfa_bonus    

                # Calculate home team win probability based on ELO ratings
                home_team_win_probability = _calculate_win_probability(away_team_elo = away_team_elo, home_team_elo = home_team_elo)

                # Caculate Margin of Victory multiplier
                mov_bonus = _calculate_mov_multiplier(point_difference = result, home_team_elo = home_team_elo, away_team_elo = away_team_elo)

                # Evaluate the outcome and calculate ELO rating change (delta)
                # Home team wins
                if result > 0:
                    delta = k * mov_bonus * (1 - home_team_win_probability)

                # Home team lost
                elif result < 0:
                    delta = k * mov_bonus * (0 - home_team_win_probability)

                # Home team tied
                else:
                    delta = k * mov_bonus * (0.5 - home_team_win_probability)

                delta = round(delta)

                # Give out new ELO ratings
                away_team_elo = away_team_elo - delta
                home_team_elo = base_home_team_elo + delta

                elo_df.loc[elo_df["Team"] == away_team, f"Week {week}"] = away_team_elo
                elo_df.loc[elo_df["Team"] == home_team, f"Week {week}"] = home_team_elo
            # End of week's schedule loop

            # Fill team's who had a BYE week with their ELO Ratings from last week
            teams_played = set(week_schedule["home_team"]).union(set(week_schedule["away_team"]))
            all_teams = set(elo_df["Team"])
            bye_teams = all_teams - teams_played

            for team in bye_teams:
                prev_elo = elo_df[elo_df["Team"] == team][f"Week {week - 1}"].values[0]
                elo_df.loc[elo_df["Team"] == team, f"Week {week}"] = prev_elo

            elo_df.loc[:, f"Week {week}"] = elo_df.loc[:, f"Week {week}"].astype(int)
        # End of week loop

        self.ratings_df = elo_df

def _calculate_win_probability(home_team_elo: int, away_team_elo: int) -> float:
    exponent = (away_team_elo - home_team_elo) / 400
    win_probability = 1 / (1 + 10 ** exponent)

    return win_probability

def _calculate_mov_multiplier(point_difference: int, home_team_elo: int, away_team_elo: int) -> float:
    return log(abs(point_difference) + 1) * (2.2 / (((home_team_elo - away_team_elo) * 0.001) + 2.2))