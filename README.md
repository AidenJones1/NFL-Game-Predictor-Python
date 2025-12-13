# NFL Game Predictor Python
A machine learning model that predicts the outcome of an NFL game.

## Table of Contents
1. [How to Setup](#how-to-setup)
2. [How to Use](#how-to-use)
3. [ELO Rating System](#elo-rating-system)
4. [Model Features](#model-features)
5. [Performance](#model-performance)
6. [Prediction History](#model-prediction-history)
7. [Future Plans](#future-plans)
8. [Author/Contact Info](#author--contact-info)
9. [Links](#links)

## How to Setup
As of right now, there is no client application but you can still make predictions and train & test models by [downloading](https://github.com/AidenJones1/NFL-Game-Predictor-Python/archive/refs/heads/main.zip) the "server" files.

Requirements: Python 3.12.0
### VS Code Setup
1. **Open** downloaded folder on VS Code
2. **Click** the search bar on the top
3. **Click** Show and Run Commands
4. **Click** Python: Create Environment
5. **Click** Venv
6. **Click** Python 3.12.0
7. **Check** requirements.txt
8. **Activate** virtual environment: **ctrl + shift + `**

## How to Use
- To make Predictions:

        python.exe .\src\nfl_predictor_package\server\__main__.py --predict
    
- To Train/Test without test results:

        python.exe .\src\nfl_predictor_package\server\__main__.py --train/test
    
- To Train/Test with test results:

        python.exe .\src\nfl_predictor_package\server\__main__.py --train/test --print

- In case any modification was made in the models features:

        python.exe .\src\nfl_predictor_package\server\__main__.py --train/test --save

## ELO Rating System
The prediction model uses a custom ELO Rating system as one of the features. At the start of a new NFL season, each team starts at a base ELO rating of **1500**. A team's ELO rating will **increase for each win** and **decrease for each loss**. The amount is determined by the **margin of victory**, the difference between the two team's scores, and if that team was *favored to win* in the matchup.

Home teams with Home Field Advantage receives a small ELO bonus. Home teams playing at a neutral site will not receive the bonus.

## Model Features
- **Home Field Advantage**

- **ELO Difference**

- Home Team **Average Offense EPA** vs Away Team **Average Defense EPA** *(5 game window)*
- Home Team **Average Defense EPA** vs Away Team **Average Offense EPA** *(5 game window)*

- Home Team **Average Offense Yards** vs Away Team **Average Defense Yards** *(5 game window)*
- Home Team **Average Defense Yards** vs Away Team **Average Offense Yards** *(5 game window)*

- Home Team **Average Touchdowns Scored** vs Away Team **Average Touchdowns Given** *(5 game window)*
- Home Team **Average Touchdowns Given** vs Away Team **Average Touchdowns Scored** *(5 game window)*

- **Rest Days Difference** *(Days since a team last played)*

*Prediction model uses stats from the 2024 NFL Season*

## Model Performance
- ${\textsf{\color{aqua} Overall:}}$ ${\textsf{\color{White} 39 / 59 (66.1\%)}}$ 
- ${\textsf{\color{aqua} Best Performace*:}}$ ${\textsf{\color{gold} 12 / 15 (80.0\%)}}$ *(2025, Week 11)*
- ${\textsf{\color{aqua} Weekly Average Percentage*:}}$ ${\textsf{\color{White} (65.8\%)}}$

    *\* Excluding Playoffs*

## Model Prediction History
- 2025 Season, Week 14: ${\textsf{\color{white} 6 / 14 (42.9\%)}}$
- 2025 Season, Week 13: ${\textsf{\color{#873014} 11 / 16 (68.8\%)}}$
- 2025 Season, Week 12: ${\textsf{\color{silver} 10 / 14 (71.4\%)}}$
- 2025 Season, Week 11: ${\textsf{\color{gold} 12 / 15 (80.0\%)}}$

## Future Plans
- Host server files on an AWS server
- Set up an API
- Develop a client application

## Author / Contact Info
- ${\textsf{\color{red} AUTHOR:}}$ Aiden Jones
- ${\textsf{\color{red} EMAIL:}}$ aidenjjones03@gmail.com

## Links
- [LinkedIn](https://www.linkedin.com/in/aiden-jones-592001228/)
- [Twitter](https://x.com/aidenjones22)