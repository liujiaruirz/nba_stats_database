# NBA Database

## Description

A Python application that operates the NBA database through a simple web front end. The database is designed to serve NBA fans, scouts, data analysts, etc., to help them compare players and analyze games throughout multiple seasons. 

Users can achieve the statistics of all NBA players and teams. Records can also be inquired by sorting certain domains, such as points, rebounds, assists, etc. The whole design includes seven entities: season, team, player, game, coach, player stats, team stats and contract. Details can be found in E-R diagram.

The featured function of the application is to help users achieve data views in a more intuitive way – users can get the “radar chart” of a player that they are interested in. On top of that, users can choose specific perspectives to generate the radar chart they need and do the comparison.

_(Please see Features for the functions we have not implement.)_

## Data Source

We plan to combine these two Kaggle dataset and form our own database.

https://www.kaggle.com/wyattowalsh/basketball

https://www.kaggle.com/nathanlauga/nba-games?select=ranking.csv

## Features

1. The all-time roster of a team. 
 - In the team detail pages, users can obtain a list of ALL players who once played for the team with their jersey numbers, positions, etc. 
 - However, player's contract was not implemented because we could not find any open dataset that records such infomation.

2. The Radar Chart.
 - As described in Part 1, radar chart is a function in our application to measure the player's abilities of based on their career stats. Here, we originate 5 different areas: PTS, AST, REB, VERS, POW, respectively standing for Scoring Ability, Asisting Ability, Rebound Ability, Versatility, and Body Strength. We calculate the values for each area based on our self-designed algorithm. 
 - We also provide the radar chart of the average number among all players for users to make comparison.
 - We did not implement the function for users to choose specific areas and generate their own radar chart. This is because we don't have enough player's stats to form more areas :(

Besides, we have some other features such as team arena information and game stats query, which help users learn more about the facts of NBA. 

## Featured Queries
```
SELECT Game_ID, Home_Team_Win, year, T1.name as hteam, T2.name as ateam, home_team_score, away_team_score 
       FROM Game G, team T1, team T2 
       WHERE G.home_team_ID = T1.team_ID AND G.away_team_ID = T2.team_ID 
             AND T1.name = :hteam and T2.name = :ateam and year = :year
```
This query statement is used in the game search page. Users input hteam(home team), ateam(away team), and year(season) of the game they want to query. It returns a list of games that satisfy the given conditions. Note that home team and away team need to be selected from two separate team tables (T1 and T2). 

```
SELECT Pr.first_name, Pr.last_name, MIN, PTS, AST, REB, Pr.Team_ID 
       FROM game G, Plays Ps, Player Pr 
       WHERE G.Game_ID = Ps.Game_ID AND Pr.Player_ID = Ps.Player_ID AND G.Game_id = :gid 
       ORDER BY PTS DESC NULLS LAST
```
This query statement is used in the game detail page. It selects all player's stats in a given game specified by Game_ID. Here we join three tables: _player_, _plays_, and _games_. In _player_ table, we achieve the information of player's full name. In _plays_ table, we obtain the player's stats such as MIN and PTS. And finally, we locate the game by Game_ID of the _game_ table.
