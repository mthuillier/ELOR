from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv
from datetime import datetime
import math 
import numpy as np
from math import log
from operator import itemgetter

def initialize():

    # create an empty DataFrame
    results_df = pd.DataFrame()

    # url that we are scraping, the IRB rankings
    url_template = "http://stats.espnscrum.com/scrum/rugby/records/team/match_results.html?id={year};type=year"

    for year in range(1890, 2021):  # for each year

        print(year)

        if year != 1915 and year != 1916 and year != 1917 and year != 1918 and year != 1941 and year != 1943 and year != 1944:
            url = url_template.format(year=year)  # get the url
    
            # open the url as an html file
            html = urlopen(url)

            # parsing the html file with the python parser 'html.parser'
            soup = BeautifulSoup(html, 'html.parser')

            # getting the column headers
            # th for table headers, soup find all the tr for table rows, limit 2 for the two lines that constituted the header, index 1 for choosing the second line
            # find all table headers

            column_headers = [th.getText() for th in soup.findAll('tr', limit=1)[0].findAll('th')]
            #print(column_headers)

            #ignore the first two lines as they are part of the header, then find all rows of the table and put them into data_rows
            data_rows = soup.findAll('tr')[1:]
            #print(data_rows)

            #inspecting the html, the data is contained in 'th' and 'tr' and 'td', so we find all in all the rows past the header in data_rows
            #we go about it for all the length in data_rows
            #We use the BeautifulSoup function getText() to extract the table data element 'td' and use it to put it into nested lists
            team_data = [[td.getText() for td in data_rows[i].findAll(['td', 'tr', 'th'])] for i in range(len(data_rows))]
            #print(team_data)

            #Finally using pandas, with the team_data and the name of the columns column_headers, from the list of lists team_data we create a pandas DF that we can then further manipulate
            df = pd.DataFrame(team_data, columns=column_headers)
            df.insert(0, 'Year', year)
    
            results_df = results_df.append(df, ignore_index=True)

    return results_df

def clean(df):
    
    df = df.drop(['Unnamed: 0', 'Unnamed: 8', 'Match', 'Ground'], axis=1)
    df = df.rename(index=str, columns={"Team": "Home_Team", "Pts": "Home_Score", "Pts.1": "Away_Score", "Team.1": "Away_Team"})
    df = df.dropna()

    return df

def set_ELO(df):
    
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

    return df

def Probability(teamhome, teamaway): 
    # Function to calculate the Probability 
    
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (teamaway - teamhome) / 400)) 

def EloRating(Ratinghome, Ratingaway, diff, K, d): 
    # Function to calculate Elo rating 
    # K is a constant.
    # d determines whether 
    # Home team wins or Away team.  

    # To calculate the Winning 
    # Probability of away team 

    Ratinghome = Ratinghome + 75
    Paway = Probability(Ratingaway, Ratinghome) 
  
    # To calculate the Winning 
    # Probability of home team 
    Phome = Probability(Ratinghome, Ratingaway) 
    Ratinghome = Ratinghome - 75

    mov = log(abs(diff) + 1)
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


def WinPer():
    tot = []
    for x in range(0,4000,10):
        newhome, newaway, homeprob, awayprob= EloRating(x, 2000, 10, 40, 1)
        bufscore = x - 2000
        bufprob = homeprob
        tot.append((bufscore,bufprob))

    WinPer = pd.DataFrame()
    WinPer["score"] = ""
    WinPer["Prob"] = ""
    for x in range(len(tot)):
        WinPer.loc[x,"score"] = tot[x][0]
        WinPer.loc[x,"Prob"] = tot[x][1]

    WinPer.to_csv("old_files/percentages.csv")

def update_ELO(df):
    
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

        Home_Rating_Updated, Away_Rating_Updated, Prob_Home, Prob_Away= EloRating(Ratinghome, Ratingaway, diff, K, d)

        df.at[x, 'Home_Rating_Updated'] = Home_Rating_Updated
        df.at[x, 'Away_Rating_Updated'] = Away_Rating_Updated
        df.at[x, 'Prob_Home'] = Prob_Home
        df.at[x, 'Prob_Away'] = Prob_Away

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
    
    return df

def get_rank(df):
    teams = list(set(df.Home_Team) | set(df.Away_Team))
    #teams = ['Argentina','Australia','Canada','England','Fiji','France','Georgia','Ireland','Italy','Japan','Namibia','New Zealand','Russia','Samoa','Scotland','South Africa','Tonga','Uruguay','USA','Wales']
    ranking = []
    for x in teams:
        for i in range(len(df)):
            if df.Home_Team[i] == x:
                rating = (x,round(df.Home_Rating_Updated[i]))
            elif df.Away_Team[i] == x:
                rating = (x,round(df.Away_Rating_Updated[i]))
        ranking.append(rating)
    ranking.sort(key = lambda x: x[1], reverse=True)
    df5 = pd.DataFrame(ranking)
    return df5

'''####################### MAIN ######################'''

df1 = initialize()
df1.to_csv("ELO/ELO1.csv")

print('######################################')
print('Data Collected')
print('######################################')

df1 = pd.read_csv("ELO/ELO1.csv")
df2 = clean(df1)
df2.to_csv("ELO/ELO2.csv")

print('######################################')
print('Data Cleaned')
print('######################################')

df2 = pd.read_csv("ELO/ELO2.csv")
df3 = set_ELO(df2)
df3.to_csv("ELO/ELO3.csv")

print('######################################')
print('ELO Initialized')
print('######################################')

df3 = pd.read_csv("ELO/ELO3.csv")
df4 = update_ELO(df3)
df4.to_csv("ELO/ELO4.csv")

print('######################################')
print('ELO Finished')
print('######################################')

df5 = get_rank(df4)
df5.to_csv("ELO/current.csv")

print('######################################')
print('Rank Finished')
print('######################################')

