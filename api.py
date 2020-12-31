from flask import Flask, jsonify, abort, request
import pandas as pd

app = Flask(__name__)


# sample code for loading the team_info.csv file into a Pandas data frame.  Repeat as
# necessary for other files
def load_teams_data():
    td = pd.read_csv("./team_info.csv")
    return td

def load_game_data():
    return pd.read_csv("./game.csv")

def load_player_skater_stats():
    return pd.read_csv("./game_skater_stats.csv")

def load_game_plays():
    return pd.read_csv("./game_plays.csv")
    # return pd.read_csv("./game_plays.csv")

def load_game_paly_players_():
    return pd.read_csv("./game_plays_players.csv")
    # return pd.read_csv("./game_plays_players.csv")

def load_game_teams():
    return pd.read_csv("./game_teams_stats.csv")

def load_player_info():
    return pd.read_csv("./player_info.csv")

#global variables
player_info = load_player_info()
game_skater = load_player_skater_stats()
game_play_players_data = load_game_paly_players_()
game_play_data = load_game_plays();

team_data = load_teams_data()
game_data = load_game_data()
game_team_data = load_game_teams();




game_plays_data = load_game_data()
print("successfully loaded teams data")


@app.route('/')
def index():
    return "NHL API"
def change_time(time):
    temp = "%02d:%02d" % divmod(time, 60)
    return temp


@app.route('/api/results/<ID>/scoringsummary')
def get_scoringsummary(ID):
    game_play_data_local = game_play_data
    game_plays_chart = game_play_data_local[game_play_data_local["game_id"] == int(ID)]

    if game_plays_chart.shape[0] < 1:
        abort(404)


    game_play_player_chart = game_play_players_data
    player_info_data = player_info.loc[:, ['player_id','firstName', 'lastName','link']]
    player_info_data_with_name = pd.merge(game_play_player_chart, player_info_data, left_on="player_id", right_on="player_id")


    #get the scorer and assist chart
    score_chart = player_info_data_with_name[player_info_data_with_name["playerType"] == "Scorer"]
    assist_chart = player_info_data_with_name[player_info_data_with_name["playerType"] == "Assist"]

    #get the goal chart
    game_plays_goal = game_plays_chart[game_plays_chart["event"] == "Goal"]


    #get the period lists wich contains 3 chart
    period_len = (game_plays_goal['period']).unique().tolist()
    period_list = []
    for i in period_len:
        period_i_chart = game_plays_goal[game_plays_goal["period"] == i]
        period_list.append(period_i_chart)
    final_result = {}
    for j in range(len(period_list)):
        period = period_list[j]
        times = []
        for time in period["periodTime"]:
            times.append(change_time(time))
        scorers = []
        assistents = []
        assistents_link = []
        current_score = []
        current_period = []
        score_session_scorer = []
        for i in range(period.shape[0]):
            temp = period.iloc[i]
            goals_away = temp["goals_away"]
            goals_home = temp["goals_home"]
            current_score.append((goals_away, goals_home))
            current_period.append(temp["period"])
            discription = str(temp["description"])
            temp = discription.split("(")
            if len(temp) > 0:
                session_score = temp[1][0]
                score_session_scorer.append(session_score)

        scorer_link = []

        for play_id in period["play_id"]:
            score_chart_player = score_chart[score_chart["play_id"] == play_id]
            assist_chart_player = assist_chart[assist_chart["play_id"] == play_id]

            for i in range(score_chart_player.shape[0]):
                temp = score_chart_player.iloc[i]
                name_score = temp["firstName"] +" "+ temp["lastName"]
                name_for_link = temp["firstName"] + temp["lastName"]
                link = "/players/" + name_for_link + play_id
                scorer_link.append(link)
                scorers.append(name_score)
            assists = []  # one goal can have multiple assists
            assists_links = []
            for i in range(assist_chart_player.shape[0]):
                temp = assist_chart_player.iloc[i]
                name_assist = temp["firstName"] + " "+ temp["lastName"]
                player_idd = str(temp["player_id"])
                assist_link = "/players" + "/" +name_assist + "/" + player_idd
                assists_links.append(assist_link)
                assists.append(name_assist)
            assistents.append(assists)
            assistents_link.append(assists_links)
        result_one_period = {}
        for i in range(len(scorers)):
            item_i = {
                    "period": str(int(j) + 1),
                    "scorer": scorers[i],
                    "scorer's link": scorer_link[i],
                    "assistents": assistents[i],
                    "assistent_link":assistents_link[i],
                    "time": times[i],
                    "current score": str(current_score[i]),
                    "current period": int(current_period[i]),
                    "the number of goals the goal scorer has in the current season": int(score_session_scorer[i])
                      }
            result_one_period["goal " +str(i+1)] = item_i
        final_result["period " + str(j+1)] = result_one_period
    return jsonify(final_result)



@app.route('/api/results/<ID>/players')
def get_player(ID):
    #get the final chart
    players = player_info
    skaters = game_skater
    team = team_data
    temp_with_team_name_chart = pd.merge(skaters, team, left_on= 'team_id', right_on='team_id')
    all_chart = pd.merge(temp_with_team_name_chart, players, left_on='player_id', right_on='player_id')
    #get the right game
    game_chart = all_chart[all_chart["game_id"] == int(ID)]
    if game_chart.shape[0] < 1:
        abort(404)
    #get the team ID
    team_nums_list = (game_chart['team_id']).unique().tolist()
    #get team_1 and team_2
    if len(team_nums_list) == 2:
        team_1 = game_chart[game_chart["team_id"] == team_nums_list[0]]
        team_2 = game_chart[game_chart["team_id"] == team_nums_list[1]]
        team_1.drop(columns="link_x", inplace=True)
        team_2.drop(columns="link_x", inplace=True)

        team_1.rename(columns={"link_y": "link"}, inplace=True)
        team_1.rename(columns={"abbreviation": "team abbreviation"}, inplace=True)
        team_1.rename(columns={"birthCity": "birth city"}, inplace=True)
        team_1.rename(columns={"birthDate": "birth date"}, inplace=True)
        team_1.rename(columns={"evenTimeOnIce": "even time on ice"}, inplace=True)
        team_1.rename(columns={"faceOffWins": "face off wins"}, inplace=True)
        team_1.rename(columns={"faceoffTaken": "face off taken"}, inplace=True)
        team_1.rename(columns={"firstName": "first name"}, inplace=True)
        team_1.rename(columns={"game_id": "game id"}, inplace=True)
        team_1.rename(columns={"lastName": "last name"}, inplace=True)
        team_1.rename(columns={"penaltyMinutes": "penalty minutes"}, inplace=True)
        team_1.rename(columns={"player_id": "player id"}, inplace=True)
        team_1.rename(columns={"plusMinus": "plus or minus"}, inplace=True)
        team_1.rename(columns={"powerPlayAssists": "power play assists"}, inplace=True)
        team_1.rename(columns={"powerPlayGoals": "power play goals"}, inplace=True)
        team_1.rename(columns={"powerPlayTimeOnIce": "power play time on ice"}, inplace=True)
        team_1.rename(columns={"primaryPosition": "primary position"}, inplace=True)
        team_1.rename(columns={"shortHandedAssists": "short handed assists"}, inplace=True)
        team_1.rename(columns={"shortHandedGoals": "short handed goals"}, inplace=True)
        team_1.rename(columns={"shortHandedTimeOnIce": "short handed time on ice"}, inplace=True)
        team_1.rename(columns={"shortName": "short name of team"}, inplace=True)
        team_1.rename(columns={"teamName": "team name"}, inplace=True)
        team_1.rename(columns={"team_id": "team id"}, inplace=True)
        team_1.rename(columns={"timeOnIce": "total time on ice"}, inplace=True)

        team_2.rename(columns={"link_y": "link"}, inplace=True)
        team_2.rename(columns={"abbreviation": "team abbreviation"}, inplace=True)
        team_2.rename(columns={"birthCity": "birth city"}, inplace=True)
        team_2.rename(columns={"birthDate": "birth date"}, inplace=True)
        team_2.rename(columns={"evenTimeOnIce": "even time on ice"}, inplace=True)
        team_2.rename(columns={"faceOffWins": "face off wins"}, inplace=True)
        team_2.rename(columns={"faceoffTaken": "face off taken"}, inplace=True)
        team_2.rename(columns={"firstName": "first name"}, inplace=True)
        team_2.rename(columns={"game_id": "game id"}, inplace=True)
        team_2.rename(columns={"lastName": "last name"}, inplace=True)
        team_2.rename(columns={"penaltyMinutes": "penalty minutes"}, inplace=True)
        team_2.rename(columns={"player_id": "player id"}, inplace=True)
        team_2.rename(columns={"plusMinus": "plus or minus"}, inplace=True)
        team_2.rename(columns={"powerPlayAssists": "power play assists"}, inplace=True)
        team_2.rename(columns={"powerPlayGoals": "power play goals"}, inplace=True)
        team_2.rename(columns={"powerPlayTimeOnIce": "power play time on ice"}, inplace=True)
        team_2.rename(columns={"primaryPosition": "primary position"}, inplace=True)
        team_2.rename(columns={"shortHandedAssists": "short handed assists"}, inplace=True)
        team_2.rename(columns={"shortHandedGoals": "short handed goals"}, inplace=True)
        team_2.rename(columns={"shortHandedTimeOnIce": "short handed time on ice"}, inplace=True)
        team_2.rename(columns={"shortName": "short name of team"}, inplace=True)
        team_2.rename(columns={"teamName": "team name"}, inplace=True)
        team_2.rename(columns={"team_id": "team id"}, inplace=True)
        team_2.rename(columns={"timeOnIce": "total time on ice"}, inplace=True)


        #get team_1 player and team_2 players
        team1_players = (team_1['player id']).unique().tolist()
        team2_players = (team_2['player id']).unique().tolist()

        team1_result = []
        team2_result = []
        for player in team1_players:
            player_chart = team_1[team_1["player id"] == int(player)]

            player_dict = player_chart.to_dict('index')
            if(len(player_dict) > 0):
                firstkey = list(player_dict.keys())[0]
                temp = player_dict[firstkey]
                firstname = str(player_chart.iloc[0]['first name'])
                lastname = str(player_chart.iloc[0]['last name'])
                name = firstname + " " + lastname
                player_dict[name] = temp
                player_dict.pop(firstkey, None)
                team1_result.append(player_dict)
        for player in team2_players:
            player_chart = team_2[team_2["player id"] == int(player)]
            player_dict = player_chart.to_dict('index')
            if len(player_dict) > 0:
                firstkey = list(player_dict.keys())[0]
                temp = player_dict[firstkey]
                firstname = str(player_chart.iloc[0]['first name'])
                lastname = str(player_chart.iloc[0]['last name'])
                name = firstname + " " + lastname
                player_dict[name] = temp
                player_dict.pop(firstkey, None)
                team2_result.append(player_dict)
        result = {}

        #find the name of team
        team_name1 = find_team_name(team_1, team_nums_list[0])
        team_name2 = find_team_name(team_2, team_nums_list[1])
        result[team_name1] = team1_result
        result[team_name2] = team2_result
        return jsonify(result)
    return "U should not have two teams in one list"



def find_team_name(frame,target):
    for i in range(frame.shape[0]):
        temp = frame.iloc[i]
        if int(temp['team id']) == int(target):
            team_name_string = temp['team abbreviation']
            return team_name_string


@app.route('/api/results/<ID>/teams')
def get_team(ID):
    ori_team_game_plays = game_team_data
    team_game = ori_team_game_plays[ori_team_game_plays["game_id"] == int(ID)]
    if team_game.shape[0] < 1:
        abort(404)
    final_chart = pd.merge(team_game, team_data, left_on='team_id', right_on='team_id')
    # get the all the json type file that we need
    acc = []
    for i in range(final_chart.shape[0]):
        temp = final_chart.iloc[i]
        item = {"game id": int(temp["game_id"]),
                "team id": int(temp["team_id"]),
                "Home or Away": temp["HoA"],
                "won": bool(temp["won"]),
                "settled in": temp["settled_in"],
                "head coach": temp["head_coach"],
                "goals": int(temp["goals"]),
                "shots": int(temp["shots"]),
                "hits": int(temp["hits"]),
                "power play opportunities": int(temp["powerPlayOpportunities"]),
                "power play goals": int(temp["powerPlayGoals"]),
                "face off win percentage": float(temp["faceOffWinPercentage"]),
                "takeaways": int(temp["takeaways"]),
                "giveaways": int(temp["giveaways"]),
                "penalties in minutes": int(temp["pim"]),
                "team abbreviation": temp["abbreviation"]}
        acc.append(item)
    return jsonify(acc)



@app.route('/api/results/') #这个Syntax很奇怪
def get_date():
    date = request.args['date']
    ori_games = game_data;
    ori_teams = team_data;
    game_clean = ori_games.loc[:,['game_id','away_team_id','date_time','home_team_id','away_goals', 'home_goals']];
    team_clean = ori_teams.loc[:,['team_id', 'abbreviation']]
    #add away team id
    added_away_team = pd.merge(game_clean, team_clean, left_on='away_team_id', right_on='team_id', how='left')
    added_away_team.rename(columns={'abbreviation': 'away_abbreviation'}, inplace=True)

    #add home team id
    added_home_team_id = pd.merge(added_away_team, team_clean, left_on='home_team_id',right_on='team_id',how='left')
    added_home_team_id.rename(columns={'abbreviation': 'home_abbreviation'}, inplace=True)
    #clean final result
    result = added_home_team_id.loc[:, ['game_id', 'away_team_id','date_time', 'home_team_id', 'away_goals', 'home_goals', 'away_abbreviation',
                          'home_abbreviation']]

    #get the dates that is in the result
    dates = result[result['date_time'] == date]

    # return 404 if there isn't one team
    if dates.shape[0] < 1:
        abort(404)

    #get the all the json type file that we need
    acc = []
    for i in range(dates.shape[0]):
        temp = dates.iloc[i]
        item = {"game id": int(temp["game_id"]),
                "away team id": int(temp["away_team_id"]),
                "date time": temp["date_time"],
                "away team goals": int(temp["away_goals"]),
                "home team vs away team": temp["home_abbreviation"] +"vs"+temp["away_abbreviation"],
                "final goals home vs away": str(int(temp["home_goals"])) +"vs"+
                str(int(temp["away_goals"])),

                "home team id": int(temp["home_team_id"]),
                "home team goals": int(temp["home_goals"]),
                "away team abbreviation": temp["away_abbreviation"],
                "home team abbreviation": temp["home_abbreviation"]}
        acc.append(item)
    return jsonify(acc)




# route mapping for HTTP GET on /api/schedule/TOR
@app.route('/api/teams/<string:team_id>', methods=['GET'])
def get_task(team_id):
    # fetch sub dataframe for all teams (hopefully 1) where abbreviation=team_id
    teams = team_data[team_data["abbreviation"] == team_id]

    # return 404 if there isn't one team
    if teams.shape[0] < 1:
        abort(404)

    # get first team
    team = teams.iloc[0]

    # return customized JSON structure in lieu of Pandas Dataframe to_json method
    teamJSON = {"abbreviation": team["abbreviation"],
                "city": team["shortName"],
                "name": team["teamName"]}

    # jsonify easly converts maps to JSON strings
    return jsonify(teamJSON)


if __name__ == '__main__':
    app.run(debug=True)
