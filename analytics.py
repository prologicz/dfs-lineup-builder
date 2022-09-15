from support_functions import *
import pandas as pd

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



