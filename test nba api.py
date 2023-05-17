from redis_api import NBAAPI
import pandas as pd
from nba_api.stats import endpoints
from nba_api.stats.static import players
from nba_api.stats.static import teams


pd.set_option('display.max_columns', None)

def get_career_stats():
    list_id, list_names = get_list_of_active_player_ids()
    print(list_id)
    api = NBAAPI(6379, 0)
    for i in range(len(list_id)):
        if not api.exists(f'{list_names[i]}Career'):
            try:
                career = endpoints.playercareerstats.PlayerCareerStats(player_id=str(list_id[i]), timeout=4)
                df = career.get_data_frames()[0]
                api.set(f'{list_names[i]}Career', df)
                print('success')
            except:
                print(f'error on {list_names[i]}')

def get_team_stats():
    list_id, list_names = get_list_of_teams_id()
    api = NBAAPI(6379, 0)
    for i in range(len(list_id)):
        if not api.exists(f'{list_names[i]}Stats'):
            try:
                stats = endpoints.teamyearbyyearstats.TeamYearByYearStats(team_id=str(list_id[i]))
                df = stats.get_data_frames()[0]
                api.set(f'{list_names[i]}Stats', df)
                list_id.remove(list_id[i])
                list_names.remove(list_names[i])
                print('success')
            except:
                print(f'error on {list_names[i]}')


def get_list_of_active_player_ids():
    list_of_ids = []
    list_of_names = []
    list_of_players = players.get_active_players()
    print(list_of_players)
    for i in range(len(list_of_players)):
        next_id = list_of_players[i]['id']
        list_of_ids.append(next_id)
        next_first_name = list_of_players[i]['first_name']
        next_last_name = list_of_players[i]['last_name']
        list_of_names.append(next_first_name + next_last_name)
    return list_of_ids, list_of_names

def get_list_of_teams_id():
    list_of_ids = []
    list_of_names = []
    list_of_teams = teams.get_teams()
    for i in range(len(list_of_teams)):
        next_id = list_of_teams[i]['id']
        list_of_ids.append(next_id)
        list_of_names.append(list_of_teams[i]['city'] + list_of_teams[i]['nickname'])
    return list_of_ids, list_of_names

def get_game_logs():
    list_id, list_names = get_list_of_active_player_ids()
    print(list_id)
    api = NBAAPI(6379, 0)
    for i in range(len(list_id)):
        if not api.exists(f'{list_names[i]}Logs'):
            try:
                career = endpoints.playergamelog.PlayerGameLog(player_id=str(list_id[i]),season='2022-23', timeout=4)
                df = career.get_data_frames()[0]
                api.set(f'{list_names[i]}Logs', df)
                print('success')
            except:
                print(f'error on {list_names[i]}')
#get_career_stats()
#get_team_stats()
#get_game_logs()
#api = NBAAPI(6379, 0)
#x = api.get('LosAngelesLakersStats')
#print(x)




