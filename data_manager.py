import csv
import os
import time

from api_client import filter_close_games, get_all_teams, get_games_for_team, get_recent_seasons

DATA_DIR = "data"
COLUMNS = ["date", "home_team", "away_team", "home_score", "away_score", "point_diff", "team_won"]


def _csv_path(team_name, seasons):
    """
    Build the CSV file path for a team + season range.

    The season range is encoded in the filename so that different season
    selections are cached separately. For example:
        seasons=[2024]           ->  data/lakers_2024_games.csv
        seasons=[2020,2021,...,2024] ->  data/lakers_2020-2024_games.csv
    """
    slug = team_name.split()[-1].lower()  # "Los Angeles Lakers" -> "lakers"

    # Encode the season range as either a single year or a "start-end" range
    if len(seasons) == 1:
        season_label = str(seasons[0])
    else:
        season_label = f"{min(seasons)}-{max(seasons)}"

    return os.path.join(DATA_DIR, f"{slug}_{season_label}_games.csv")

def save_team_id(data):
    with open('data/team_id', 'w') as f:
        f.write(data)

    return 


def save_close_games(team_name, seasons, close_games):
    """
    Write close_games to a CSV file under data/.
    Creates the data/ directory if it doesn't exist.
    Returns the path of the file written.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    path = _csv_path(team_name, seasons)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(close_games)
    return path


def load_close_games(team_name, seasons):
    """
    Read close games from the cached CSV for this team + season range.
    Returns None if no cache file exists yet.

    CSV stores everything as strings, so numeric and boolean fields
    are converted back to their correct types on load.
    """
    path = _csv_path(team_name, seasons)
    if not os.path.exists(path):
        return None

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        games = []
        for row in reader:
            # Restore types that CSV serializes as plain strings
            row["home_score"] = int(row["home_score"])
            row["away_score"] = int(row["away_score"])
            row["point_diff"] = int(row["point_diff"])
            row["team_won"] = row["team_won"] == "True"
            games.append(row)

    return games


def fetch_and_cache(team_id, team_name, seasons_back=5, force_refresh=False):
    """
    Return close games for a team, loading from CSV cache when available.

    Args:
        team_id:       integer team ID from the API
        team_name:     full team name, e.g. "Los Angeles Lakers"
        seasons_back:  how many past seasons to include (default 5)
                       e.g. seasons_back=1 -> last season only
                            seasons_back=10 -> last 10 seasons
        force_refresh: set True to ignore the cache and re-fetch from the API

    Returns:
        List of close game dicts (same structure as filter_close_games output).
    """
    seasons = get_recent_seasons(seasons_back)

    # Return cached data if it exists and a refresh wasn't requested
    if not force_refresh:
        cached = load_close_games(team_name, seasons)
        if cached is not None:
            return cached

    # Cache miss — fetch from API, filter, save, then return
    raw_games = get_games_for_team(team_id, seasons)
    close_games = filter_close_games(raw_games, team_id)
    save_close_games(team_name, seasons, close_games)
    return close_games


def warm_cache_all_teams(seasons_back=3, delay=2):
    """
    Pre-fetch and cache close game data for all 30 NBA teams.

    Run this once before starting the app. After it completes, every
    request reads from CSV with no API calls needed.

    Args:
        seasons_back: how many past seasons to fetch per team (default 3)
        delay:        seconds to wait between each team to avoid rate limiting (default 2)
    """
    teams = get_all_teams()
    total = len(teams)

    for i, team in enumerate(teams, start=1):
        name = team["full_name"]
        seasons = get_recent_seasons(seasons_back)

        # Skip teams that are already cached for this season range
        if load_close_games(name, seasons) is not None:
            print(f"[{i}/{total}] {name} — already cached, skipping")
            continue

        print(f"[{i}/{total}] {name} — fetching...", end=" ", flush=True)
        raw_games = get_games_for_team(team["id"], seasons)
        close_games = filter_close_games(raw_games, team["id"])
        save_close_games(name, seasons, close_games)
        print(f"{len(close_games)} close games saved")

        # Pause between teams to stay under the API rate limit
        if i < total:
            time.sleep(delay)
