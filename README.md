# NBA Close Game Analyzer

# Authors: Sujan Nandikol Sunilkumar, Aaditya Deshmukh


# Project Description:

The NBA Close Game Analyzer is a GUI-based application that allows users to compare the "clutch" performances of two NBA teams head-to-head. Users can select any two teams and the app filters through historical matchups to surface only the games that ended with a point differential of 5 or fewer, giving a true measure of how teams perform under pressure. By focusing exclusively on these tight finishes, the tool provides meaningful insight into which teams are most resilient and competitive when it matters most. The application is powered by the [BallDontLie API](https://www.balldontlie.io/), a free basketball statistics API that requires creating a free account on their website to obtain an API key. This project was built by Sujan Nandikol Sunilkumar and Aaditya Deshmukh as part of a CS122 course project.




# Project Outline / Plan

## 1. Interface — GUI with Tkinter (Author 1: Sujan + Author 2: Aaditya)
*30 points — both partners each responsible for one page of the interface*

The application will be built using Python's **Tkinter** library and will consist of at least two windows:

- **Home Screen (Window 1):** The main page where users select two NBA teams from dropdown menus and click a button to run the analysis. Widgets include:
  - Team 1 dropdown (OptionMenu)
  - Team 2 dropdown (OptionMenu)
  - "Analyze" button to trigger data fetch and analysis
  - Status label to show loading/error messages

- **Results Screen (Window 2):** A pop-up or secondary window that displays the close game comparison results between the two selected teams. Widgets include:
  - A results summary label (win/loss record in close games)
  - An embedded matplotlib chart showing the visualization
  - A "Back" button to return to the home screen

This gives us at least **4 widgets** (2 dropdowns, 1 button, 1 results display) as required.

---

## 2. Access Web Data (Author 1: Sujan)
*20 points*

Data is fetched from the internet using the [BallDontLie API](https://www.balldontlie.io/), a free, publicly accessible NBA statistics API. For a selected team, the app queries all historical game results and retrieves game scores, dates, and team identifiers. API calls are made using Python's `requests` library with the user's API key stored in a local config or environment variable.

---

## 3. Data Organization (Author 1: Sujan)
*20 points*

Retrieved game data is organized and stored as **CSV files**, one per team (e.g., `lakers_games.csv`). Each CSV file contains rows for each game with columns for date, home team, away team, home score, away score, and point differential. Only games with a point differential of ≤ 5 are retained. This file-based caching system ensures data is stored in a structured, human-readable spreadsheet format that matches the project data and avoids repeated API calls.

---

## 4. Data Analysis (Author 2: Aaditya) 
*20 points*

The data analysis portion of the project will take the stored close-game CSV data and compare how the two selected NBA teams perform in games decided by 5 points or fewer. For each team, the program will count the total number of close games, the number of wins, and the number of losses. From this, it will calculate a close-game win percentage to help measure which team performs better under pressure. The analysis will also compare the two selected teams head-to-head based on these statistics and generate a summary that can be displayed in the results window. This allows the user to quickly understand which team has been more successful in clutch situations.

## 5. Visualization (Author 2: Aaditya)
*20 points* 

The visualization portion of the project will present the analysis results in a simple and clear graphical format using matplotlib. After the close-game data is analyzed, the program will generate a chart comparing the two selected teams. The chart will visually display information such as close-game wins and losses or win percentage so that users can easily interpret the results. This chart will be embedded into the Tkinter results screen, alongside a text summary of the comparison. The purpose of the visualization is to make the data more interactive, readable, and meaningful for the user.

