import pandas as pd 
import numpy as np 
from scipy.stats import norm
import itertools
import random
import warnings
warnings.filterwarnings("ignore")

dfELO = pd.read_csv("~/Desktop/Rugby/current.csv")
dfELO.columns = ["ind","Team","ELO"]
dfGroup = pd.read_csv("~/Desktop/Rugby/Group_Rank.csv")
dfGroup = dfGroup.drop(['Unnamed: 0'], axis=1)

def Probability(teamhome, teamaway): 
    # Function to calculate the Probability 
    return 1.0 * 1.0 / (1 + 1.0 * np.power(10, 1.0 * (teamaway - teamhome) / 400)) 

# Q1 1C/2D
def Q1f(dfGroup):
    C1 = dfGroup.iloc[:1, 11:16]*1000
    D2 = dfGroup.iloc[1:2, 16:21]*1000

    list01 = list(C1.columns)
    list02 = list(C1.loc[0,:])
    list03 = list(D2.columns)
    list04 = list(D2.loc[1,:])

    list05 = []
    list06 = []
    for x in range(5):
        list05.append(list(itertools.repeat(list01[x], round(list02[x]))))
        list06.append(list(itertools.repeat(list03[x], round(list04[x]))))

    list07 = [item for sublist in list05 for item in sublist]
    list08 = [item for sublist in list06 for item in sublist]
    random.shuffle(list07)
    random.shuffle(list08)

    return list07, list08

# Q2 1B/2A
def Q2f(dfGroup):
    B1 = dfGroup.iloc[:1, 6:11]*1000
    A2 = dfGroup.iloc[1:2, 1:6]*1000

    list01 = list(B1.columns)
    list02 = list(B1.loc[0,:])
    list03 = list(A2.columns)
    list04 = list(A2.loc[1,:])

    list05 = []
    list06 = []
    for x in range(5):
        list05.append(list(itertools.repeat(list01[x], round(list02[x]))))
        list06.append(list(itertools.repeat(list03[x], round(list04[x]))))

    list07 = [item for sublist in list05 for item in sublist]
    list08 = [item for sublist in list06 for item in sublist]
    random.shuffle(list07)
    random.shuffle(list08)

    return list07, list08

# Q3 1D/2C
def Q3f(dfGroup):
    D1 = dfGroup.iloc[:1, 16:21]*1000
    C2 = dfGroup.iloc[1:2, 11:16]*1000

    list01 = list(D1.columns)
    list02 = list(D1.loc[0,:])
    list03 = list(C2.columns)
    list04 = list(C2.loc[1,:])

    list05 = []
    list06 = []
    for x in range(5):
        list05.append(list(itertools.repeat(list01[x], round(list02[x]))))
        list06.append(list(itertools.repeat(list03[x], round(list04[x]))))

    list07 = [item for sublist in list05 for item in sublist]
    list08 = [item for sublist in list06 for item in sublist]
    random.shuffle(list07)
    random.shuffle(list08)

    return list07, list08

# Q4 1A/2B
def Q4f(dfGroup):
    A1 = dfGroup.iloc[:1, 1:6]*1000
    B2 = dfGroup.iloc[1:2, 6:11]*1000

    list01 = list(A1.columns)
    list02 = list(A1.loc[0,:])
    list03 = list(B2.columns)
    list04 = list(B2.loc[1,:])

    list05 = []
    list06 = []
    for x in range(5):
        list05.append(list(itertools.repeat(list01[x], round(list02[x]))))
        list06.append(list(itertools.repeat(list03[x], round(list04[x]))))

    list07 = [item for sublist in list05 for item in sublist]
    list08 = [item for sublist in list06 for item in sublist]
    random.shuffle(list07)
    random.shuffle(list08)

    return list07, list08

# S1 Q1/Q2
def S1f(df):

    list01 = list(df.Q1)
    list02 = list(df.Q1_count)
    list03 = list(df.Q2)
    list04 = list(df.Q2_count)

    list05 = []
    list06 = []
    for x in range(len(list01)):
        list05.append(list(itertools.repeat(list01[x], round(list02[x]))))
    for x in range(len(list02)):
        list06.append(list(itertools.repeat(list03[x], round(list04[x]))))

    list07 = [item for sublist in list05 for item in sublist]
    list08 = [item for sublist in list06 for item in sublist]
    random.shuffle(list07)
    random.shuffle(list08)

    return list07, list08

# S2 Q3/Q4
def S2f(df):

    list01 = list(df.Q3)
    list02 = list(df.Q3_count)
    list03 = list(df.Q4)
    list04 = list(df.Q4_count)

    list05 = []
    list06 = []
    for x in range(len(list01)):
        list05.append(list(itertools.repeat(list01[x], round(list02[x]))))
    for x in range(len(list02)):
        list06.append(list(itertools.repeat(list03[x], round(list04[x]))))

    list07 = [item for sublist in list05 for item in sublist]
    list08 = [item for sublist in list06 for item in sublist]
    random.shuffle(list07)
    random.shuffle(list08)

    return list07, list08

# G3 S1D/S2D
def G3f(df):

    list01 = list(df.S1)
    list02 = list(df.S1_count)
    list03 = list(df.S2)
    list04 = list(df.S2_count)

    list05 = []
    list06 = []
    for x in range(len(list01)):
        list05.append(list(itertools.repeat(list01[x], round(list02[x]))))
    for x in range(len(list02)):
        list06.append(list(itertools.repeat(list03[x], round(list04[x]))))

    list07 = [item for sublist in list05 for item in sublist]
    list08 = [item for sublist in list06 for item in sublist]
    random.shuffle(list07)
    random.shuffle(list08)

    return list07, list08

# F S1W/S2W
def Ff(df):
    
    list01 = list(df.S1)
    list02 = list(df.S1_count)
    list03 = list(df.S2)
    list04 = list(df.S2_count)

    list05 = []
    list06 = []
    for x in range(len(list01)):
        list05.append(list(itertools.repeat(list01[x], round(list02[x]))))
    for x in range(len(list02)):
        list06.append(list(itertools.repeat(list03[x], round(list04[x]))))

    list07 = [item for sublist in list05 for item in sublist]
    list08 = [item for sublist in list06 for item in sublist]
    random.shuffle(list07)
    random.shuffle(list08)

    return list07, list08

def build(list07,list08):
    df = pd.DataFrame()
    df["Team_A"] = list07
    df["Team_B"] = list08

    df = df.merge(dfELO, left_on="Team_A", right_on="Team")
    df = df.merge(dfELO, left_on="Team_B", right_on="Team")
    df = df.drop(['ind_x', 'ind_y', 'Team_x', 'Team_y'], axis=1)
    df = df.rename(columns={"Team_A": "Team_A", "Team_B": "Team_B", "ELO_x": "ELO_A", "ELO_y": "ELO_B"})
    df["Home_Prob"] = Probability(df.ELO_A,df.ELO_B)
    df["Percentile"] = norm.ppf(df["Home_Prob"])

    list01 = []
    list02 = []
    for x in range(len(df)):
        count = np.random.normal(loc = 0, scale = 1, size = 1)
        list01.extend([df.Team_A[x] if count < df.Percentile.iloc[x] else df.Team_B[x]]) 
        list02.extend([df.Team_A[x] if count > df.Percentile.iloc[x] else df.Team_B[x]]) 
    df01 = pd.DataFrame([[x,list01.count(x)] for x in set(list01)])
    df02 = pd.DataFrame([[x,list02.count(x)] for x in set(list02)])
    
    return df01, df02

def MC(dfGroup):
    # Q1/Q2 into S1
    list07, list08 = Q1f(dfGroup)
    Q1, _ = build(list07,list08)

    print('######################################')
    print('Q1 Finished')
    print('######################################')

    list07, list08 = Q2f(dfGroup)
    Q2, _ = build(list07,list08)

    print('######################################')
    print('Q2 Finished')
    print('######################################')

    df = pd.concat([Q1, Q2], axis=1).fillna(0)
    df.columns = ['Q1','Q1_count','Q2','Q2_count']

    list07, list08 = S1f(df)
    S1W, S1D = build(list07,list08)

    print('######################################')
    print('S1 Finished')
    print('######################################')

    # Q3/Q4 into S2
    list07, list08 = Q3f(dfGroup)
    Q3, _ = build(list07,list08)

    print('######################################')
    print('Q3 Finished')
    print('######################################')

    list07, list08 = Q4f(dfGroup)
    Q4, _ = build(list07,list08)

    print('######################################')
    print('Q4 Finished')
    print('######################################')

    df = pd.concat([Q3, Q4], axis=1).fillna(0)
    df.columns = ['Q3','Q3_count','Q4','Q4_count']

    list07, list08 = S2f(df)
    S2W, S2D = build(list07,list08)

    print('######################################')
    print('S2 Finished')
    print('######################################')

    # S1W/S2W into F
    df = pd.concat([S1W, S2W], axis=1).fillna(0)
    df.columns = ['S1','S1_count','S2','S2_count']

    list07, list08 = Ff(df)
    FW, FD = build(list07,list08)

    FW.columns = ['FW','FW_count']
    FW.FW_count = FW.FW_count/1000
    FD.columns = ['FD','FD_count']
    FD.FD_count = FD.FD_count/1000

    print('######################################')
    print('F Finished')
    print('######################################')

    # S1D/S2D into G3
    df = pd.concat([S1D, S2D], axis=1).fillna(0)
    df.columns = ['S1','S1_count','S2','S2_count']

    list07, list08 = G3f(df)
    G3W, G3D = build(list07,list08)

    G3W.columns = ['G3W','G3W_count']
    G3W.G3W_count = G3W.G3W_count/1000
    G3D.columns = ['G3W','G3D_count']
    G3D.G3D_count = G3D.G3D_count/1000

    print('######################################')
    print('G3 Finished')
    print('######################################')

    Q1.columns = ['Team','Count']
    Q3.columns = ['Team','Count']
    QCD = pd.DataFrame(pd.merge(Q1, Q3, on=['Team'], how='outer').set_index(['Team']).sum(axis=1))
    Q2.columns = ['Team','Count']
    Q4.columns = ['Team','Count']
    QAB = pd.DataFrame(pd.merge(Q2, Q4, on=['Team'], how='outer').set_index(['Team']).sum(axis=1))

    QCD.reset_index(level=0, inplace=True)
    QAB.reset_index(level=0, inplace=True)


    Q = QCD.append(QAB, ignore_index=True)
    Q = Q.T
    Q.columns = Q.iloc[0]
    Q = Q.iloc[1:2,:]/1000
    result = dfGroup.append(Q)
    result = result.drop(['Finish'], axis=1)

    Q1 = Q1.T
    Q1.columns = Q1.iloc[0]
    Q1 = Q1.iloc[1:2,:]/1000
    result = result.append(Q1)

    Q2 = Q2.T
    Q2.columns = Q2.iloc[0]
    Q2 = Q2.iloc[1:2,:]/1000
    result = result.append(Q2)

    Q3 = Q3.T
    Q3.columns = Q3.iloc[0]
    Q3 = Q3.iloc[1:2,:]/1000
    result = result.append(Q3)

    Q4 = Q4.T
    Q4.columns = Q4.iloc[0]
    Q4 = Q4.iloc[1:2,:]/1000
    result = result.append(Q4)

    print('######################################')
    print('Q Integrated')
    print('######################################')

    S1W.columns = ['Team','Count']
    S2W.columns = ['Team','Count']
    S = pd.DataFrame(pd.merge(S1W, S2W, on=['Team'], how='outer').set_index(['Team']).sum(axis=1))
    S = S.T
    S = S/1000
    result = result.append(S)

    S1W = S1W.T
    S1W.columns = S1W.iloc[0]
    S1W = S1W.iloc[1:2,:]/1000
    result = result.append(S1W)

    S2W = S2W.T
    S2W.columns = S2W.iloc[0]
    S2W = S2W.iloc[1:2,:]/1000
    result = result.append(S2W)

    print('######################################')
    print('S Integrated')
    print('######################################')

    G3D = G3D.T
    G3D.columns = G3D.iloc[0]
    G3D = G3D.iloc[1:2,:]
    result = result.append(G3D)

    G3W = G3W.T
    G3W.columns = G3W.iloc[0]
    G3W = G3W.iloc[1:2,:]
    result = result.append(G3W)

    print('######################################')
    print('G3 Integrated')
    print('######################################')

    FL = FD.T
    FL.columns = FL.iloc[0]
    FL = FL.iloc[1:2,:]
    result = result.append(FL)

    print('######################################')
    print('F Integrated')
    print('######################################')

    F = FW.T
    F.columns = F.iloc[0]
    F = F.iloc[1:2,:]
    result = result.append(F)
    result = result.reset_index(drop=True).fillna(0)
    result = result.T.reset_index()
    result.columns = ["Team","1st","2nd","3rd","4th","5th","Q","QW","Q1","Q2","Q3","Q4","SW","S1","S2","3L","3W","Runner-up","W"]

    return result

print('######################################')
print('Initialization')
print('######################################')

df = MC(dfGroup)

print('######################################')
print('MC finished')
print('######################################')

df.to_csv("Final_Rank.csv")
