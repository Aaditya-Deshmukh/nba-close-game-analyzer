from flask import Flask, abort, request, jsonify, render_template
from api_client import get_all_teams, get_team_id, get_recent_seasons
from data_manager import fetch_and_cache
from analysis import (
    load_team_csv,
    games_to_df,
    compare_teams,
    summarize_by_season,
    format_close_games_by_season
)
from visualizations import (
    create_win_loss_chart,
    create_season_trend_chart,
    create_close_games_by_season_chart
)

app = Flask(__name__)

def load_or_fetch_team_games(team_id, team_name, seasons_back):
    """
    First check if the team's preloaded CSV using Pandas.
    If the CSV does not exist, it tries to fetch_and_cache.
    Always returns a Pandas DataFrame.
    """
    seasons = get_recent_seasons(seasons_back)

    cached_df = load_team_csv(team_name, seasons)

    if cached_df is not None:
        return cached_df

    fetched_games = fetch_and_cache(
        team_id,
        team_name,
        seasons_back=seasons_back
    )

    return games_to_df(fetched_games)


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

    team1_games = load_or_fetch_team_games(
        team1["id"],
        team1["full_name"],
        seasons
    )

    team2_games = load_or_fetch_team_games(
        team2["id"],
        team2["full_name"],
        seasons
    )


    summary = compare_teams(team1_games, team2_games)

    team1_seasons = summarize_by_season(team1_games)
    team2_seasons = summarize_by_season(team2_games)

    team1_games_by_season = format_close_games_by_season(team1_games, team1['full_name'])
    team2_games_by_season = format_close_games_by_season(team2_games, team2['full_name'])

    season_trend_chart = create_season_trend_chart(
        team1["full_name"],
        team2["full_name"],
        team1_seasons,
        team2_seasons
    )

    close_games_by_season_chart = create_close_games_by_season_chart(
        team1["full_name"],
        team2["full_name"],
        team1_seasons,
        team2_seasons
    )

    win_loss_chart = create_win_loss_chart(
    team1["full_name"],
    team2["full_name"],
    summary
)

    return render_template(
    "results.html",
    team1_name=team1["full_name"],
    team2_name=team2["full_name"],
    seasons=seasons,

    team1_total=summary["team1"]["total"],
    team1_wins=summary["team1"]["wins"],
    team1_losses=summary["team1"]["losses"],
    team1_pct=summary["team1"]["win_pct"],

    team2_total=summary["team2"]["total"],
    team2_wins=summary["team2"]["wins"],
    team2_losses=summary["team2"]["losses"],
    team2_pct=summary["team2"]["win_pct"],

    win_loss_chart=win_loss_chart,
    season_trend_chart=season_trend_chart,
    close_games_by_season_chart=close_games_by_season_chart,

    team1_games_by_season=team1_games_by_season,
    team2_games_by_season=team2_games_by_season
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
        team1_close_games = load_or_fetch_team_games(
            team1["id"],
            team1["full_name"],
            seasons
        )

        team2_close_games = load_or_fetch_team_games(
            team2["id"],
            team2["full_name"],
            seasons
        )
    except ValueError:
        abort(404)

    team1_records = team1_close_games.copy()
    team2_records = team2_close_games.copy()

    team1_records["date"] = team1_records["date"].dt.strftime("%Y-%m-%d")
    team2_records["date"] = team2_records["date"].dt.strftime("%Y-%m-%d")

    return jsonify({
        "team1": team1_records.to_dict("records"),
        "team2": team2_records.to_dict("records")
    })


if __name__ == "__main__":
    app.run(debug=True)
