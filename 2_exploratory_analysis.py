''''''
'Exploratory Analysis
'Summary statistics and visuals on scraped data
''''''''''''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Check the documentation for '%matplotlib' to be able to work interactively
%matplotlib qt

# Increase figure and font sizes for easier viewing
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

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

# Read in FPL data, use first row as column headers
fpldata = pd.read_csv('fpldata.csv')

# Top FPL players (points)
fpldata.groupby('player').total_points.sum().sort_values(ascending=False)

# Rank by goals scored
fpldata.groupby('player').goals_scored.sum().sort_values(ascending=False)

# Rank by number of assists
fpldata.groupby('player').assists.sum().sort_values(ascending=False)

# Function to group, sum and sort by a particular column (top 10)
def csort(field):
    if field in fields:
        x = fpldata.groupby('player')[field].sum().sort_values(ascending=False)
        return x.head(10)
    else:
        return 'Field not in dataset. Try another.'

csort('completed_passes')
csort('saves')
csort('yellow_cards')

# Rank by points per minutes played
fplagg = fpldata.groupby('player').sum()
(fplagg.total_points / fplagg.minutes).sort_values(ascending=False)


# To-do: filter by number of gameweeks
# Visualisations
