''''''
'Exploration
'There are two apis that are used:
'1) Contains player IDs, names and other general details: https://fantasy.premierleague.com/drf/elements/
'2) https://fantasy.premierleague.com/drf/element-summary/{id} has detailed stats on footballers
''''''
#import modules

import pandas as pd
import numpy as np
import requests
from time import sleep


# get list of player_ids
player_ids = requests.get('https://fantasy.premierleague.com/drf/elements/').json()

# example with Ospina (id: 0):
player_ids[0]['web_name'].encode('ascii')

# dictionary of player names put together by looping ids and player names
dict_players = {}
for n in range(len(player_ids)):
    name = player_ids[n]['web_name']
    dict_players[n] = name

# We have all player_ids. Next step: get more detailed data (split by GW) for each player
# Generate list of URLs to iterate over
# Parsing data with Kane
i = 393
kane = requests.get('https://fantasy.premierleague.com/drf/element-summary/'+str(i+1)).json()

#create function to return json object for given integer (i.e. playerID)
def player_data(i):
    return requests.get('https://fantasy.premierleague.com/drf/element-summary/'+str(i+1)).json()

# To navigate through json object, use .viewkeys() method and indices to get to gameweek-level data
# kane['history'] contains gameweek-level data
# kane['history'][0] is gameweek 1 data, and so on.

# saving all field names in the api to a variable that we can reference
fields = [u'transfers_out', u'yellow_cards', u'tackles', u'goals_conceded',
u'winning_goals', u'errors_leading_to_goal_attempt', u'saves', u'influence', u'key_passes',
u'transfers_in', u'transfers_balance', u'goals_scored', u'id', u'own_goals', u'team_h_score',
u'selected', u'creativity', u'kickoff_time_formatted', u'bonus', u'big_chances_created',
u'ict_index', u'total_points', u'penalties_missed', u'attempted_passes', u'opponent_team',
u'completed_passes', u'target_missed', u'errors_leading_to_goal', u'loaned_in', u'fixture',
u'was_home', u'recoveries', u'clean_sheets', u'assists', u'team_a_score', u'open_play_crosses',
u'clearances_blocks_interceptions', u'penalties_conceded', u'offside', u'ea_index', u'kickoff_time',
u'penalties_saved', u'fouls', u'red_cards', u'loaned_out', u'value', u'element', u'bps', u'dribbles',
u'threat', u'tackled', u'big_chances_missed', u'minutes', u'round']

# create list of dictionaries with data for gameweek 1
# testing with one row, Kane GW1
row = {'id':393,'player': dict_players[393]}
for n in range(len(fields)):
    row[fields[n]] = kane['history'][0][fields[n]]

# iterate over all players and weeks upto 9
latest_gw = 9
fpl_data = []

# generate data
for playerid in range(len(dict_players)):
    for week in range(latest_gw):
        row = {'fpl_id': playerid, 'player': dict_players[playerid]}
        fplurl = player_data(playerid)
        for n in range(len(fields)):
            row[fields[n]] = fplurl['history'][week][fields[n]]
        fpl_data.append(row)
    print dict_players[playerid] + ' done..'
    sleep(5)


''''''''''''
'Executable code
''''''''''''

import pandas as pd
import numpy as np
import requests
from time import sleep

# get list of player_ids
player_ids = requests.get('https://fantasy.premierleague.com/drf/elements/').json()

# dictionary put together by looping ids and player names
dict_players = {}
for n in range(len(player_ids)):
    name = player_ids[n]['web_name']
    dict_players[n] = name

#create function to return json object for given integer representing player id
def player_data(i):
    return requests.get('https://fantasy.premierleague.com/drf/element-summary/'+str(i+1)).json()

# save field names (from url)
fields = [u'transfers_out', u'yellow_cards', u'tackles', u'goals_conceded',
u'winning_goals', u'errors_leading_to_goal_attempt', u'saves', u'influence', u'key_passes',
u'transfers_in', u'transfers_balance', u'goals_scored', u'id', u'own_goals', u'team_h_score',
u'selected', u'creativity', u'kickoff_time_formatted', u'bonus', u'big_chances_created',
u'ict_index', u'total_points', u'penalties_missed', u'attempted_passes', u'opponent_team',
u'completed_passes', u'target_missed', u'errors_leading_to_goal', u'loaned_in', u'fixture',
u'was_home', u'recoveries', u'clean_sheets', u'assists', u'team_a_score', u'open_play_crosses',
u'clearances_blocks_interceptions', u'penalties_conceded', u'offside', u'ea_index', u'kickoff_time',
u'penalties_saved', u'fouls', u'red_cards', u'loaned_out', u'value', u'element', u'bps', u'dribbles',
u'threat', u'tackled', u'big_chances_missed', u'minutes', u'round']

# iterate over all players and weeks upto 9

# set values
latest_gw = 9
fpl_data = []

# create list of dictionaries
for playerid in range(len(dict_players)): # for each player
    fplurl = player_data(playerid) # save url for their data
    for week in range(latest_gw): # loop through all available gameweeks
        #generate row of data
        row = {'fpl_id': playerid, 'player': dict_players[playerid]}
        for n in range(len(fields)): #grab data on each field and add to dict
            row[fields[n]] = fplurl['history'][week][fields[n]]
        fpl_data.append(row) # add to list
    print dict_players[playerid] + ' done..'
    sleep(1) # to not overload api 

#convert to dataframe
fpl_data2 = pd.DataFrame(fpl_data)

#export to csv
fpl_data2.to_csv('fpldata.csv', header=True, index=False, encoding = 'utf-8')
