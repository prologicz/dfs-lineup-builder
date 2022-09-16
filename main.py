from support_functions import *
from linuep_builder import *
from reports import *
import pandas as pd
import datetime


currentWeek = 1

df = createInitialDF('DKSalaries.csv')
solutions = lineupBuilder(df) 
lineups_file = draftKingsAllLineups(df, solutions)
lineup_percentages = usagePercentage(df, solutions)
lineup_summary = summaryReport(df,solutions)



ROOT_DIR = os.path.dirname(__file__)
timestamp = str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
lineups_file.to_csv(os.path.join(ROOT_DIR, 'output', 'DK_Week' + str(currentWeek) + '_Lineups_' + timestamp + '.csv'), index=False)
lineup_percentages.to_csv(os.path.join(ROOT_DIR, 'output', 'DK_Week' + str(currentWeek) + '_Percentages_' + timestamp + '.csv'), index=True)
lineup_summary.to_csv(os.path.join(ROOT_DIR, 'output', 'DK_Week' + str(currentWeek) + '_Summary_' + timestamp + '.csv'), index=True)
