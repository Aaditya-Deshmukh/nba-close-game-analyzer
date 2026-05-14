import os
from collections import defaultdict

import pandas as pd


DATA_DIR = "data"


#build the CSV file path using the same naming convention as data_manager.py
def get_csv_path(team_name, seasons):
    slug = team_name.split()[-1].lower()

    if len(seasons) == 1:
        season_label = str(seasons[0])
    else:
        season_label = f"{min(seasons)}-{max(seasons)}"

    return os.path.join(DATA_DIR, f"{slug}_{season_label}_games.csv")


#clean the dataframe so the columns have the right data types
def clean_games_df(df):
    if df.empty:
        return df

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["home_score"] = pd.to_numeric(df["home_score"], errors="coerce")
    df["away_score"] = pd.to_numeric(df["away_score"], errors="coerce")
    df["point_diff"] = pd.to_numeric(df["point_diff"], errors="coerce")

    #CSV files may store True/False as text, so convert it back to boolean
    if df["team_won"].dtype == "object":
        df["team_won"] = df["team_won"].astype(str).str.lower() == "true"

    return df


#load a team's close game CSV into a pandas dataframe
def load_team_csv(team_name, seasons):
    path = get_csv_path(team_name, seasons)

    #return None if the CSV is not already preloaded
    if not os.path.exists(path):
        return None

    df = pd.read_csv(path)
    return clean_games_df(df)


#convert fetched list of dictionaries into a pandas dataframe
def games_to_df(games):
    df = pd.DataFrame(games)
    return clean_games_df(df)


#get summary of wins losses and win percentage
def summarize_team_games(df):
    total = len(df)

    if total == 0:
        return {
            "total": 0,
            "wins": 0,
            "losses": 0,
            "win_pct": 0
        }

    wins = int(df["team_won"].sum())
    losses = total - wins
    win_pct = round((wins / total) * 100, 1)

    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "win_pct": win_pct
    }


#compare the close game stats for two teams
def compare_teams(team1_games, team2_games):
    return {
        "team1": summarize_team_games(team1_games),
        "team2": summarize_team_games(team2_games)
    }


#get the season that the game was from for labeling
def get_game_season(date_value):
    """
    Converts the game date into the NBA season.

    Example:
    2023-10-26 -> 2023 season
    2024-02-10 -> 2023 season
    """
    if pd.isna(date_value):
        return "Unknown"

    year = date_value.year
    month = date_value.month

    #nba season starts around october
    return year if month >= 10 else year - 1


#group and summarize the close games by season
def summarize_by_season(df):
    if df.empty:
        return []

    df = df.copy()
    df["season"] = df["date"].apply(get_game_season)

    #remove rows with invalid dates so the season chart only uses real seasons
    df = df[df["season"] != "Unknown"]

    if df.empty:
        return []

    summary = (
        df.groupby("season")
        .agg(
            total=("team_won", "count"),
            wins=("team_won", "sum")
        )
        .reset_index()
    )

    summary["wins"] = summary["wins"].astype(int)
    summary["losses"] = summary["total"] - summary["wins"]
    summary["win_pct"] = round((summary["wins"] / summary["total"]) * 100, 1)

    return summary.sort_values("season").to_dict("records")


#format each close game by season for the app display
def format_close_games_by_season(df, team_name):
    if df.empty:
        return {}

    df = df.copy()
    df["season"] = df["date"].apply(get_game_season)

    games_by_season = defaultdict(list)

    for _, game in df.iterrows():
        season = game["season"]

        home_team = game["home_team"]
        away_team = game["away_team"]
        home_score = game["home_score"]
        away_score = game["away_score"]

        if team_name == home_team:
            opponent = away_team
            team_score = home_score
            opponent_score = away_score
        elif team_name == away_team:
            opponent = home_team
            team_score = away_score
            opponent_score = home_score
        else:
            opponent = "Unknown Opponent"
            team_score = None
            opponent_score = None

        margin = game["point_diff"]

        game_info = {
            "date": game["date"].strftime("%Y-%m-%d") if pd.notna(game["date"]) else "Unknown Date",
            "opponent": opponent,
            "team_score": int(team_score) if pd.notna(team_score) else None,
            "opponent_score": int(opponent_score) if pd.notna(opponent_score) else None,
            "final_score": f"{int(team_score)}-{int(opponent_score)}"
            if pd.notna(team_score) and pd.notna(opponent_score)
            else "N/A",
            "result": "Win" if game["team_won"] else "Loss",
            "margin": int(margin) if pd.notna(margin) else "N/A"
        }

        games_by_season[season].append(game_info)

    return dict(sorted(games_by_season.items()))