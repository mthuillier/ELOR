import pandas as pd 

df1 = pd.read_csv("current.csv")
df2 = pd.read_csv("location.csv")

df3 = df1.merge(df2, how='inner', left_on="0", right_on="name")
df3.to_csv("ELOR.csv")