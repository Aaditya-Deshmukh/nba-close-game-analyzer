import plotly.graph_objects as go


#create a bar chart to compare wins and losses
def create_win_loss_chart(team1_name, team2_name, summary):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name=team1_name,
        x=["Wins", "Losses"],
        y=[
            summary["team1"]["wins"],
            summary["team1"]["losses"]
        ]
    ))

    fig.add_trace(go.Bar(
        name=team2_name,
        x=["Wins", "Losses"],
        y=[
            summary["team2"]["wins"],
            summary["team2"]["losses"]
        ]
    ))

    fig.update_layout(
        title="Team Win/Loss Comparison",
        xaxis_title="Result",
        yaxis_title="Number of Games",
        barmode="group",
        template="plotly_white"
    )

    return fig.to_html(full_html=False)


#create a line chart to show win percentage by season
def create_season_trend_chart(team1_name, team2_name, team1_seasons, team2_seasons):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[row["season"] for row in team1_seasons],
        y=[row["win_pct"] for row in team1_seasons],
        mode="lines+markers",
        name=team1_name
    ))

    fig.add_trace(go.Scatter(
        x=[row["season"] for row in team2_seasons],
        y=[row["win_pct"] for row in team2_seasons],
        mode="lines+markers",
        name=team2_name
    ))

    fig.update_layout(
        title="Close-Game Win Percentage by Season",
        xaxis_title="Season",
        yaxis_title="Close-Game Win Percentage",
        yaxis=dict(range=[0, 100]),
        template="plotly_white"
    )

    return fig.to_html(full_html=False)


#create a bar chart to show how many close games each team had by season
def create_close_games_by_season_chart(team1_name, team2_name, team1_seasons, team2_seasons):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[row["season"] for row in team1_seasons],
        y=[row["total"] for row in team1_seasons],
        name=team1_name
    ))

    fig.add_trace(go.Bar(
        x=[row["season"] for row in team2_seasons],
        y=[row["total"] for row in team2_seasons],
        name=team2_name
    ))

    fig.update_layout(
        title="Number of Close Games by Season",
        xaxis_title="Season",
        yaxis_title="Close Games Played",
        barmode="group",
        template="plotly_white"
    )

    return fig.to_html(full_html=False)