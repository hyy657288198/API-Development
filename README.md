# API Development

# Instructions and descriptions
1. Game Rsults Summary - /api/results?date={YYYY-MM-DD}
    * a resource that provides summarizes all game results on a given date
    * Input: date time  e.g.2012-04-29
    * List the data of games in the given date, and the structure of each game looks like <br /> 
    {<br />
    &nbsp; &nbsp;"away team abbreviation": "OTT", <br />
    &nbsp; &nbsp;"away team goals": 2, <br />
    &nbsp; &nbsp;"away team id": 9, <br />
    &nbsp; &nbsp;"date time": "2016-03-11", <br />
    &nbsp; &nbsp;"game id": 2015021010, <br />
    &nbsp; &nbsp;"home team abbreviation": "FLA", <br />
    &nbsp; &nbsp;"home team goals": 6, <br />
    &nbsp; &nbsp;"home team id": 13<br />
  }, <br />
    * The resources has been used are 
        * game.csv, which provides "away_goals", "away_team_id", "date_time", "game_id", "home_goals", "home_team_id",  
        * team_info.csv, which provides "away_abbreviation", "away_team_id", "home_abbreviation", "home_team_id"
        
    * The design rationale is for any game results summary in a given date, the data is all in the file called "game.csv", but this file doesn't contain the name of each team. And "team_info.csv" contains those data, and those two file have common variables, which are the home_team_id and away_team_id in "game.csv" and the team_id in "team_info.csv". home_team_id and away_team_id are all in the team_id, so, merge those two files with left join twice, one for the away team and one for the home team. Since those two solutions of merging have the same name for one column, but they actually represent different information. So we rename the abbreviation to home_abbreviation for the home team and the abbreviation to away_abbreviation for the away team. This will give the final solution.

2. Game Results Details - /api/results/{ID}/teams
    * a resource that provides performance information for each team involved in a completed game
    * Input: a game id  e.g.2011030221
    * The structure look likes <br />
[<br />
&nbsp; &nbsp; {<br />
    &nbsp; &nbsp; &nbsp; &nbsp; "Home or Away": "away", <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "team abbreviation": "NJD", <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "face off win percentage": 44.9, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "game id": 2011030221, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "giveaways": 6, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "goals": 3, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "head coach": "Peter DeBoer", <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "hits": 31, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "penalties in minutes": 12, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "power play goals": 1, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "power play opportunities": 3, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "settled in": "OT", <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "shots": 26, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "takeaways": 7, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "team id": 1, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "won": false <br />
  &nbsp; &nbsp; }, <br />
  &nbsp; &nbsp; {<br />
    &nbsp; &nbsp; &nbsp; &nbsp; "Home or Away": "home", <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "team abbreviation": "PHI", <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "face off win percentage": 55.1, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "game id": 2011030221, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "giveaways": 13, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "goals": 4, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "head coach": "Peter Laviolette", <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "hits": 27, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "penalties in minutes": 6, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "power play goals": 1, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "power play opportunities": 6, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "settled in": "OT", <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "shots": 36, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "takeaways": 4, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "team id": 4, <br />
    &nbsp; &nbsp; &nbsp; &nbsp; "won": true<br />
  &nbsp; &nbsp; }<br />
]

    * The resources has been used are 
        * game_teams_stats.csv, which provides "HoA", "faceOffWinPercentage", "game_id", "giveaways", "goals", "head_coach", "hits", "pim", "powerPlayGoals", "powerPlayOpportunities", "settled_in", "shots", "takeaways", "team_id", "won",  
        * team_info.csv, which provides "abbreviation", "team_id"".
    
    * The design rationale is for any game results details in any given game, the data is all in the file called "game_teams_stats.csv", but this file doesn't contain the name of each team. And "team_info.csv" contains those data, and those two file have common variables, which are the team_id. Therefore, merge those two files will give the solution.

3. Game Player Stats - /api/results/{ID}/players
    * a resource that provides detailed player performance statistics for each of the players that participate in a game
    * Input: a game id  e.g.2011030221
    * List the data of players in the game, and the structure of each player looks like <br /> 
    "BraydenSchenn": {<br />
        &nbsp; &nbsp; "team abbreviation": "PHI", <br />
        &nbsp; &nbsp; "assists": 0, <br />
        &nbsp; &nbsp; "birth city": "Saskatoon", <br />
        &nbsp; &nbsp; "birth date": "1991-08-22", <br />
        &nbsp; &nbsp; "blocked": 0, <br />
        &nbsp; &nbsp; "even time on ice": 501, <br />
        &nbsp; &nbsp; "face off wins": 2, <br />
        &nbsp; &nbsp; "face off taken": 4, <br />
        &nbsp; &nbsp; "first name": "Brayden", <br />
        &nbsp; &nbsp; "franchiseId": 16, <br />
        &nbsp; &nbsp; "game id": 2011030221, <br />
        &nbsp; &nbsp; "giveaways": 0, <br />
        &nbsp; &nbsp; "goals": 0, <br />
        &nbsp; &nbsp; "hits": 2, <br />
        &nbsp; &nbsp; "last name": "Schenn", <br />
        &nbsp; &nbsp; "link": "/api/v1/people/8475170", <br />
        &nbsp; &nbsp; "nationality": "CAN", <br />
        &nbsp; &nbsp; "penalty minutes": 0, <br />
        &nbsp; &nbsp; "player id": 8475170, <br />
        &nbsp; &nbsp; "plus or minus": -1, <br />
        &nbsp; &nbsp; "power play assists": 0, <br />
        &nbsp; &nbsp; "power play goals": 0, <br />
        &nbsp; &nbsp; "power play time on ice": 83, <br />
        &nbsp; &nbsp; "primary position": "C", <br />
        &nbsp; &nbsp; "short handed assists": 0, <br />
        &nbsp; &nbsp; "short handed goals": 0, <br />
        &nbsp; &nbsp; "short handed time on ice": 0, <br />
        &nbsp; &nbsp; "short name of team": "Philadelphia", <br />
        &nbsp; &nbsp; "shots": 1, <br />
        &nbsp; &nbsp; "takeaways": 0, <br />
        &nbsp; &nbsp; "team name": "Flyers", <br />
        &nbsp; &nbsp; "team id": 4, <br />
        &nbsp; &nbsp; "total time on ice": 584<br />
    * The resources has been used are  
        * team_info.csv, which provides "abbreviation", "team_id", "teamName", "shortName",
        * player_info.csv, "player_id","firstName","lastName","nationality","birthCity","primaryPosition","birthDate","link",
        * game_skater_stats.csv, which provides "game_id","player_id","team_id","timeOnIce","assists","goals","shots","hits","powerPlayGoals","powerPlayAssists","penaltyMinutes","faceOffWins","faceoffTaken","takeaways","giveaways","shortHandedGoals","shortHandedAssists","blocked","plusMinus","evenTimeOnIce","shortHandedTimeOnIce","powerPlayTimeOnIce".
        
    * The design rationale is for any game player stats in a given game, the data is all in the file called "game_skater_stats.csv", but this file doesn't contain the name of each team and the personal information of each player. "team_info.csv" contains the team information, and "player_info.csv" contains the player information, "game_skater_stats.csv" and "team_info.csv" have common variables, which are the team_id; "game_skater_stats.csv" and "player_info.csv" have common variables, which are the player_id. So we need to merge twice, the first merge is between "game_skater_stats.csv" and "team_info.csv", the new file has the team information and player stats now. The second merge is between "game_skater_stats.csv" and "player_info.csv", and the final file has all information we want now.<br />
    We find the given game first, and find those two teams and put corresponding player to their team list. Also, we drop the time link and just keep the personal link for each player.

4. Enhencement Resource - /api/results/{ID}/scoringsummary
    * a resource that represents the scoring timeline for a game
    * The player info resourse url looks like /players/DanielBriere/1977-10-06-8464975
    * List all scoring timelines for a game, the structure of each period looks like <br />
    "period 3": {<br />
    &nbsp; &nbsp; "goal 0": {<br />
      &nbsp; &nbsp; &nbsp; &nbsp; "assistents": [<br />
        &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "Jakub Voracek", <br />
        &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "Matt Carle"<br />
      &nbsp; &nbsp; &nbsp; &nbsp; ], <br />
      &nbsp; &nbsp; &nbsp; &nbsp; "current period": 4, <br />
      &nbsp; &nbsp; &nbsp; &nbsp; "current score": "(3, 4)", <br />
      &nbsp; &nbsp; &nbsp; &nbsp; "scorer": "Daniel Briere", <br />
      &nbsp; &nbsp; &nbsp; &nbsp; "scorer's link": "/players/DanielBriere/<ID>", <br />
      &nbsp; &nbsp; &nbsp; &nbsp; "the number of goals the goal scorer has in the current season": 7, <br />
      &nbsp; &nbsp; &nbsp; &nbsp; "time": "22:15"<br />
    &nbsp; &nbsp; }<br />
  }<br />
  <br />
    * The resources has been used are 
        * game_plays.csv, which provides "game_id", "current_score", "player_id", "dateTime", "period", "event". 
        * game_plays_players.csv, which provides "play_id","game_id", "play_num", "player_id", "playerType",
        * player_info.csv, which provides "player_id", "firstName", "lastName".
         <br />
    * The design rationale is for any game player stats in a given game, the data is all in the file called "game_plays.csv", but this file doesn't contain the name of each player and the player type of each player. "game_plays_players.csv" contains the player type, and "player_info.csv" contains the player information, those two files have a common variable, which is the player_id, so we merge those two files first. Then we separate the new file to two tables by player type, one is about the scorer, another is about the assist. <br />
    After this, we want to get data for all goals, which is when event = 'Goal' in "game_plays.csv". Then we can use the variable period to find corresponding information. Those information will give us the play id, and we can compare this play id with the scorer file and the assist file. Then we can find the name of scorers and assists. We also want the time of this goal in this period, which is using date time to find it. And we want the data about the score in this whole session of each scorer, so we find all goals of this scorer and add them together. <br />
    And the scorer's links just represent an assuming player info resourse, the link contains the player's name and his real ID, since we don't have this information, we leave \<ID\> there.

# User stories
1. As a sports journalist, I want data about all game results on 2012-04-29 for my report, so I can write an article to finish my job.<br />
/api/results?date=2012-04-29<br />
<br />
2. As a hokey fan, I miss the game that I had been looking forward, so I want data about performance information for this game which the game id is 2011030221 for my interest, so I can make up for this regret.<br />
/api/results/2011030221/teams<br />
<br />
3. As a gambler, I want data about all player performance statistics for each of the players that participate in a game which the game id is 2011030221 to find the best player, so I can win money from another game that still those 2 teams play.<br />
/api/results/2011030221/players<br />

# Acceptance criteria
##1.
* Ability to provide all games ID in the given date
* Ability to provide all teams' IDs and names that played the specific game
* For each game, provide:
    * "away team goals"
    * "date time"
    * "home team goals"
    * "home team id",  
    * "away team abbreviation"
    * "away team id"
    * "home team abbreviation"
    * "home team id"

##2.
*  Ability to provide those 2 teams' IDs and names
*  For each team, provide:
    * "Home or Away"
    * "face off win percentage"
    * "giveaways"
    * "goals"
    * "head coach"
    * "hits"
    * "penalties in minutes"
    * "power play goals"
    * "power play opportunities"
    * "settled in"
    * "shots"
    * "takeaways"
    * "won"

##3.
*  Ability to provide those 2 teams' ID and name
*  For each player, provide:
    * "player id"
    * "first name"
    * "last name"
    * "nationality"
    * "birth city"
    * "primary position"
    * "birth date"
    * "link",
    * "total time on ice"
    * "assists"
    * "goals"
    * "shots"
    * "hits"
    * "power play goals"
    * "power play assists"
    * "penalty minutes"
    * "face off wins"
    * "face off taken"
    * "takeaways"
    * "giveaways"
    * "short handed goals"
    * "short handed assists"
    * "blocked"
    * "plus or minus"
    * "even time on ice",
    * "short handed time on ice"
    * "power play time on ice".

