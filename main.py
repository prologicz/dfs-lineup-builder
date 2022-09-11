import pandas as pd
import os
from pulp import *



def lineupBuilder (thisWeeksFile):
    #Establish root directory
    ROOT_DIR = os.path.dirname(__file__)

    #Ingest and format file
    #TODO clean up file formatting
    df = pd.read_csv(os.path.join(ROOT_DIR, 'input', thisWeeksFile))
    df[['team', 'gameTime']] = df['Game Info'].str.split('@', expand=True)
    df[['opp', 'date', 'time', 'timezone']] = df['gameTime'].str.split(' ', expand=True); 
    df.set_index('Name')
    
    #Variables
    lineup = 1 #Lineup Counter
    score_check = 1000 #Initialize scoring threshold
    solutions = pd.DataFrame() #Initialize solution dataframe

    
    #LP Optimzation loop, Modify while loop between lineup or scorecheck depending on requirements
    while score_check >= 150:

        player_ids = df.index
        player_vars = LpVariable.dicts('player', player_ids, cat = 'Binary')
        prob = LpProblem ("Fantasy", LpMaximize)

        rewards = lpSum([df['AvgPointsPerGame'][i] * player_vars[i] for i in player_ids]) #Maximize Points
        prob += lpSum([df['Salary'][i] * player_vars[i] for i in player_ids]) <= 50000 # Constrained by Salary Cap
        prob += lpSum([player_vars[i] for i in player_ids]) == 9 #Constrained by 9 players

        # Constrained by teamates and/or opponents with QB
        for qbid in player_ids:
            if df['Position'][qbid] == 'QB':
                prob += lpSum([player_vars[i] for i in player_ids if (df['TeamAbbrev'][i] == df['TeamAbbrev'][qbid] and df['Position'][i] in ('WR', 'TE', 'RB'))] + [-5*player_vars[qbid]]) >= 0
                prob += lpSum([player_vars[i] for i in player_ids if (df['TeamAbbrev'][i] == df['opp'][qbid] and df['Position'][i] in ('WR'))] + [-1*player_vars[qbid]]) >= 0
     
        # Constrained by position counts including FLEX
        prob += lpSum([player_vars[i] for i in player_ids if df['Position'][i] == 'QB']) == 1
        prob += lpSum([player_vars[i] for i in player_ids if df['Position'][i] == 'DST']) == 1
        prob += lpSum([player_vars[i] for i in player_ids if df['Position'][i] == 'RB']) >= 2
        prob += lpSum([player_vars[i] for i in player_ids if df['Position'][i] == 'RB']) <= 3
        prob += lpSum([player_vars[i] for i in player_ids if df['Position'][i] == 'WR']) >= 3
        prob += lpSum([player_vars[i] for i in player_ids if df['Position'][i] == 'WR']) <= 4
        prob += lpSum([player_vars[i] for i in player_ids if df['Position'][i] == 'TE']) >= 1
        prob += lpSum([player_vars[i] for i in player_ids if df['Position'][i] == 'TE']) <= 2

        # Constrain points to last solutions's total_score - .001.  Using this to provide next best lineup instead of repeating
        prob += lpSum(rewards)
        if not lineup == 1:
            prob += lpSum(rewards) <= total_score - .001

        # Solving LP Optimzation problem
        prob.solve(PULP_CBC_CMD(msg=0))
        solution_status = LpStatus[prob.status]
        lineup_score =  value(prob.objective)

        #Return lineup solutions in dataframe
        current_lineup = []
        for v in prob.variables():
            if v.varValue != 0.0:
                if v.name.startswith('player_'):
                    current_lineup.append(df.iat[int(v.name.removeprefix('player_')), df.columns.get_loc('Name + ID')])
                else:
                    current_lineup.append(df.iat[int(v.name.removeprefix('player_')), df.columns.get_loc('Name + ID')])
        
        solutions = solutions.append({"Lineup#": lineup,'Status': solution_status, 'Score': lineup_score, 'Lineup': current_lineup}, ignore_index=True)
        

        #Update counters        
        total_score = value(prob.objective)
        lineup += 1
        score_check = total_score
        
        #Output solutions
        solutions[['player1', 'player2','player3', 'player4', 'player5','player6','player7','player8','player9']] = pd.DataFrame(solutions.Lineup.tolist())
        solutions.to_csv(os.path.join(ROOT_DIR, 'output', thisWeeksFile[:-4] + '_lineups.csv'))
        print(solutions)


lineupBuilder('DKSalaries_09112022.csv')    