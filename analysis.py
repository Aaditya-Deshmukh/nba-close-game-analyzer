from data_manager import fetch_and_cache
from api_client import get_team_id
import matplotlib.pyplot as plt
import os


def analyze_team_close_games(team_name, seasons=None, max_games=10):
    """
    Analyze one team's close games for the selected season(s).
    """

    # Get the teams API information using the team name
    team = get_team_id(team_name)
    full_team_name = team["full_name"]

    # Fetch close-game data 
    games = fetch_and_cache(
        team["id"],
        full_team_name,
        seasons=seasons
    )

    # Sort games 
    games = sorted(games, key=lambda game: game["date"], reverse=True)

    # Count total close games, wins, and losses
    total_games = len(games)
    wins = sum(1 for game in games if game["team_won"])
    losses = total_games - wins

    # Calculate win percentage 
    if total_games == 0:
        win_percentage = 0.0
    else:
        win_percentage = round((wins / total_games) * 100, 2)

    # Keep only the most recent games for display
    recent_games = games[:max_games]

    # Create a summary
    summary = generate_summary(
        full_team_name,
        seasons,
        total_games,
        wins,
        losses,
        win_percentage
    )

    # Return all results in one dictionary
    return {
        "team": full_team_name,
        "seasons": seasons,
        "total_games": total_games,
        "wins": wins,
        "losses": losses,
        "win_percentage": win_percentage,
        "recent_games": recent_games,
        "summary": summary
    }


def generate_summary(team_name, seasons, total_games, wins, losses, win_percentage):
    """
    Create a short text summary of the team's close-game results.
    """

    # Format the selected seasons for display
    if seasons is None:
        season_text = "the selected seasons"
    elif len(seasons) == 1:
        season_text = f"the {seasons[0]} season"
    else:
        season_text = ", ".join(str(season) for season in seasons)

    # Create the summary text
    summary = (
        f"{team_name} had {total_games} close games in {season_text}. "
        f"They won {wins}, lost {losses}, and had a close-game win percentage "
        f"of {win_percentage}%."
    )

    return summary


def create_recent_games_chart(analysis_result, output_path="static/close_games_chart.png"):
    """
    Create a matplotlib chart for recent close games and save it as an image.
    """

    # Get recent games from the analysis result
    recent_games = analysis_result["recent_games"]

    # Make sure the folder exists for web image output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create the chart figure
    fig, ax = plt.subplots(figsize=(8, 4))

    # Display a message if there are no games to graph
    if len(recent_games) == 0:
        ax.text(
            0.5,
            0.5,
            "No close games found",
            ha="center",
            va="center",
            fontsize=14
        )
        ax.set_axis_off()
        fig.savefig(output_path, bbox_inches="tight")
        plt.close(fig)
        return output_path

    labels = []
    signed_diffs = []

    # Build chart labels and point diff values
    for game in recent_games:
        # Determine the opponent for the selected team
        opponent = (
            game["away_team"]
            if game["home_team"] == analysis_result["team"]
            else game["home_team"]
        )

        labels.append(f"{game['date']}\nvs {opponent}")

        # Wins are positive, losses are negative
        if game["team_won"]:
            signed_diffs.append(game["point_diff"])
        else:
            signed_diffs.append(-game["point_diff"])

    # Plot the point diffs
    ax.bar(labels, signed_diffs)

    # Add chart labels and formatting
    ax.axhline(0, linewidth=1)
    ax.set_title(f"{analysis_result['team']} Recent Close Games")
    ax.set_xlabel("Game")
    ax.set_ylabel("Point Differential")
    ax.tick_params(axis="x", labelrotation=45)

    fig.tight_layout()

    # Save chart as an image for the web app
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)

    return output_path