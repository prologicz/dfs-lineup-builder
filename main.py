import pandas as pd
import os

ROOT_DIR = os.path.dirname(__file__)
thisWeeksFile = 'DKSalaries_09112022.csv'

df = pd.read_csv(os.path.join(ROOT_DIR, thisWeeksFile))
df[['team', 'gameTime']] = df['Game Info'].str.split('@', expand=True)
df[['opp', 'date', 'time', 'timezone']] = df['gameTime'].str.split(' ', expand=True); 


print(df)
