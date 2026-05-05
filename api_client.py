import datetime
import os
import requests
from dotenv import load_dotenv

# Load BALLDONTLIE_API_KEY from the .env file into the environment
load_dotenv()

BASE_URL = "https://api.balldontlie.io/v1"


def _headers():
    # The BallDontLie API requires the key in the Authorization header
    api_key = os.getenv("BALLDONTLIE_API_KEY")
    if not api_key:
        raise ValueError(
            "BALLDONTLIE_API_KEY not found. Set it in a .env file or as an environment variable."
        )
    return {"Authorization": api_key}


def get_recent_seasons(seasons_back):
    """
    Return a list of season years for the last `seasons_back` seasons.

    In the BallDontLie API, a season is identified by the year it started.
    For example, the 2023-24 season is season 2023.
    The most recently completed season is assumed to be (current year - 1).

    Examples:
        get_recent_seasons(1)  ->  [2024]
        get_recent_seasons(3)  ->  [2022, 2023, 2024]
        get_recent_seasons(10) ->  [2015, 2016, ..., 2024]
    """
    # Subtract 1 because the current calendar year's season is still in progress
    most_recent = datetime.date.today().year - 1
    return list(range(most_recent - seasons_back + 1, most_recent + 1))


def get_all_teams():
    """
    Return a list of all 30 NBA teams from the API.
    Each team is a dict with keys: id, full_name, abbreviation, city, name, conference, division.
    Used to populate the GUI dropdowns.
    """
    resp = requests.get(
        f"{BASE_URL}/teams",
        headers=_headers(),
        params={"per_page": 100},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["data"]


def get_team_id(team_name):
    """
    Return the team dict for the first team whose full name contains team_name (case-insensitive).
    Raises ValueError if no match is found.

    Example:
        get_team_id("Lakers") -> {"id": 14, "full_name": "Los Angeles Lakers", ...}
    """
    teams = get_all_teams()
    # Search through all teams for a case-insensitive substring match
    team = next((t for t in teams if team_name.lower() in t["full_name"].lower()), None)
    if team is None:
        raise ValueError(f"No team found matching '{team_name}'")
    return team


def get_games_for_team(team_id, seasons):
    """
    Fetch every game for a team across the given list of seasons.

    The API returns at most 100 games per response, so this function loops
    using cursor-based pagination until all pages are collected.

    Args:
        team_id: the integer ID of the team (from get_team_id)
        seasons:  list of season-start years, e.g. [2022, 2023, 2024]

    Returns:
        Flat list of raw game dicts from the BallDontLie API.
    """
    params = {
        "per_page": 100,       # maximum allowed per request
        "team_ids[]": team_id,
        "seasons[]": seasons,
    }

    all_games = []
    cursor = None

    while True:
        # Add cursor to params on every page after the first
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

        # next_cursor is None when we've reached the last page
        cursor = payload.get("meta", {}).get("next_cursor")
        if cursor is None:
            break

    return all_games


def filter_close_games(games, team_id, max_diff=5):
    """
    Filter a list of raw API games down to only close finishes.

    A game is considered "close" if the final score difference is <= max_diff points.
    Games with missing scores (e.g. future/postponed games) are skipped.

    Args:
        games:    list of raw game dicts from get_games_for_team
        team_id:  the team we're tracking wins/losses for
        max_diff: maximum point difference to be considered a close game (default 5)

    Returns:
        List of simplified game dicts with keys:
            date, home_team, away_team, home_score, away_score, point_diff, team_won
    """
    close = []
    for game in games:
        home_score = game.get("home_team_score")
        away_score = game.get("visitor_team_score")

        # Skip games that haven't been played yet
        if home_score is None or away_score is None:
            continue

        diff = abs(home_score - away_score)
        if diff > max_diff:
            continue

        # Determine if our team won:
        # Win if we're home and scored more, or we're away and scored more
        home_id = game["home_team"]["id"]
        team_won = (
            (home_score > away_score and home_id == team_id)
            or (away_score > home_score and home_id != team_id)
        )

        close.append(
            {
                "date": game["date"][:10],  # trim timestamp, keep YYYY-MM-DD
                "home_team": game["home_team"]["full_name"],
                "away_team": game["visitor_team"]["full_name"],
                "home_score": home_score,
                "away_score": away_score,
                "point_diff": diff,
                "team_won": team_won,
            }
        )

    return close
