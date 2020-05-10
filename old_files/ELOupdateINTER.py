# Python 3 program for Elo Rating 
import math 
import pandas as pd
from math import log

df = pd.read_csv("match_results_1995_to_2018_ELO.csv")


# Function to calculate the Probability 
def Probability(teamhome, teamaway): 
  
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (teamaway - teamhome) / 400)) 

# Function to calculate Elo rating 
# K is a constant.
# d determines whether 
# Home team wins or Away team.  
def EloRating(Ratinghome, Ratingaway, diff, K, d, count): 

    #if count == 1:
    #    Ratinghome = Ratinghome / .9
    #elif count == 2:
    #    Ratingaway = Ratingaway / .9

    # To calculate the Winning 
    # Probability of away team 

    Ratinghome = Ratinghome + 80
    Paway = Probability(Ratingaway, Ratinghome) 
  
    # To calculate the Winning 
    # Probability of home team 
    Phome = Probability(Ratinghome, Ratingaway) 
    Ratinghome = Ratinghome - 80

    #if count == 1:
    #    Ratinghome = Ratinghome * .9
    #elif count == 2:
    #    Ratingaway = Ratingaway * .9

    mov = log(abs(diff)+1)
    cor = 2.2 / ((Phome - Paway)*.001 + 2.2)
    
    # Case -1 When Home team wins 
    # Updating the Elo Ratings 
    if (d == 1) : 
        Ratinghome = Ratinghome + cor * mov * K * (1 - Phome) 
        Ratingaway = Ratingaway + cor * mov * K * (0 - Paway) 
      
    # Case -2 When Away team wins 
    # Updating the Elo Ratings 
    elif (d == 0) : 
        Ratinghome = Ratinghome + cor * mov * K * (0 - Phome) 
        Ratingaway = Ratingaway + cor * mov * K * (1 - Paway) 

    # Case -3 When draw 
    # Updating the Elo Ratings 
    elif (d == .5) :
        Ratinghome = Ratinghome + cor * mov * K * (0.5 - Phome) 
        Ratingaway = Ratingaway + cor * mov * K * (0.5 - Paway) 

    return (round(Ratinghome, 6),round(Ratingaway, 6),round(Phome, 3),round(Paway, 3))

#print(EloRating(2174.159085, 1907.279527, 5, 40, 1))

# Driver code 

# Ratinghome and Ratingaway are current ELO ratings 

teams = ['New Zealand', 'France', 'Wales', 'Scotland', 'South Africa', 'Australia', 'England', 'Ireland', 'Lions', 'Italy', 'Argentina']

df["Home_Away_Draw"] = ""
df["Prob_Home"] = ""
df["Prob_Away"] = ""

for i in range(len(df)):

    try:
        df.loc[i,'Home_Score'] = int(df.Home_Score[i])
        df.loc[i,'Away_Score'] = int(df.Away_Score[i])
    except:
        df.drop(i, inplace=True)
df = df.reset_index(drop=True)


for x in range(len(df)):

    
    print(str(x) + " - " + str(len(df)))

    Ratinghome = df.Home_Rating[x]
    Ratingaway = df.Away_Rating[x]
    diff = abs(df.Margin[x])
  
    if int(df.Home_Score[x]) is not None and int(df.Away_Score[x]) is not None:
        if int(df.Home_Score[x]) > int(df.Away_Score[x]):
            d = 1
        elif int(df.Home_Score[x]) < int(df.Away_Score[x]):
            d = 0
        elif int(df.Home_Score[x]) == int(df.Away_Score[x]):
            d = .5


    df.loc[x,'Home_Away_Draw'] = d

    K = 40










    count = 0
    if df.Home_Team[x] in teams and df.Away_Team[x] not in teams:
        count = 1
    elif df.Away_Team[x] in teams and df.Home_Team[x] not in teams:
        count = 2
    














    Home_Rating_Updated, Away_Rating_Updated, Prob_Home, Prob_Away= EloRating(Ratinghome, Ratingaway, diff, K, d, count)

    df.set_value(x, 'Home_Rating_Updated', Home_Rating_Updated)
    df.set_value(x, 'Away_Rating_Updated', Away_Rating_Updated)
    df.set_value(x, 'Prob_Home', Prob_Home)
    df.set_value(x, 'Prob_Away', Prob_Away)

    counthome = 0
    countaway = 0


    for i in range(x+1, len(df)): #entire DF
        if counthome == 0: #repeat once
#HOME TEAM NEW RANKING
            if df.Home_Team[i] == df.Home_Team[x] or df.Away_Team[i] == df.Home_Team[x]:
                
                #enter the loop and check case
                if df.Home_Team[i] == df.Home_Team[x]:
                    #For each new year, adjust the rating
                    if df.Year[i] != df.Year[x]:
                        df.loc[i,'Home_Rating'] = df.Home_Rating_Updated[x]
                    else:
                        df.loc[i,'Home_Rating'] = df.Home_Rating_Updated[x]
                    counthome = 1

                elif df.Away_Team[i] == df.Home_Team[x]:
                    if df.Year[i] != df.Year[x]:
                        df.loc[i,'Away_Rating'] = df.Home_Rating_Updated[x]
                    else:
                        df.loc[i,'Away_Rating'] = df.Home_Rating_Updated[x]
                    counthome = 1

        if countaway == 0:
#AWAY TEAM NEW RANKING
            if df.Home_Team[i] == df.Away_Team[x] or df.Away_Team[i] == df.Away_Team[x]:
                #enter the loop and check case
                if df.Home_Team[i] == df.Away_Team[x]:
                    if df.Year[i] != df.Year[x]:
                        df.loc[i,'Home_Rating'] = df.Away_Rating_Updated[x]
                    else:
                        df.loc[i,'Home_Rating'] = df.Away_Rating_Updated[x]
                    countaway = 1

                elif df.Away_Team[i] == df.Away_Team[x]:
                    if df.Year[i] != df.Year[x]:
                        df.loc[i,'Away_Rating'] = df.Away_Rating_Updated[x]
                    else:
                        df.loc[i,'Away_Rating'] = df.Away_Rating_Updated[x]
                    countaway = 1

df.to_csv("match_results_1995_to_2018_ELO_all.csv")
