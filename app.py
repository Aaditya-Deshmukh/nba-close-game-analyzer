from flask import Flask, abort, request, jsonify
from api_client import get_recent_seasons, get_all_teams, get_team_id, get_games_for_team, filter_close_games
from data_manager import fetch_and_cache

app = Flask(__name__)

@app.route("/")
def home():
    return "welcome to NBA close game analyzer"



"""
This is the api route to get the data for both teams

team 1 is the name of the first team we are comparing
team 2 is the name of the second team we are comparing

"""
@app.route("/get-team-data")
def get_data():
    # get the team ids for each team

    team1= request.args.get("team1")
    team2=request.args.get("team2")
    seasons = int(request.args.get("seasons", 5))
    try:
        team1_id = get_team_id(team1)['id']
        team2_id = get_team_id(team2)['id']
        team1_close_games = fetch_and_cache(team1_id, team1, seasons_back=seasons)
        team2_close_games = fetch_and_cache(team2_id, team2, seasons_back=seasons)
    except ValueError:
        abort(404)


    return jsonify(
        {
            "team1": team1_close_games, 
            "team2": team2_close_games
        }
    )



if __name__ == "__main__":
    app.run(debug=True)