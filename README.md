# NBA Close Game Analyzer

# Authors: Sujan Nandikol Sunilkumar, Aaditya Deshmukh


# Project Description:

The NBA Close Game Analyzer is a web application that allows users to compare the "clutch" performances of two NBA teams head-to-head. Users can select any two teams and the app filters through historical matchups to surface only the games that ended with a point differential of 5 or fewer, giving a true measure of how teams perform under pressure. By focusing exclusively on these tight finishes, the tool provides meaningful insight into which teams are most resilient and competitive when it matters most. The application is powered by the [BallDontLie API](https://www.balldontlie.io/), a free basketball statistics API that requires creating a free account on their website to obtain an API key. This project was built by Sujan Nandikol Sunilkumar and Aaditya Deshmukh as part of a CS122 course project.


# Installation

1. Clone the repository and navigate into it:
```bash
git clone https://github.com/Aaditya-Deshmukh/nba-close-game-analyzer.git
cd nba-close-game-analyzer
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Add your API key — copy the example file and fill it in:
```bash
cp .env.example .env
# open .env and set BALLDONTLIE_API_KEY=your_key_here
```

5. Pre-fetch and cache close game data for all 30 NBA teams (run once before starting the app):
```bash
python3 -c "from data_manager import warm_cache_all_teams; warm_cache_all_teams(seasons_back=3)" #change the seasons_back to what you want (3,5,...)
```
This downloads data for every team and saves it as CSV files in `data/`. After this completes, the app reads from disk and makes no further API calls.

6. Start the web app:
```bash
python3 app.py
```

Then open `http://127.0.0.1:5000` in your browser (use Safari or Firefox — Chrome may block localhost).


# Project Outline / Plan

## 1. Interface — Web App with Flask (Author 1: Sujan + Author 2: Aaditya)
*30 points — both partners each responsible for one page of the interface*

The application is built using Python's **Flask** framework and consists of two pages:

- **Home Page (`/`):** The main page where users select two NBA teams from dropdown menus, choose how many seasons to compare, and click a button to run the analysis. Widgets include:
  - Team 1 dropdown
  - Team 2 dropdown
  - Seasons number input
  - "Analyze" button to trigger the comparison

- **Results Page (`/results`):** Displays the close game comparison results between the two selected teams. Widgets include:
  - A results summary showing win/loss record and win percentage for each team
  - A winner banner comparing the two teams
  - A matplotlib chart showing the visualization
  - A "Back" button to return to the home page

This gives us at least **4 widgets** (2 dropdowns, 1 number input, 1 button) as required.

---

## 2. Access Web Data (Author 1: Sujan)
*20 points*

Data is fetched from the internet using the [BallDontLie API](https://www.balldontlie.io/), a free, publicly accessible NBA statistics API. For a selected team, the app queries all historical game results and retrieves game scores, dates, and team identifiers. API calls are made using Python's `requests` library with the user's API key stored in a local `.env` file.

---

## 3. Data Organization (Author 1: Sujan)
*20 points*

Retrieved game data is organized and stored as **CSV files**, one per team (e.g., `lakers_games.csv`). Each CSV file contains rows for each game with columns for date, home team, away team, home score, away score, and point differential. Only games with a point differential of ≤ 5 are retained. This file-based caching system ensures data is stored in a structured, human-readable spreadsheet format and avoids repeated API calls.

---

## 4. Data Analysis (Author 2: Aaditya) 
*20 points*

The data analysis portion of the project will take the stored close-game CSV data and compare how the two selected NBA teams perform in games decided by 5 points or fewer. For each team, the program will count the total number of close games, the number of wins, and the number of losses. From this, it will calculate a close-game win percentage to help measure which team performs better under pressure. The analysis will also compare the two selected teams head-to-head based on these statistics and generate a summary displayed in the results page.

## 5. Visualization (Author 2: Aaditya)
*20 points* 

The visualization portion of the project will present the analysis results in a simple and clear graphical format using matplotlib. After the close-game data is analyzed, the program will generate a chart comparing the two selected teams. The chart will visually display information such as close-game wins and losses or win percentage so that users can easily interpret the results. This chart will be embedded into the Flask results page alongside a text summary of the comparison.

---

# Future Updates
- Add head-to-head filtering to show only games where the two selected teams played each other
- Add per-season breakdown charts to show clutch performance trends over time
- Deploy the app to a public server so no local installation is required
