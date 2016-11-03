#STAN model of 2015-16 Premiership season

Quick and dirty STAN model of the match results. Each team is given a ranking based on where they finished in the 2014-15 season, and then each match is modelled based on that rank and a Student-t distribution for the goals scored. This gives a "ranking" of team performance that year. This model is very simple, ignores lots of stuff, but it generally agrees with how I feel the teams performed last season - so that's nice.

![Rankings](https://github.com/neal-o-r/pl_stan/blob/master/rank.png)
