from flask import Flask, abort, request, jsonify, render_template
from api_client import get_all_teams, get_team_id
from data_manager import fetch_and_cache

app = Flask(__name__)


@app.route("/")
def home():
    teams = get_all_teams()
    return render_template("index.html", teams=teams)


@app.route("/results")
def results():
    team1_name = request.args.get("team1")
    team2_name = request.args.get("team2")
    seasons = int(request.args.get("seasons", 3))

    try:
        team1 = get_team_id(team1_name)
        team2 = get_team_id(team2_name)
    except ValueError:
        abort(404)

    team1_games = fetch_and_cache(team1["id"], team1["full_name"], seasons_back=seasons)
    team2_games = fetch_and_cache(team2["id"], team2["full_name"], seasons_back=seasons)

    team1_wins   = sum(1 for g in team1_games if g["team_won"])
    team2_wins   = sum(1 for g in team2_games if g["team_won"])
    team1_total  = len(team1_games)
    team2_total  = len(team2_games)
    team1_pct    = round(team1_wins / team1_total * 100, 1) if team1_total else 0
    team2_pct    = round(team2_wins / team2_total * 100, 1) if team2_total else 0

    return render_template(
        "results.html",
        team1_name   = team1["full_name"],
        team2_name   = team2["full_name"],
        seasons      = seasons,
        team1_total  = team1_total,
        team1_wins   = team1_wins,
        team1_losses = team1_total - team1_wins,
        team1_pct    = team1_pct,
        team2_total  = team2_total,
        team2_wins   = team2_wins,
        team2_losses = team2_total - team2_wins,
        team2_pct    = team2_pct,
    )


# JSON API endpoint — kept for programmatic access
@app.route("/get-team-data")
def get_data():
    team1_name = request.args.get("team1")
    team2_name = request.args.get("team2")
    seasons = int(request.args.get("seasons", 5))

    try:
        team1 = get_team_id(team1_name)
        team2 = get_team_id(team2_name)
        team1_close_games = fetch_and_cache(team1["id"], team1["full_name"], seasons_back=seasons)
        team2_close_games = fetch_and_cache(team2["id"], team2["full_name"], seasons_back=seasons)
    except ValueError:
        abort(404)

    return jsonify({"team1": team1_close_games, "team2": team2_close_games})


if __name__ == "__main__":
    app.run(debug=True)
