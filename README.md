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
*Change `seasons_back` to however many seasons you want to compare, e.g. 3:*

for example if you wanted to compare 3 seasons:

```bash
python3 -c "from data_manager import warm_cache_all_teams; warm_cache_all_teams(seasons_back=3)" #change the seasons_back to what you want (3,5,...)
```
This downloads data for every team and saves it as CSV files in `data/`. After this completes, the app reads from disk and makes no further API calls.

6. Start the web app:
```bash
python3 app.py
```

Then open `http://127.0.0.1:8080` in your browser (use Safari or Firefox — Chrome may block localhost).


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
- Compare individual player stats across teams
- Deploy the app to a public server so no local installation is required

# Team Contributions

This project was completed as a partner project. Both partners contributed to different parts of the NBA Close Game Analyzer, including the Flask interface, data access, data organization, analysis, and visualizations.

## Partner 1 (Sujan) Contributions

Sujan worked mainly on the data access, data organization, and initial Flask app structure. This included setting up the BallDontLie API connection, retrieving NBA team and game data, and storing the results in local CSV files so the app would not need to repeatedly call the API. Sujan also helped set up the main Flask routes and page templates, including the basic layout and structure for the interface.

Main contributions included:

- Connected the project to the BallDontLie API
- Retrieved team and game data
- Cached API results into local CSV files
- Organized game data by team and season range
- Helped create the Flask app structure
- Set up the main page template and helped with visual layout

## Partner 2 (Aaditya) Contributions

Aaditya worked mainly on the analysis, visualizations, and the second/results page of the project. This included using the stored CSV data to calculate close-game statistics such as total close games, wins, losses, and win percentage. Aaditya also created the interactive Plotly visualizations and organized the results page sections where the charts and analysis outputs are displayed.

Main contributions included:

- Used stored CSV data for analysis
- Calculated close-game wins, losses, total games, and win percentage
- Compared two selected teams using close-game metrics
- Created interactive Plotly charts
- Embedded visualizations into the Flask results page
- Built sections on the second/results page for charts and analysis
- Helped make the data easier to understand through visual summaries

## Project Components Covered

Together, the project includes the major components required for the final project:

- **Interface:** Flask web app with pages for selecting teams/seasons and viewing results
- **Data Access:** BallDontLie API used to retrieve NBA team and game data
- **Data Organization:** Game data stored locally in CSV files by team and season range
- **Analysis:** Close-game performance metrics calculated from the stored data
- **Visualizations:** Interactive Plotly charts embedded into the Flask results page
- **GitHub:** Project code and partner contributions are stored in the GitHub repository
