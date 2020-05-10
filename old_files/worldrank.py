# Python 3 program for Elo Rating 
import math 
import pandas as pd
from statistics import mean
import numpy as np
from sklearn.metrics import brier_score_loss, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
from prettytable import PrettyTable
from operator import itemgetter
from datetime import date, timedelta, datetime

df = pd.read_csv("match_results_1995_to_2018_ELO_all.csv")

home = df[['Date','Home_Team','Home_Rating']]
away = df[['Date','Away_Team','Away_Rating']]

home = home.rename(index=str, columns={"Date": "Date", "Home_Team": "Team", "Home_Rating": "ELO"})
away = away.rename(index=str, columns={"Date": "Date", "Away_Team": "Team", "Away_Rating": "ELO"})

frames = [home,away]

rank = pd.concat(frames,ignore_index=True)

rank["Rank"] = rank.groupby('Date')["ELO"].rank(ascending=False,method='dense')

#rank.sort_values("Rank", inplace = True) 

print(rank)
