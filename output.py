import pandas as pd
import numpy as np
import os


def draftKingsOutput(df, lineup_index):

    lineup = df.iloc[lineup_index]
    lineup_list = list(zip(lineup['Position'], lineup['Name + ID']))


    solution_df = pd.DataFrame(columns=['QB','RB','RB','WR','WR','WR','TE','FLEX','DST'])
    solution_list = [0,0,0,0,0,0,0,0,0]
    

    for player in range(len(lineup_list)):
        if lineup_list[player][0] == 'QB' and solution_list[0] == 0:
            solution_list[0]= lineup_list[player][1]
        elif lineup_list[player][0] == 'QB' and solution_list[0] != 0:
            solution_list = [0,0,0,0,0,0,0,0,0]
            print('Position Count Mismatch.  Extra QB')

        elif lineup_list[player][0] == 'RB' and solution_list[1] == 0 and solution_list[2] == 0:
            solution_list[1]= lineup_list[player][1]
        elif lineup_list[player][0] == 'RB' and solution_list[1] != 0 and solution_list[2] == 0:
            solution_list[2]= lineup_list[player][1]
        elif lineup_list[player][0] == 'RB' and solution_list[1] != 0 and solution_list[2] != 0 and solution_list[7] == 0:
            solution_list[7]= lineup_list[player][1]
        elif lineup_list[player][0] == 'RB' and solution_list[1] != 0 and solution_list[2] != 0 and solution_list[7] != 0:
            solution_list = [0,0,0,0,0,0,0,0,0]
            print('Position Count Mismatch.  Extra RB')
        
        elif lineup_list[player][0] == 'WR' and solution_list[3] == 0 and solution_list[4] == 0 and solution_list[5] == 0:
            solution_list[3]= lineup_list[player][1]
        elif lineup_list[player][0] == 'WR' and solution_list[3] != 0 and solution_list[4] == 0 and solution_list[5] == 0:
            solution_list[4]= lineup_list[player][1]
        elif lineup_list[player][0] == 'WR' and solution_list[3] != 0 and solution_list[4] != 0 and solution_list[5] == 0:
            solution_list[5]= lineup_list[player][1]
        elif lineup_list[player][0] == 'WR' and solution_list[3] != 0 and solution_list[4] != 0 and solution_list[5] != 0 and solution_list[7] == 0:
            solution_list[7]= lineup_list[player][1]
        elif lineup_list[player][0] == 'WR' and solution_list[3] != 0 and solution_list[4] != 0 and solution_list[5] != 0 and solution_list[7] != 0:
            solution_list = [0,0,0,0,0,0,0,0,0]
            print('Position Count Mismatch.  Extra WR')

        elif lineup_list[player][0] == 'TE' and solution_list[6] == 0:
            solution_list[6]= lineup_list[player][1]
        elif lineup_list[player][0] == 'TE' and solution_list[6] != 0 and solution_list[7] == 0:
            solution_list[7]= lineup_list[player][1]
        elif lineup_list[player][0] == 'TE' and solution_list[6] != 0 and solution_list[7] != 0:
            solution_list = [0,0,0,0,0,0,0,0,0]
            print('Position Count Mismatch.  Extra TE')


        elif lineup_list[player][0] == 'DST' and solution_list[8] == 0:
            solution_list[8]= lineup_list[player][1]
        elif lineup_list[player][0] == 'DST' and solution_list[8] != 0:
            solution_list = [0,0,0,0,0,0,0,0,0]
            print('Position Count Mismatch.  Extra DST')

    solution_df.loc[len(solution_df)] = solution_list
    solution_df.reset_index
    print(solution_df)
    solution_df.to_csv('test.csv', index=False)






ROOT_DIR = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(ROOT_DIR, 'input', 'DKSalaries.csv'))
df[['away', 'gametime']] = df['Game Info'].str.split('@', expand=True)
df[['home', 'date', 'time', 'timezone']] = df['gametime'].str.split(' ', expand=True);

conditions = [df.TeamAbbrev.eq(df.away), df.TeamAbbrev.eq(df.home)]
choices = [df['home'], df['away']]
df['opponent'] = np.select(conditions, choices)
df.set_index('Name')




lineup_index = [0, 10, 129, 163, 18, 28, 543, 79, 207]
draftKingsOutput(df,lineup_index)


