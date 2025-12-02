from modules.model import NFLPredictionModel, evaluate_predictions, get_predictions
from modules.nfl_info import get_nfl_time
from modules.nfl_stats import NFLData

import sys

def main(task: str, options: list[str]):
    if task == "--train/test":
        season = 2024
        week = 23

        # Get Data
        data = NFLData(season, week)

        # Create Model
        model = NFLPredictionModel(data.schedule, data.pbp, data.elo_ratings)
        model.create()

        # Print Testing Results
        if "--print" in options:
            model.print_test()

        # Save Model
        if "--save" in options:
            model.save("model.pkl")

    elif task == "--predict":
        # Current NFL season/week
        season, week = get_nfl_time()

        if week == 0 or week == 1:
            print("Currently in offseason or week 1. No predictions were made.")
            return
        
        last_week = week - 1

        # Get Data
        data = NFLData(season, week)

        # Split the schedule into current week and last week
        current_schedule = data.schedule[data.schedule["week"] == week]
        last_week_schedule = data.schedule[data.schedule["week"] == last_week]

        # Evaluate last week predicitons
        try:
            last_week_predictions = get_predictions(season, last_week)
            evaluate_predictions(last_week_schedule, last_week_predictions)
            
        except:
            print("Unable to get last weeks prediction.")

        # Load Model
        model = NFLPredictionModel(current_schedule, data.pbp, data.elo_ratings)
        model.load("model.pkl")

        # Make Predictions
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