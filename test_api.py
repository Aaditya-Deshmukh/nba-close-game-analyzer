from api_client import get_all_teams, get_team_id, get_recent_seasons
from data_manager import fetch_and_cache

# ── 1. Confirm the API connection works ──────────────────────────────────────
print("Fetching all teams...")
teams = get_all_teams()
print(f"  Got {len(teams)} teams\n")

# ── 2. Look up teams by name ─────────────────────────────────────────────────
lakers = get_team_id("Lakers")
celtics = get_team_id("Celtics")
print(f"Lakers  -> id={lakers['id']}, full name: {lakers['full_name']}")
print(f"Celtics -> id={celtics['id']}, full name: {celtics['full_name']}\n")

# ── 3. Test the seasons_back feature ─────────────────────────────────────────
# Show what season lists are generated for different lookback windows
for n in (1, 3, 5, 10):
    print(f"  seasons_back={n:2d}  ->  {get_recent_seasons(n)}")
print()

# ── 4. Fetch and cache close games for different lookback windows ─────────────
for seasons_back in (1, 5):
    print(f"── Last {seasons_back} season(s) ──────────────────────────────")
    for team in (lakers, celtics):
        games = fetch_and_cache(team["id"], team["full_name"], seasons_back=seasons_back)
        wins = sum(1 for g in games if g["team_won"])
        losses = len(games) - wins
        pct = (wins / len(games) * 100) if games else 0
        print(f"  {team['full_name']:<30}  close games: {len(games):3d}  |  W: {wins}  L: {losses}  ({pct:.1f}%)")
    print()