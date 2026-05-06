from collections import defaultdict


#get summary of wins losses and win percentage
def summarize_team_games(games):
    total = len(games)
    wins = sum(1 for g in games if g["team_won"])
    losses = total - wins
    win_pct = round(wins / total * 100, 1) if total else 0

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
def get_game_season(game):
    """
    Converts the game date into the NBA season.

    Example:
    2023-10-26 -> 2023 season
    2024-02-10 -> 2023 season
    """
    date_str = game.get("date", "")

    if not date_str:
        return "Unknown"

    year = int(date_str[:4])
    month = int(date_str[5:7])

    #nba season starts around october
    return year if month >= 10 else year - 1


#get the date of the game for display
def get_game_date(game):
    return game.get("date", "Unknown Date")


#group and summarize the close games by season
def summarize_by_season(games):
    season_summary = {}

    for game in games:
        season = get_game_season(game)

        if season not in season_summary:
            season_summary[season] = {
                "season": season,
                "total": 0,
                "wins": 0,
                "losses": 0,
                "win_pct": 0
            }

        season_summary[season]["total"] += 1

        if game["team_won"]:
            season_summary[season]["wins"] += 1
        else:
            season_summary[season]["losses"] += 1

    for season in season_summary:
        total = season_summary[season]["total"]
        wins = season_summary[season]["wins"]
        season_summary[season]["win_pct"] = round((wins / total) * 100, 1) if total else 0

    return sorted(season_summary.values(), key=lambda x: x["season"])


#format each close game by season for the app display
def format_close_games_by_season(games, team_name):
    games_by_season = defaultdict(list)

    for game in games:
        season = get_game_season(game)

        home_team = game.get("home_team")
        away_team = game.get("away_team")
        home_score = game.get("home_score")
        away_score = game.get("away_score")

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

        margin = game.get("point_diff")

        if margin is None and team_score is not None and opponent_score is not None:
            margin = abs(team_score - opponent_score)

        game_info = {
            "date": get_game_date(game),
            "opponent": opponent,
            "team_score": team_score,
            "opponent_score": opponent_score,
            "final_score": f"{team_score}-{opponent_score}",
            "result": "Win" if game["team_won"] else "Loss",
            "margin": margin if margin is not None else "N/A"
        }

        games_by_season[season].append(game_info)

    return dict(sorted(games_by_season.items()))