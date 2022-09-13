import pandas as pd
import numpy as np
import os


def draftKingsSingleLineup(df, lineup_index):

    lineup = df.iloc[lineup_index]
    lineup_list = list(zip(lineup['Position'], lineup['Name + ID']))



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

    return solution_list

def draftKingsAllLineups (df, solutions_index):

    all_lineups = pd.DataFrame(columns=['QB','RB','RB','WR','WR','WR','TE','FLEX','DST'])
    for lineup_index in range(len(solutions_index)):
        current_index = solutions_index[lineup_index]
        current_lineup = draftKingsSingleLineup(df, current_index)
        all_lineups.loc[len(all_lineups)] = current_lineup
        all_lineups.reset_index

    return all_lineups



