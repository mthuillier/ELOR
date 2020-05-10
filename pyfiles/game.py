import pandas as pd
import numpy as np

df = pd.read_csv("ELO4.csv")

df1 = df[["Home_Team","Home_Rating_Updated","Date","Year"]]
df2 = df[["Away_Team","Away_Rating_Updated","Date","Year"]]
df1.columns = ["Team","Rating","Date","Year"]
df2.columns = ["Team","Rating","Date","Year"]
df = df1.append(df2, ignore_index = True)



df['Date'] = pd.to_datetime(df['Date'])

df['Month'] = df.Date.dt.strftime('%b')

df = df.drop(['Date'], axis=1)

df["Date"] = str(df.Year)

print(df.Month)
#df.to_csv("rank.csv")