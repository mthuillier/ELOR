
# Python 3 program for analysis
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

# load in data
df = pd.read_csv("match_results_1995_to_2018_ELO_all.csv")
df = df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'line'], axis=1)

# get teams
teams = sorted(list(set(df.Home_Team.unique())|set(df.Away_Team.unique())))

mask = df.Series.str.contains('Six Nations') | df.Series.str.contains('Tri Nations') | df.Series.str.contains('Rugby Championship') | df.Series.str.contains('Five Nations')
mask2 = df.Series.str.contains('Six Nations') | df.Series.str.contains('Rugby World Cup') | df.Series.str.contains('Tri Nations') | df.Series.str.contains('Rugby Championship') | df.Series.str.contains('Five Nations')
mask3 = df.Series.str.contains('Rugby World Cup') 

#prime games and non prime games
df_prime = df.loc[mask]
df_second = df.loc[~mask2]
df_world = df.loc[mask3]

#analysis on prime/non prime
print(mean(df.Margin))
print(mean(df_prime.Margin))
print(mean(df_second.Margin))
print(mean(df_world.Margin))

#group_by teams
