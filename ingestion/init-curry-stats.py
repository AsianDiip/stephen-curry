"""
Pandas Webscraper

Data is Taken from Basketball Reference

Data includes all regular season game during Curry's Career from the 2013-2014 season to the 2024-2025 season
INCLUDING games where he did not dress or play, and therefore will match up with the number of regular season games
that the GSW have played in those seasons
"""
import pandas as pd
import time
from pathlib import Path

data_dir = Path(__file__).parent.parent / 'data' / 'raw' / 'nba'
data_file = data_dir / 'curry_13_14_24_25.parquet'
url = 'https://www.basketball-reference.com/players/c/curryst01/gamelog/2014'
dfs = pd.read_html(url)
raw_curry_games = dfs[7]
raw_curry_games = raw_curry_games[raw_curry_games['Rk'] != 'Rk'].reset_index()
raw_curry_games = raw_curry_games.drop(['index', 'Unnamed: 5'], axis=1)
time.sleep(2)

for year in range(2015, 2026):
    year_url = f'https://www.basketball-reference.com/players/c/curryst01/gamelog/{year}'
    dfs = pd.read_html(year_url)
    unclean = dfs[7]
    clean = unclean[unclean['Rk'] != 'Rk'].reset_index().drop(['index', 'Unnamed: 5'], axis=1)
    raw_curry_games = pd.concat([raw_curry_games, clean], axis=0, ignore_index=True)
    time.sleep(2)

curry_games = raw_curry_games[raw_curry_games['Rk'].notna()].reset_index().drop('index', axis = 1)


data_dir.mkdir(parents = True, exist_ok = True)

curry_games.to_parquet(data_file)
