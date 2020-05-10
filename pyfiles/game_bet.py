
import pandas as pd
import math 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import pickle
from sympy.solvers import solve
from sympy import Symbol
import math

#pickle load

df = pd.read_csv("ELO6.csv")

cat = pd.read_csv("categories.csv")

separation = abs(cat.iloc[0][1] - cat.iloc[1][1])

x = pd.DataFrame()

x["pts_for_home"] = df.pts_for_home
x["pts_against_home"] = df.pts_against_home
x["pts_for_away"] = df.pts_for_away
x["pts_against_away"] = df.pts_against_away
x["elo_home"] = df.Home_Rating
x["elo_away"] = df.Away_Rating
x["avg_margin"] = df.avg_margin
x["avg_A"] = df.avg_A
x["avg_B"] = df.avg_B

y = pd.DataFrame()

y["Home_Team"] = df.Home_Team
y["Away_Team"] = df.Away_Team

#model predict
model = pickle.load(open("model1.pkl", "rb"))
prediction = model.predict(x)
y["margin"] = prediction

model = pickle.load(open("model2.pkl", "rb"))
prediction = model.predict(x)
y["Home_Score_Predicted"] = prediction

model = pickle.load(open("model3.pkl", "rb"))
prediction = model.predict(x)
y["Away_Score_Predicted"] = prediction

Team_A = "Wales"
Team_B = "Fiji"
#print(y[(y.Home_Team == Team_A) & (y.Away_Team == Team_B)])

print(y.tail(2))