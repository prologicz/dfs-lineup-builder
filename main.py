import pandas as pd
import os
from pulp import *



def lineupBuilder (thisWeeksFile):
    ROOT_DIR = os.path.dirname(__file__)

    
    df = pd.read_csv(os.path.join(ROOT_DIR, 'input', thisWeeksFile))
    df[['team', 'gameTime']] = df['Game Info'].str.split('@', expand=True)
    df[['opp', 'date', 'time', 'timezone']] = df['gameTime'].str.split(' ', expand=True); 
    df.set_index('Name')
    
    


    # salaries = {}
    # scores = {}
  
    # for pos in df.Position.unique():
    #     available_pos = df[df.Position == pos]
    #     salary = list(available_pos [['Name + ID', 'Salary']].set_index('Name + ID').to_dict().values())[0]
    #     score = list(available_pos [['Name + ID', 'AvgPointsPerGame']].set_index('Name + ID').to_dict().values())[0]

    #     salaries[pos] = salary
    #     scores[pos] = score


    # pos_num_available = {
    #     "QB": 1,
    #     "RB": 2,
    #     "WR": 3,
    #     "TE": 1,
    #     "FLEX" : 1,
    #     "DST" : 1
    # }

    # flexible_positions = ("RB", "WR", "TE")

    # SALARY_CAP = 50000

    lineup = 1
    score_check = 1000
    solutions = pd.DataFrame()
    #while lineup <= 50:


    player_ids = df.index
    print(player_ids)
    player_vars = LpVariable.dicts('player', player_ids, cat = 'Binary')

    prob = LpProblem ("Fantasy", LpMaximize)


    prob += lpSum([df['AvgPointsPerGame'][i] * player_vars[i] for i in player_ids])
    prob += lpSum([df['Salary'][i] * player_vars[i] for i in player_ids]) <= 50000
    prob += lpSum([player_vars[i] for i in player_ids]) == 9

    prob.solve(PULP_CBC_CMD(msg=0))


    solution_status = LpStatus[prob.status]
    lineup_score =  value(prob.objective)
    current_lineup = []
    for v in prob.variables():
        if v.varValue != 0.0:
            if v.name.startswith('player_'):
                current_lineup.append(df.iat[int(v.name.removeprefix('player_')), df.columns.get_loc('Name + ID')])
            else:
                current_lineup.append(df.iat[int(v.name.removeprefix('player_')), df.columns.get_loc('Name + ID')])
    
    solutions = solutions.append({"Lineup#": lineup,'Status': solution_status, 'Score': lineup_score, 'Lineup': current_lineup}, ignore_index=True)
    

            
    total_score = value(prob.objective)
    lineup += 1
    score_check = total_score
    

    solutions[['player1', 'player2','player3', 'player4', 'player5','player6','player7','player8','player9']] = pd.DataFrame(solutions.Lineup.tolist())
    solutions.to_csv(os.path.join(ROOT_DIR, 'output', thisWeeksFile[:-4] + '_lineups.csv'))
    print(solutions)


lineupBuilder('DKSalaries_09112022.csv')    