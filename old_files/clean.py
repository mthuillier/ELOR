import pandas as pd 
import csv
from datetime import datetime

df = pd.read_csv("match_results_1995_to_2018.csv")

df = df.drop(['Unnamed: 0', 'Unnamed: 8', 'Match', 'Ground'], axis=1)
df = df.rename(index=str, columns={"Team": "Home_Team", "Pts": "Home_Score", "Pts.1": "Away_Score", "Team.1": "Away_Team"})
df = df.dropna()

df.to_csv("match_results_1995_to_2018_all_teams.csv")