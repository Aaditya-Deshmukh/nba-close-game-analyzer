from api_client import get_all_teams, get_team_id
from data_manager import fetch_and_cache, load_close_games

print("Fetching all teams...")
teams = get_all_teams()
print(f"  Got {len(teams)} teams")

lakers = get_team_id("Lakers")
celtics = get_team_id("Celtics")
print(f"  Lakers ID: {lakers['id']}, Celtics ID: {celtics['id']}")

for team in (lakers, celtics):
    name = team["full_name"]
    print(f"\nFetching/caching close games for {name} (2023 season)...")
    games = fetch_and_cache(team["id"], name, seasons=[2023])
    wins = sum(1 for g in games if g["team_won"])
    print(f"  Close games: {len(games)}  |  Wins: {wins}  |  Losses: {len(games) - wins}")
    if games:
        g = games[0]
        print(f"  Sample: {g['date']}  {g['home_team']} {g['home_score']} - {g['away_score']} {g['away_team']}  (diff: {g['point_diff']})")

print("\nVerifying cache round-trip for Lakers...")
cached = load_close_games(lakers["full_name"])
print(f"  Loaded {len(cached)} games from CSV — types: home_score={type(cached[0]['home_score']).__name__}, team_won={type(cached[0]['team_won']).__name__}")