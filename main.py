import pandas as pd
import os
from pulp import *



def lineupBuilder (thisWeeksFile):
    ROOT_DIR = os.path.dirname(__file__)
    thisWeeksFile

    df = pd.read_csv(os.path.join(ROOT_DIR, thisWeeksFile))
    df[['team', 'gameTime']] = df['Game Info'].str.split('@', expand=True)
    df[['opp', 'date', 'time', 'timezone']] = df['gameTime'].str.split(' ', expand=True); 


    salaries = {}
    scores = {}

    for pos in df.Position.unique():
        available_pos = df[df.Position == pos]
        salary = list(available_pos [['Name + ID', 'Salary']].set_index('Name + ID').to_dict().values())[0]
        score = list(available_pos [['Name + ID', 'AvgPointsPerGame']].set_index('Name + ID').to_dict().values())[0]
        
        salaries[pos] = salary
        scores[pos] = score


    pos_num_available = {
        "QB": 1,
        "RB": 2,
        "WR": 3,
        "TE": 1,
        "FLEX" : 1,
        "DST" : 1
    }

    flexible_positions = ("RB", "WR", "TE")

    SALARY_CAP = 50000

    lineup = 1
    score_check = 1000
    solutions = pd.DataFrame()
    while lineup <= 50:

        _vars = {k: LpVariable.dict(k, v, cat='Binary') for k , v in scores.items()}

        prob = LpProblem ("Fantasy", LpMaximize)
        rewards = []
        costs = []
        position_constraints = []

        for k, v in _vars.items():
            costs += lpSum([salaries[k][i] * _vars[k][i] for i in v])
            rewards += lpSum ([scores[k][i] * _vars[k][i] for i in v])
                    
            if k not in flexible_positions:
                prob += lpSum ([_vars[k][i] for i in v]) == pos_num_available[k]
            else:
                prob += lpSum ([_vars[k][i] for i in v]) >= pos_num_available[k]
                prob += lpSum ([_vars[k][i] for i in v]) <= pos_num_available[k] + pos_num_available['FLEX']

            position_constraints += lpSum([_vars[k][i] for i in v])


        prob += lpSum(position_constraints) == 9
        prob += lpSum(rewards)
        prob +=lpSum(costs) <= SALARY_CAP
        if not lineup == 1:
            prob += lpSum(rewards) <= total_score - .001
        prob.solve(PULP_CBC_CMD(msg=0))


        solution_status = LpStatus[prob.status]
        lineup_score =  value(prob.objective)
        current_lineup = []
        for v in prob.variables():
            if v.varValue != 0.0:
                if v.name.startswith('QB_'):
                    current_lineup.append(v.name.removeprefix('QB_'))
                elif v.name.startswith('RB_'):
                    current_lineup.append(v.name.removeprefix('RB_'))
                elif v.name.startswith('WR_'):
                    current_lineup.append(v.name.removeprefix('WR_'))
                elif v.name.startswith('TE_'):
                    current_lineup.append(v.name.removeprefix('TE_'))
                elif v.name.startswith('Def_'):
                    current_lineup.append(v.name.removeprefix('Def_'))
                else:
                    current_lineup.append(v.name)
        
        solutions = solutions.append({"Lineup#": lineup,'Status': solution_status, 'Score': lineup_score, 'Lineup': current_lineup}, ignore_index=True)
        

                
        total_score = value(prob.objective)
        lineup += 1
        score_check = total_score
        

        solutions[['player1', 'player2','player3', 'player4', 'player5','player6','player7','player8','player9']] = pd.DataFrame(solutions.Lineup.tolist())
        solutions.to_csv(thisWeeksFile + '_lineups.csv')
        print(solutions)


lineupBuilder('DKSalaries_09112022.csv')    