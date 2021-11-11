# NBA Database

**Database Account**: yh3290

**Web Front-End App URL: http://34.139.184.242:8111**

**Team Members:** Jiarui Liu, Yong Hao

## Description

A Python application that operates the NBA database through a simple web front end. The database is designed to serve NBA fans, scouts, data analysts, etc., to help them compare players and analyze games throughout multiple seasons. 

Users can achieve the statistics of all NBA players and teams. Records can also be inquired by sorting certain domains, such as points, rebounds, assists, etc. The whole design includes seven entities: season, team, player, game, coach, player stats, team stats and contract. Details can be found in E-R diagram.

The featured function of the application is to help users achieve data views in a more intuitive way – users can get the “radar chart” of a player, a team, or a coach that they inquiry. On top of that, users can choose specific perspectives to generate the radar chart they need and do the comparison.

## Data Source

We plan to combine these two Kaggle dataset and form our own database.

https://www.kaggle.com/wyattowalsh/basketball

https://www.kaggle.com/nathanlauga/nba-games?select=ranking.csv

## Features

1. The all-time roster of a team. 

- In the team detail pages, users can obtain a list of players who once played for the team with their Jersey number, position, etc. 

2. The Radar Chart.

- As described in Part 1, radar chart is a function in our application to measure the player's ability of based on their career stats. Here, we originate 5 different areas: PTS, AST, REB, VERS, POW, respectively standing for Scoring ability, Asisting ability, Rebound ability, Versatility, Body Strength. We calculate the values for each area based on our own algorithm. Besides, we provide the radar chart of the average number among all players in the league to make comparison.

## Interesting Queries
```
SELECT name, Year_Founded, Head_Coach, State, City, Capacity, arena_name FROM team, arena WHERE team.Arena_ID = arena.Arena_ID AND team.name != 'Free_Player'
```

```
SELECT Pr.first_name, Pr.last_name, MIN, PTS, AST, REB, Pr.Team_ID FROM game G, Plays Ps, Player Pr WHERE G.Game_ID = Ps.Game_ID AND Pr.Player_ID = Ps.Player_ID AND G.game_id = :gid ORDER BY PTS DESC NULLS LAST
```
