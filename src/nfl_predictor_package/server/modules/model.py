from .utils.file_utils import SERVER_DATA_CONFIGS_PATH, read_json, load_model, write_prediction
from .model_utils.model_utils import calculate_elo_difference, calculate_stat, calculate_stat_difference

from pandas import DataFrame, Series
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc


def get_response(schedule: DataFrame) -> Series:
    # Win Status
    home_win_status = (schedule["result"] > 0).astype(int)

    return home_win_status

def get_features(pbp: DataFrame, schedule: DataFrame, elo_ratings: DataFrame) -> DataFrame:
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

    # Rest Days Difference
    metrics["rest_days_difference"] = schedule["home_rest"] - schedule["away_rest"]

    return metrics

def create_model(X: DataFrame, y: Series, print_test_results: bool):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

    scalar = StandardScaler()
    X_train = scalar.fit_transform(X_train)
    X_test = scalar.transform(X_test)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    cnf_matrix = confusion_matrix(y_test, y_pred)

    if print_test_results:
        print("\nTEST PERFORMANCE")
        print(f"Coefficients: {model.coef_}")
        print("Accuracy: {:.2f}%".format(accuracy * 100))
        print(f"Confidence Matrix:\n{cnf_matrix}")

    return model

def make_predictions(schedule: DataFrame, x: DataFrame):
    prediction_string = ""
    model: LogisticRegression = load_model()
    
    y = model.predict(x)

    season = int(schedule.iloc[0]["season"])
    week = int(schedule.iloc[0]["week"])

    for i in range(schedule.shape[0]):
        home_team = schedule.iloc[i]["home_team"]
        away_team = schedule.iloc[i]["away_team"]

        if y[i] == 1:
            prediction_string += f"{away_team} <-- {home_team}\n"

        elif y[i] == 0:
            prediction_string += f"{away_team} --> {home_team}\n"

    write_prediction(prediction_string, f"{season} NFL Season/Predictions/Week {week}.txt")
