import time
import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

PLAYER_NAME = "Stephen Curry"
START_YEAR = 2009
END_YEAR = 2025
SLEEP_SECONDS = 1.2

def generate_seasons(start_year, end_year):
    return [f"{y}-{str(y + 1)[-2:]}" for y in range(start_year, end_year)]

def parse_minutes(column):
    if pd.isna(column):
        return None
    if isinstance(column, (int, float)):
        return float(column)
    if isinstance(column, str):
        print("OOGA BOOGA")

player_info = players.find_players_by_full_name(PLAYER_NAME)
curry_id = player_info[0]["id"]

seasons = generate_seasons(START_YEAR, END_YEAR)

all_games = []

# Start loop to go through all seasons and get the curry stats for those regular season games
for season in seasons:
    print(f"Fetching season {season}")

    try:
        gamelog = playergamelog.PlayerGameLog(
            player_id = curry_id,
            season = season,
            season_type_all_star = "Regular Season"
        )

        df = gamelog.get_data_frames()[0]

        if df.empty:
            continue
        
#Normalize the column schema
        df = df.rename(columns={
            "GAME_ID": "game_id",
            "GAME_DATE": "game_date",
            "MATCHUP": "matchup",
            "WL": "team_result",
            "MIN": "minutes",
            "FGM": "fgm",
            "FGA": "fga",
            "FG3M": "three_pm",
            "FG3A": "three_pa",
            "FTM": "ftm",
            "FTA": "fta",
            "REB": "reb",
            "AST": "ast",
            "STL": "stl",
            "BLK": "blk",
            "TO": "tov",
            "PF": "pf",
            "PTS": "pts",
            "PLUS_MINUS": "plus_minus"
        })

        df["minutes"] = df["minutes"].apply(parse_minutes)
        

        df["is_home_game"] = ~df["matchup"].str.contains("@")
        df["opponent_id"] = df["matchup"].str.split().str[-1]
        df["season"] = season
        df["player_id"] = curry_id
        df["player_name"] = PLAYER_NAME

        # Select canonical columns
        df = df[
            [
                "game_id",
                "game_date",
                "season",
                "player_id",
                "player_name",
                "minutes",
                "fgm",
                "fga",
                "three_pm",
                "three_pa",
                "ftm",
                "fta",
                "pts",
                "reb",
                "ast",
                "stl",
                "blk",
                "tov",
                "pf",
                "plus_minus",
                "is_home_game",
                "opponent_id",
                "team_result",
            ]
        ]

        all_games.append(df)

        time.sleep(SLEEP_SECONDS)

    except Exception as e:
        print(f"Failed season {season}: {e}")


# Combine all the seasons
career_df = pd.concat(all_games, ignore_index=True)

#Normalize/Convert all date data
career_df["game_date"] = pd.to_datetime(career_df["game_date"])

#Sort by time
career_df = career_df.sort_values("game_date")

#Make sure games are unique
career_df = career_df.drop_duplicates(
    subset=["player_id", "game_date"]
)
career_df = career_df.reset_index(drop=True)


career_df.to_parquet(
    "data/raw/nba/stephen_curry_games.parquet",
    index = False
)
