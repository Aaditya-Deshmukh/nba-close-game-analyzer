from analysis import analyze_team_close_games, create_recent_games_chart

# Run the analysis for one team and one season
result = analyze_team_close_games(
    team_name="Los Angeles Lakers",
    seasons=[2023],
    max_games=10
)

# Print the summary
print(result["summary"])

# Print recent close games
print("\nRecent close games:")
for game in result["recent_games"]:
    game_result = "Win" if game["team_won"] else "Loss"
    print(
        f"{game['date']} | {game_result} | "
        f"{game['home_team']} {game['home_score']} - "
        f"{game['away_score']} {game['away_team']} | "
        f"Diff: {game['point_diff']}"
    )

# Save chart image for web app use
chart_path = create_recent_games_chart(result)
print(f"\nChart saved to: {chart_path}")