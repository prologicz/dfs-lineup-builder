from xml.etree.ElementInclude import include
import pandas as pd
import os
from pulp import *
import numpy as np


def createInitialDF (thisWeeksFile):

    ROOT_DIR = os.path.dirname(__file__)

    #Ingest and format file
    #TODO clean up file formatting
    df = pd.read_csv(os.path.join(ROOT_DIR, 'input', thisWeeksFile))
    df[['Away', 'Gametime']] = df['Game Info'].str.split('@', expand=True)
    df[['Home', 'Date', 'Time', 'Timezone']] = df['Gametime'].str.split(' ', expand=True)

    conditions = [df.TeamAbbrev.eq(df.Away), df.TeamAbbrev.eq(df.Home)]
    choices = [df['Home'], df['Away']]
    df['Opponent'] = np.select(conditions, choices)
    df.set_index('Name')

    return df

def singleLineupPlayers(df, lineup_index):

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

def singleLineupScore (df, lineup_index):
    lineup = df.iloc[lineup_index]
    lineup_list = list(lineup['AvgPointsPerGame'])
    return sum(lineup_list)

def singleLineupSalary (df, lineup_index):
    lineup = df.iloc[lineup_index]
    lineup_list = list(lineup['Salary'])
    return sum(lineup_list)


def uploadInitalFile (uploadedFile):

    #Ingest and format file
    #TODO clean up file formatting

    uploadedFile[['Away', 'Gametime']] = uploadedFile['Game Info'].str.split('@', expand=True)
    uploadedFile[['Home', 'Date', 'Time', 'Timezone']] = uploadedFile['Gametime'].str.split(' ', expand=True)

    conditions = [uploadedFile.TeamAbbrev.eq(uploadedFile.Away), uploadedFile.TeamAbbrev.eq(uploadedFile.Home)]
    choices = [uploadedFile['Home'], uploadedFile['Away']]
    uploadedFile['Opponent'] = np.select(conditions, choices)
    uploadedFile.set_index('Name')

    return uploadedFile