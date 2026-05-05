import csv
import os

from api_client import filter_close_games, get_games_for_team

DATA_DIR = "data"
COLUMNS = ["date", "home_team", "away_team", "home_score", "away_score", "point_diff", "team_won"]


def _csv_path(team_name):
    # Use only the last word of the team name (e.g. "Los Angeles Lakers" -> "lakers_games.csv")
    slug = team_name.split()[-1].lower()
    return os.path.join(DATA_DIR, f"{slug}_games.csv")


def save_close_games(team_name, close_games):
    """Write close_games list to a CSV file under data/."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = _csv_path(team_name)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(close_games)
    return path


def load_close_games(team_name):
    """Read close games from the cached CSV. Returns None if file doesn't exist."""
    path = _csv_path(team_name)
    if not os.path.exists(path):
        return None
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        games = []
        for row in reader:
            row["home_score"] = int(row["home_score"])
            row["away_score"] = int(row["away_score"])
            row["point_diff"] = int(row["point_diff"])
            row["team_won"] = row["team_won"] == "True"
            games.append(row)
    return games


def fetch_and_cache(team_id, team_name, seasons=None, force_refresh=False):
    """
    Return close games for a team, using the cached CSV when available.

    Set force_refresh=True to re-fetch from the API even if a cache exists.
    """
    if not force_refresh:
        cached = load_close_games(team_name)
        if cached is not None:
            return cached

    raw_games = get_games_for_team(team_id, seasons=seasons)
    close_games = filter_close_games(raw_games, team_id)
    save_close_games(team_name, close_games)
    return close_games