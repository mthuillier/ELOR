import math 
import pandas as pd
import numpy as np

df = pd.read_csv("match_results_1995_to_2018_all_teams.csv")
df = df.rename(index=str, columns={"Unnamed: 0": "line"})

# Driver code 

df["Margin"] = np.nan
df["Home_Rating"] = ""
df["Away_Rating"] = ""
df["Home_Rating_Updated"] = ""
df["Away_Rating_Updated"] = ""

names = sorted(list(set(df.Home_Team.unique())|set(df.Away_Team.unique())))

first = []
teams = ['New Zealand', 'France', 'Wales', 'Scotland', 'South Africa', 'Australia', 'England', 'Ireland', 'Lions', 'Italy', 'Argentina']

for i in names:
    x = 0
    while df.Home_Team[x] != i and df.Away_Team[x] != i:
        x = x + 1
        if df.Home_Team[x] == i:
            first.append((x,'Home',i))
        elif df.Away_Team[x] == i:
            first.append((x,'Away',i))
first.append((0,'Home','Arabian Gulf'))
first.append((0,'Away','Kenya'))

pd.options.mode.chained_assignment = None  # default='warn'
for x in range(len(first)):
    if first[x][1] == 'Home' and first[x][2] not in teams:
        Rating = 1500
        df.Home_Rating[first[x][0]] = Rating
    elif first[x][1] == 'Home' and first[x][2] in teams:
        Rating = 1500
        df.Home_Rating[first[x][0]] = Rating
    elif first[x][1] == 'Away' and first[x][2] not in teams:
        Rating = 1500
        df.Away_Rating[first[x][0]] = Rating
    elif first[x][1] == 'Away' and first[x][2] in teams:
        Rating = 1500
        df.Away_Rating[first[x][0]] = Rating

for x in range(len(df)):
    if df.Home_Score[x].isdigit() and df.Away_Score[x].isdigit():
        df.Margin[x] = int(df.Home_Score[x]) - int(df.Away_Score[x])

df.to_csv("match_results_1995_to_2018_ELO.csv")



