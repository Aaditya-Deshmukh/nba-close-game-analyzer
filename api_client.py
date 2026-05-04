import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.balldontlie.io/v1"


def _headers():
    api_key = os.getenv("BALLDONTLIE_API_KEY")
    if not api_key:
        raise ValueError(
            "BALLDONTLIE_API_KEY not found. Set it in a .env file or as an environment variable."
        )
    return {"Authorization": api_key}


def get_all_teams():
    """Return a list of all NBA teams."""
    resp = requests.get(
        f"{BASE_URL}/teams",
        headers=_headers(),
        params={"per_page": 100},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["data"]


def get_team_id(team_name):
    """Return the team dict for the first team whose full name contains team_name."""
    teams = get_all_teams()
    team = next((t for t in teams if team_name.lower() in t["full_name"].lower()), None)
    if team is None:
        raise ValueError(f"No team found matching '{team_name}'")
    return team


def get_games_for_team(team_id, seasons=None):
    """
    Fetch all games for a given team ID across the specified seasons.

    seasons: list of ints, e.g. [2022, 2023]. Defaults to last 5 seasons if None.
    Returns a flat list of game dicts from the BallDontLie API.
    """
    if seasons is None:
        current_year = datetime.date.today().year
        seasons = list(range(current_year - 4, current_year + 1))

    params = {
        "per_page": 100,
        "team_ids[]": team_id,
        "seasons[]": seasons,
    }

    all_games = []
    cursor = None

    while True:
        if cursor is not None:
            params["cursor"] = cursor

        resp = requests.get(
            f"{BASE_URL}/games",
            headers=_headers(),
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        payload = resp.json()

        all_games.extend(payload["data"])

        cursor = payload.get("meta", {}).get("next_cursor")
        if cursor is None:
            break

    return all_games


def filter_close_games(games, team_id, max_diff=5):
    """
    Filter games to only those decided by max_diff points or fewer.

    Returns a list of dicts with normalized fields:
        date, home_team, away_team, home_score, away_score,
        point_diff, team_won (bool for whether team_id won)
    """
    close = []
    for game in games:
        home_score = game.get("home_team_score")
        away_score = game.get("visitor_team_score")

        if home_score is None or away_score is None:
            continue

        diff = abs(home_score - away_score)
        if diff > max_diff:
            continue

        home_id = game["home_team"]["id"]
        team_won = (
            (home_score > away_score and home_id == team_id)
            or (away_score > home_score and home_id != team_id)
        )

        close.append(
            {
                "date": game["date"][:10],
                "home_team": game["home_team"]["full_name"],
                "away_team": game["visitor_team"]["full_name"],
                "home_score": home_score,
                "away_score": away_score,
                "point_diff": diff,
                "team_won": team_won,
            }
        )

    return close