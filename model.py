import pandas as pd
import pystan as pys
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

games = pd.read_csv('2015-16.csv')
teams = pd.read_csv('rankings.csv')

stan_code="""
data {
  int nteams;
  int ngames;
  vector[nteams] prior;
  int team1[ngames];
  int team2[ngames];
  vector[ngames] score1;
  vector[ngames] score2;
  real df;
}
transformed data {
  vector[ngames] dif;
  dif <- score1 - score2;
}
parameters {
  real b;
  real sigma_a;
  real sigma_y;
  vector[nteams] eta_a;
}
transformed parameters {
  vector[nteams] a;
  a <- b*prior + sigma_a*eta_a;
}  
model {
  eta_a ~ normal(0,1);
  for (i in 1:ngames)
    dif[i] ~ student_t(df, a[team1[i]]-a[team2[i]], sigma_y);
}
"""

names = list(set(games.Home))
map_names = lambda x: teams[teams.Team == x].index[0]+1


games['HNo'] = games.Home.apply(map_names)
games['ANo'] = games.Away.apply(map_names)

prior_score = range(1, 21)[::-1]
prior = (prior_score - np.mean(prior_score))/(2*np.std(prior_score))

data = {
        'nteams': len(set(games.Home)),
        'ngames': len(games),
        'prior' : prior, 
        'score1': games.HScore.values,
        'score2': games.AScore.values,
        'team1' : games.HNo.values,
        'team2' : games.ANo.values,
        'df'    : 7.
}

fit = pys.stan(model_code=stan_code, data=data, iter=2000, chains=2)
results = fit.extract() 


