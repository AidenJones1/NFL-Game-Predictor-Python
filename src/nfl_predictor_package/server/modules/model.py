from .utils.file_utils import SERVER_DATA_CONFIGS_PATH, read_json, load_model, write_prediction, save_model
from .model_utils.features import parse_features, parse_response

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

class NFLPredictionModel():
    def __init__(self, schedule: DataFrame, pbp: DataFrame, elo_ratings: DataFrame) -> None:
        self.schedule = schedule
        self.pbp = pbp
        self.elo_ratings = elo_ratings

    def create(self):
        # Drop incomplete rows
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
        if not self.__check_for_model():
            return
        
        prediction_string = ""
    
        # Get Data
        X = parse_features(self.pbp, self.schedule, self.elo_ratings)
        y = self.model.predict(X)

        season = int(self.schedule.iloc[0]["season"])
        week = int(self.schedule.iloc[0]["week"])

        for i in range(self.schedule.shape[0]):
            home_team = self.schedule.iloc[i]["home_team"]
            away_team = self.schedule.iloc[i]["away_team"]

            if y[i] == 1:
                prediction_string += f"{away_team} --> {home_team}\n"

            elif y[i] == 0:
                prediction_string += f"{away_team} <-- {home_team}\n"

        write_prediction(prediction_string, f"{season} NFL Season/Predictions/Week {week}.txt")

    def save(self, filename: str):
        if self.__check_for_model():
            save_model(self.model, filename)
            print("Model saved!!!")
            

    def load(self, model_file: str):
        loaded_model = load_model(model_file)

        if not loaded_model:
            print("Model filename not found. Ensure that it is located in 'src/server/models'")
            return
        
        self.model = loaded_model

    def __check_for_model(self):
        if not self.model:
            print("Model not created!!! Either create a new model or load an existing model.")
            return False
        
        return True
