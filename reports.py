from support_functions import *
import pandas as pd



def draftKingsAllLineups (df, solutions_index):

    all_lineups = pd.DataFrame(columns=['QB','RB','RB','WR','WR','WR','TE','FLEX','DST'])
    for lineup_index in range(len(solutions_index)):
        current_index = solutions_index[lineup_index]
        current_lineup = singleLineupPlayers(df, current_index)
        all_lineups.loc[len(all_lineups)] = current_lineup
        all_lineups.reset_index

    return all_lineups

def usagePercentage (df, index):
    lineups = draftKingsAllLineups(df, index)
    lineupCount= len(index)
    usagePercent = lineups.melt(var_name='columns', value_name='player')
    usagePercent = pd.crosstab(index=usagePercent['player'], columns=usagePercent['columns'])
    usagePercent['counts'] = usagePercent.sum(axis=1)
    usagePercent['percent of lineups'] = (usagePercent['counts'] / lineupCount)
    usagePercent = usagePercent.drop(columns = ['DST','FLEX','QB','RB','WR','TE','counts'])
    print(usagePercent)
    return usagePercent



