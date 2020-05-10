
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

teams = ['Argentina','Australia','Canada','England','Fiji','France','Georgia','Ireland','Italy','Japan','Namibia','New Zealand','Russia','Samoa','Scotland','South Africa','Tonga','Uruguay','USA','Wales']


df = pd.read_csv("ELO4.csv")

df = df[df.Year >= 1995]
df["pts_for_home"] = ""
df["pts_against_home"] = ""
df["pts_for_away"] = ""
df["pts_against_away"] = ""
df["avg_margin"] = ""
df["score_diff"] = df.Home_Score - df.Away_Score
df04 = df[((df.Year == 2019) & (df.Series == "Rugby World Cup"))]
df04["ELO_diff"] = df04.Home_Rating - df04.Away_Rating
df = df[~((df.Year == 2019) & (df.Series == "Rugby World Cup"))]
df["ELO_diff"] = df.Home_Rating + 75 - df.Away_Rating

margin = []
all_teams = pd.unique(df[['Home_Team', 'Away_Team']].values.ravel('K'))
for i in all_teams:
    test01 = df[(df.Home_Team == i)]
    test02 = df[(df.Away_Team == i)]

    avg_for = (sum(test01.Home_Score) + sum(test02.Away_Score)) / (len(test01) + len(test02))
    avg_against = (sum(test01.Away_Score) + sum(test02.Home_Score)) / (len(test01) + len(test02))

    margin.append((i,avg_for,avg_against))

x = np.array(df.Home_Rating + 75 - df.Away_Rating)

range01 = max(x) - min(x)

z = Symbol('z')
separation = round(solve(range01/z - 75, z)[0])

cat = []
for i in range(int(min(x)), int(max(x)), separation):
    test = df[(df.ELO_diff > i) & (df.ELO_diff <= i+separation)]
    cat.append((i,np.mean(test.score_diff)))

cat = [t for t in cat if not any(isinstance(n, float) and math.isnan(n) for n in t)]

pd.DataFrame(cat).to_csv("categories.csv")

df = df.append(df04)
df = df.reset_index(drop=True)


for i in range(len(df)):
    for j in range(len(cat)):
        if df.ELO_diff.iloc[i] > cat[j][0] and df.ELO_diff.iloc[i] <= cat[j][0] + separation:
            df.avg_margin.iloc[i] = cat[j][1]

for x in range(len(df)):
    print(x/len(df)*100)
    for y in range(len(margin)):
        if df.Home_Team.iloc[x] == margin[y][0]:
            df.pts_for_home.iloc[x] = margin[y][1]
            df.pts_against_home.iloc[x] = margin[y][2]
        elif df.Away_Team.iloc[x] == margin[y][0]:
            df.pts_for_away.iloc[x] = margin[y][1]
            df.pts_against_away.iloc[x] = margin[y][2]


df = df.reset_index(drop=True)

df01 = df[df.Home_Team.isin(teams)]
df02 = df[df.Away_Team.isin(teams)]
df03 = df01.append(df02)
df03.drop_duplicates(inplace=True)

df04 = df03[~((df03.Year == 2019) & (df03.Series == "Rugby World Cup"))]

years = []
for i in range(len(df04)):

    test01 = df04[((df04.Home_Team == df04.Home_Team.iloc[i]) & (df04.Away_Team == df04.Away_Team.iloc[i]))]
    if len(test01[test01.Year >= 2015]) >= 5:
        test02 = test01[:-5]
    else:
        test02 = test01[test01.Year >= 2015]

    try:
        years.append((df04.Home_Team.iloc[i],df04.Away_Team.iloc[i],np.sum(test02.Home_Score),np.sum(test02.Away_Score),len(test02)))
    except:
        years.append((df04.Home_Team.iloc[i],df04.Away_Team.iloc[i],np.sum(test01.Home_Score),np.sum(test01.Away_Score),len(test01)))

years = list(set(years))
years = pd.DataFrame(years)
years.columns = ["Team_A","Team_B","SUM_A","SUM_B","COUNT"]


years['TeamA'] = years[['Team_A', 'Team_B']].values.min(axis=1)
years['TeamB'] = years[['Team_A', 'Team_B']].values.max(axis=1)

for i in range(len(years)):
    if years.Team_A.iloc[i] != years.TeamA.iloc[i]:
        score = years.SUM_A.iloc[i]
        years.SUM_A.iloc[i] = years.SUM_B.iloc[i]
        years.SUM_B.iloc[i] = score

years = years.groupby(['TeamA','TeamB']).agg({'SUM_A':'sum','SUM_B':'sum','COUNT':'sum'}).reset_index()
years["avg_A"] = years.SUM_A / years.COUNT
years["avg_B"] = years.SUM_B / years.COUNT



df03["avg_A"] = ""
df03["avg_B"] = ""
for i in range(len(df03)):
    print(i/len(df03)*100)
    for j in range(len(years)):
        if df03.Home_Team.iloc[i] == years.TeamA.iloc[j] and df03.Away_Team.iloc[i] == years.TeamB.iloc[j]:
            df03.avg_A.iloc[i] = years.avg_A.iloc[j]
            df03.avg_B.iloc[i] = years.avg_B.iloc[j]
        elif df03.Home_Team.iloc[i] == years.TeamB.iloc[j] and df03.Away_Team.iloc[i] == years.TeamA.iloc[j]:
            df03.avg_B.iloc[i] = years.avg_A.iloc[j]
            df03.avg_A.iloc[i] = years.avg_B.iloc[j]


df03.avg_A.replace('', np.nan, regex=True, inplace=True)
df03.avg_B.replace('', np.nan, regex=True, inplace=True)
df03 = df03.fillna(0)

for i in range(len(df03)):
    if df03.avg_A.iloc[i] == 0:
        df03.avg_A.iloc[i] = df03.pts_for_home.iloc[i]
    if df03.avg_B.iloc[i] == 0:
        df03.avg_B.iloc[i] = df03.pts_for_away.iloc[i]


df06 = df03[((df03.Year == 2019) & (df03.Series == "Rugby World Cup"))]
df03 = df03[~((df03.Year == 2019) & (df03.Series == "Rugby World Cup"))]

df03.to_csv("ELO5.csv")
df06.to_csv("ELO6.csv")


df03 = pd.read_csv("ELO5.csv")

df03 = df03[~df03.pts_for_home.isnull()]
df03 = df03[~df03.pts_against_home.isnull()]
df03 = df03[~df03.pts_for_away.isnull()]
df03 = df03[~df03.pts_against_away.isnull()]
df03 = df03[~df03.avg_margin.isnull()]

x = pd.DataFrame()
y = np.array(df03.Home_Score - df03.Away_Score)


x["pts_for_home"] = np.array(df03.pts_for_home)
x["pts_against_home"] = np.array(df03.pts_against_home)

x["pts_for_away"] = np.array(df03.pts_for_away)
x["pts_against_away"] = np.array(df03.pts_against_away)

x["elo_home"] = np.array(df03.Home_Rating)
x["elo_away"] = np.array(df03.Away_Rating)

x["avg_margin"] = np.array(df03.avg_margin)

x["avg_A"] = np.array(df03.avg_A)
x["avg_B"] = np.array(df03.avg_B)

rf1 = RandomForestRegressor(n_estimators = 1000, random_state = 42, bootstrap=True)

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

rf1.fit(x, y)
predictions = rf1.predict(x_test)
print("R2 for the model is: ", round(r2_score(predictions, y_test)*100,1))

pickle.dump(rf1, open("model1.pkl" , "wb"))


y = np.array(df03.Home_Score)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
rf2 = RandomForestRegressor(n_estimators = 1000, random_state = 42, bootstrap=True)
rf2.fit(x, y)
predictions = rf2.predict(x_test)
print("R2 for the model is: ", round(r2_score(predictions, y_test)*100,1))

pickle.dump(rf2, open("model2.pkl" , "wb"))

y = np.array(df03.Away_Score)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
rf3 = RandomForestRegressor(n_estimators = 1000, random_state = 42, bootstrap=True)
rf3.fit(x, y)
predictions = rf3.predict(x_test)
print("R2 for the model is: ", round(r2_score(predictions, y_test)*100,1))

pickle.dump(rf3, open("model3.pkl" , "wb"))
