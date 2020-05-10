import pandas as pd 
import numpy as np 
from scipy.stats import norm

def Probability(teamhome, teamaway): 
    # Function to calculate the Probability 
    return 1.0 * 1.0 / (1 + 1.0 * np.power(10, 1.0 * (teamaway - teamhome) / 400)) 

def Load():
    dfELO = pd.read_csv("~/Desktop/Rugby/current.csv")
    dfELO.columns = ["ind","Team","ELO"]
    dfGame = pd.read_csv("~/Desktop/Rugby/games.csv")
    dfGame = dfGame.merge(dfELO, left_on="Team_A", right_on="Team")
    dfGame = dfGame.merge(dfELO, left_on="Team_B", right_on="Team")
    dfGame = dfGame.drop(['ind_x', 'ind_y', 'Team_x', 'Team_y'], axis=1)
    df = dfGame.rename(columns={"ELO_x": "ELO_A", "ELO_y": "ELO_B"})
    df["Prob_A"] = Probability(df.ELO_A,df.ELO_B)
    df["Prob_B"] = 1 - df["Prob_A"]
    df["Percentile"] = norm.ppf(df["Prob_A"])
    return df

def MC(df):
    list02 = [] 
    for y in range(100000):
        list01 = []
        for x in range(len(df)):
            count = np.random.normal(loc = 0, scale = 1, size = 1)
            list01.extend([df.Team_A[x] if count < df.Percentile.iloc[x] else df.Team_B[x]]) 
        list02.append(list01)
    df = pd.DataFrame(list02)
    return df

def data():
    data = {'Finish':[1.0,2.0,3.0,4.0,5.0]} 
    group_rank = pd.DataFrame(data) 
    return group_rank

def Rollup(group_rank):
    ind1 = 0
    ind2 = 10
    for i in range(4):
        a = group_result.iloc[:, ind1:ind2]
        b = pd.get_dummies(a, prefix_sep='', prefix='').sum(axis=1, level=0)
        c = b.rank(axis=1,method='first',ascending=False)
        list01 = c.columns
        for i in list01:
            d = c[i].value_counts()/1000
            e = d.rename_axis('Finish').reset_index(name=i)
            group_rank = pd.merge(group_rank, e, on="Finish", how="left").fillna(0)
        ind1 += 10
        ind2 += 10
    new_row = group_rank.iloc[0] + group_rank.iloc[1]
    group_rank = group_rank.append([new_row])
    return group_rank

'''####################### MAIN ######################'''

df = Load()
df[["Pool","Team_A","Team_B","ELO_A","ELO_B","Prob_A","Prob_B"]].to_csv("games_prob.csv")
df01 = df[["Pool","Team_A","Team_B","Prob_A"]]
df01.columns = ["Pool","Team_A","Team_B","Prob"]
df02 = df[["Pool","Team_B","Team_A","Prob_B"]]
df02.columns = ["Pool","Team_A","Team_B","Prob"]
df01.append(df02).to_csv("games_prob_viz.csv")

print('######################################')
print('Data loaded')
print('######################################')

group_result = MC(df)

print('######################################')
print('MC group')
print('######################################')

group_rank = data()

print('######################################')
print('Initialize Rank')
print('######################################')

group_rank = Rollup(group_rank)

print('######################################')
print('Group Rollup')
print('######################################')

group_rank.to_csv("Group_Rank.csv")




