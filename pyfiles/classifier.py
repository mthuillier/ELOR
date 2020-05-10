
import pandas as pd
import math 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics import r2_score
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import math

import numpy as np
import pandas as pd
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import pymc3 as pm, theano.tensor as tt
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import seaborn as sns

#pickle load
"""
df = pd.read_csv("ELO4.csv")
df = df[:-4]

year = df.Year.unique()

years = []
perc = []
for i in range(1995,2020):

    df1 = df[df.Year == i]
    y_true = df1.Home_Away_Draw * 2
    y_pred = df1.Prob_Home
    y_pred = np.where(y_pred > .5, 2, 
         (np.where(y_pred < .5, 0, 1)))
    print("Accuracy for year " + str(i) + " is " + str(round(accuracy_score(y_true, y_pred),2)*100) + "%")
    years.append(i)
    perc.append(round(accuracy_score(y_true, y_pred),2)*100)

plt.plot(years,perc,'.')

z = np.polyfit(years, perc, 1)
p = np.poly1d(z)
plt.plot(years,p(years),"r--")

plt.show()

"""

df = pd.read_csv("ELO5.csv")

teams = ['Argentina','Australia','Canada','England','Fiji','France','Georgia','Ireland','Italy','Japan','Namibia','New Zealand','Russia','Samoa','Scotland','South Africa','Tonga','Uruguay','USA','Wales']

df = df[(df.Home_Team.isin(teams)) & (df.Away_Team.isin(teams))]
df = df[df.Year >= 2015]
df_all = df[["Year","Home_Team","Away_Team","Home_Score","Away_Score"]]
df_all.columns = ["year", "home_team", "away_team", "home_score", "away_score"]

df_all['difference'] = np.abs(df_all['home_score']-df_all['away_score'])

df_all.groupby('year')['difference'].mean().plot(kind='bar', title='Average magnitude of scores difference', yerr=df_all.groupby('year')['difference'].std()).set_ylabel('Average (abs) point difference')
#plt.show()

df_all['difference_non_abs']=df_all['home_score']-df_all['away_score']
df_all.pivot_table('difference_non_abs', 'home_team', 'year')

df_all.pivot_table('difference_non_abs', 'home_team').rename_axis("Home_Team").plot(kind='bar', rot=0, legend=False).set_ylabel('Score difference Home team and away team')


df_all.pivot_table('difference_non_abs', 'away_team').rename_axis("Away_Team").plot(kind='bar', rot=0, legend=False).set_ylabel('Score difference Home team and away team')

#plt.show()

df = df_all[['home_team', 'away_team', 'home_score', 'away_score']]
teams = df.home_team.unique()
teams = pd.DataFrame(teams, columns=['team'])
teams['i'] = teams.index

df = pd.merge(df, teams, left_on='home_team', right_on='team', how='left')
df = df.rename(columns = {'i': 'i_home'}).drop('team', 1)
df = pd.merge(df, teams, left_on='away_team', right_on='team', how='left')
df = df.rename(columns = {'i': 'i_away'}).drop('team', 1)

observed_home_goals = df.home_score.values
observed_away_goals = df.away_score.values

home_team = df.i_home.values
away_team = df.i_away.values

num_teams = len(df.i_home.drop_duplicates())
num_games = len(home_team)

g = df.groupby('i_away')
att_starting_points = np.log(g.away_score.mean())
g = df.groupby('i_home')
def_starting_points = -np.log(g.away_score.mean())

with pm.Model() as model:
    # global model parameters
    home = pm.Flat('home')
    sd_att = pm.HalfStudentT('sd_att', nu=3, sigma=2.5)
    sd_def = pm.HalfStudentT('sd_def', nu=3, sigma=2.5)
    intercept = pm.Flat('intercept')

    # team-specific model parameters
    atts_star = pm.Normal("atts_star", mu=0, sigma=sd_att, shape=num_teams)
    defs_star = pm.Normal("defs_star", mu=0, sigma=sd_def, shape=num_teams)

    atts = pm.Deterministic('atts', atts_star - tt.mean(atts_star))
    defs = pm.Deterministic('defs', defs_star - tt.mean(defs_star))
    home_theta = tt.exp(intercept + home + atts[home_team] + defs[away_team])
    away_theta = tt.exp(intercept + atts[away_team] + defs[home_team])

    # likelihood of observed data
    home_points = pm.Poisson('home_points', mu=home_theta, observed=observed_home_goals)
    away_points = pm.Poisson('away_points', mu=away_theta, observed=observed_away_goals)

with model:
    trace = pm.sample(1000, tune=1000, cores=3)

pm.traceplot(trace, var_names=['intercept', 'home', 'sd_att', 'sd_def'])

bfmi = pm.bfmi(trace)
max_gr = max(np.max(gr_stats) for gr_stats in pm.gelman_rubin(trace).values())

#print(pm.stats.hpd(trace['atts']))

#print(pm.stats.quantiles(trace['atts'])[50])

df_hpd = pd.DataFrame(pm.stats.hpd(trace['atts']),
                      columns=['hpd_low', 'hpd_high'],
                      index=teams.team.values)
df_median = pd.DataFrame(pm.stats.quantiles(trace['atts'])[50],
                         columns=['hpd_median'],
                        index=teams.team.values)
df_hpd = df_hpd.join(df_median)
df_hpd['relative_lower'] = df_hpd.hpd_median - df_hpd.hpd_low
df_hpd['relative_upper'] = df_hpd.hpd_high - df_hpd.hpd_median
df_hpd = df_hpd.sort_values(by='hpd_median')
df_hpd = df_hpd.reset_index()
df_hpd['x'] = df_hpd.index + .5

df_hpd.to_csv("atts.csv")

fig, axs = plt.subplots(figsize=(10,4))
axs.errorbar(df_hpd.x, df_hpd.hpd_median,
             yerr=(df_hpd[['relative_lower', 'relative_upper']].values).T,
             fmt='o')
axs.set_title('HPD of Attack Strength, by Team')
axs.set_xlabel('Team')
axs.set_ylabel('Posterior Attack Strength')
_= axs.set_xticks(df_hpd.index + .5)
_= axs.set_xticklabels(df_hpd['index'].values, rotation=45)

df_hpd = pd.DataFrame(pm.stats.hpd(trace['defs']),
                      columns=['hpd_low', 'hpd_high'],
                      index=teams.team.values)
df_median = pd.DataFrame(pm.stats.quantiles(trace['defs'])[50],
                         columns=['hpd_median'],
                        index=teams.team.values)
df_hpd = df_hpd.join(df_median)
df_hpd['relative_lower'] = df_hpd.hpd_median - df_hpd.hpd_low
df_hpd['relative_upper'] = df_hpd.hpd_high - df_hpd.hpd_median
df_hpd = df_hpd.sort_values(by='hpd_median')
df_hpd = df_hpd.reset_index()
df_hpd['x'] = df_hpd.index + .5

df_hpd.to_csv("defs.csv")

fig, axs = plt.subplots(figsize=(10,4))
axs.errorbar(df_hpd.x, df_hpd.hpd_median,
             yerr=(df_hpd[['relative_lower', 'relative_upper']].values).T,
             fmt='o')
axs.set_title('HPD of Defense Strength, by Team')
axs.set_xlabel('Team')
axs.set_ylabel('Posterior Defense Strength')
_= axs.set_xticks(df_hpd.index + .5)
_= axs.set_xticklabels(df_hpd['index'].values, rotation=45)

#plt.show()