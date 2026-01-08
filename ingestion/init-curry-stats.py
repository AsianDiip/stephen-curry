#This is all curry box scores from regular season games (DOES NOT INCLUDE EMIRATES CUP)
# before 2026-01-07 (YYYY-MM-DD) (script was initially ran on 1-07-2026)

#/eoinamoore/historical-nba-data-and-player-box-scores?select=PlayerStatistics.csv

import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
import tempfile

DATASET = "eoinamoore/historical-nba-data-and-player-box-scores"
CSV_FILE = "PlayerStatistics.csv"
DEST_DIR = "data/raw/nba"
OUTPUT_FILE = os.path.join(DEST_DIR, "Stephen_Curry_Stats_Init.csv")
PLAYER_NAME = "Stephen Curry"

os.makedirs(DEST_DIR, exist_ok = True)

api = KaggleApi()
api.authenticate()

def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = os.path.join(tmpdir, CSV_FILE)
        api.dataset_download_file(
            dataset = DATASET,
            file_name = CSV_FILE, 
            path = tmpdir,
            force = True
        )

        curry_rows = []
        for chunk in pd.read_csv(temp_path, chunksize = 100000):
            curry_chunk = chunk[
                (chunk['firstName'] == 'Stephen') &
                (chunk['lastName'] == 'Curry')
            ]
            if not curry_chunk.empty:
                curry_chunk['gameDateTimeEst'] = pd.to_datetime(curry_chunk['gameDateTimeEst'])

                mask = (
                    (curry_chunk['gameType'] == 'Regular Season') &
                    (curry_chunk['gameDateTimeEst'] >= '2015-07-01') &
                    (curry_chunk['gameDateTimeEst'] <= '2025-07-01')
                )

                curry_chunk = curry_chunk[mask]

                if not curry_chunk.empty:
                    curry_rows.append(curry_chunk)

        if curry_rows:
            curry_stats = pd.concat(curry_rows, ignore_index = True)
            curry_stats.to_csv(OUTPUT_FILE, index = False)
        else:
            print("Curry rows empty")

main()

