from .utils.file_utils import SERVER_DATA_PATH, load_model, save_model, get_dataframe
from .model_utils.features import parse_features, parse_response

from pandas import DataFrame, concat
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

class NFLPredictionModel():
    def __init__(self, schedule: DataFrame, pbp: DataFrame, elo_ratings: DataFrame) -> None:
        """Sets a base for the learning model with the schedule data, play-by-play data, and elo ratings data."""
        
        self.schedule = schedule
        self.pbp = pbp
        self.elo_ratings = elo_ratings

    def create(self):
        """Instantiates a new Linear Regression model and fits it."""

        # Drop incomplete rows (likely week 1 data)
        features = parse_features(self.pbp, self.schedule, self.elo_ratings)
        response = parse_response(self.schedule)

        dataset = features.copy()
        dataset["home_win"] = response
        dataset.to_csv("dataset.csv", index = False)
        dataset = dataset.dropna()

        # Split Dataset
        X = dataset.iloc[:, :-1]
        y = dataset.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
        
        scalar = StandardScaler()
        X_train = scalar.fit_transform(X_train)
        X_test = scalar.transform(X_test)
        
        self.testing_set = (X_test, y_test)

        # Train Model
        self.model = LogisticRegression()
        self.model.fit(X_train, y_train)

    def print_test(self):
        """Test the training model and prints out the results."""

        if not self.__check_for_model():
            return
        
        # Test Model
        y_pred = self.model.predict(self.testing_set[0])

        accuracy = accuracy_score(self.testing_set[1], y_pred)
        cnf_matrix = confusion_matrix(self.testing_set[1], y_pred)

        # Print Test Results
        print("\nTEST PERFORMANCE")
        print(f"Coefficients: {self.model.coef_}")
        print("Accuracy: {:.2f}%".format(accuracy * 100))
        print(f"Confidence Matrix:\n{cnf_matrix}")

    def make_predictions(self):
        """Make a set of predictions with the provided schedule."""

        if not self.__check_for_model():
            return
    
        # Get Data
        X = parse_features(self.pbp, self.schedule, self.elo_ratings)
        y = self.model.predict(X)

        season = int(self.schedule.iloc[0]["season"])
        week = int(self.schedule.iloc[0]["week"])

        prediction_df = DataFrame({"away_team": [], "home_team": [], "prediction": []})

        for i in range(self.schedule.shape[0]):
            home_team = self.schedule.iloc[i]["home_team"]
            away_team = self.schedule.iloc[i]["away_team"]

            new_row = DataFrame({"away_team": [away_team], "home_team": [home_team], "prediction": [y[i]]})
            prediction_df = concat([prediction_df, new_row], ignore_index = True)

        # Save predictions
        prediction_df.to_csv(f"{SERVER_DATA_PATH}/{season} NFL Season/Predictions/Week {week}.csv", index = False)

    def save(self, filename: str):
        """Saves the loaded model under the 'src/server/models' directory."""

        if self.__check_for_model():
            save_model(self.model, filename)
            print("Model saved!!!")
            

    def load(self, model_file: str):
        """Load a saved model from the 'src/server/models' diretory."""

        loaded_model = load_model(model_file)

        if not loaded_model:
            print("Model filename not found. Ensure that it is located in 'src/server/models'")
            return
        
        self.model = loaded_model

    def __check_for_model(self):
        """[PRIVATE METHOD]\n\nChecks if a model is loaded."""
        if not self.model:
            print("Model not created!!! Either create a new model or load an existing model.")
            return False
        
        return True

def get_predictions(season: int, week: int):
    return get_dataframe(f"{SERVER_DATA_PATH}/{season} NFL Season/Predictions/Week {week}.csv")

def evaluate_predictions(last_week_schedule: DataFrame, predictions: DataFrame):
    evaluations = DataFrame({"away_team": [], "away_score": [], "home_team": [], "home_score": [], "result": [], "prediction": [], "correct_prediction": []})
    last_week_schedule = last_week_schedule.reset_index(drop = True)

    week = last_week_schedule.iloc[0]["week"]
    season = last_week_schedule.iloc[0]["season"]

    evaluations["away_team"] = last_week_schedule["away_team"]
    evaluations["away_score"] = last_week_schedule["away_score"]
    evaluations["home_team"] = last_week_schedule["home_team"]
    evaluations["home_score"] = last_week_schedule["home_score"]
    evaluations["result"] = last_week_schedule["result"]
    evaluations["prediction"] = predictions["prediction"]
    
    res = (last_week_schedule["result"] > 0).astype(int)
    evaluations["correct_prediction"] = res == predictions["prediction"].astype(int)

    evaluations.to_csv(f"{SERVER_DATA_PATH}/{season} NFL Season/Predictions/Week {week} Results.csv", index = False)