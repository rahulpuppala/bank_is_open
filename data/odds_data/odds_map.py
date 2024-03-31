import numpy as np
import pandas as pd
import json
import glob
from pybettor import convert_odds, implied_odds


#Quarter has to be Q1, Q2, Q3, or Q4
def comeback(game,quarter):
    if(game['Total Spread '+quarter]<0):
        if(game['Winner']=='H'):
            return True
    elif(game['Total Spread '+quarter]>0):
        if(game['Winner']=='V'):
            return True
    return False


# Path to the directory containing the Excel files
path = '*.xlsx'

# Get a list of all Excel files in the directory
files = glob.glob(path)
dfs = []

# Read each Excel file into a dataframe and append it to the list
for file in files:
    temp = pd.read_excel(file)
    dfs.append(temp)

# Concatenate all dataframes in the list into a single dataframe
df = pd.concat(dfs, ignore_index=True)

df['Game_ID'] = df.index // 2 + 1
# Display the first few rows of the DataFrame

games = [group for _, group in df.groupby(df.index // 2)]

game_data = []

for game in games:


    spread_q1 = game.iloc[1]['1st'] - game.iloc[0]['1st']
    spread_q2 = game.iloc[1]['2nd'] - game.iloc[0]['2nd']
    spread_q3 = game.iloc[1]['3rd'] - game.iloc[0]['3rd']
    spread_q4 = game.iloc[1]['4th'] - game.iloc[0]['4th']

    total_spread_q1 = spread_q1
    total_spread_q2 = total_spread_q1 + spread_q2
    total_spread_q3 = total_spread_q2 + spread_q3
    total_spread_q4 = total_spread_q3 + spread_q4
    
    winner = 'H' if game.iloc[1]['Final'] > game.iloc[0]['Final'] else 'V'
    game_stats = {
        'Game': game.iloc[0]['Game_ID'],
        'Home Team': game.iloc[1]['Team'],
        'Visitor Team': game.iloc[0]['Team'],
        'Spread Q1': spread_q1,
        'Spread Q2': spread_q2,
        'Spread Q3': spread_q3,
        'Spread Q4': spread_q4,
        'Total Spread Q1': total_spread_q1,
        'Total Spread Q2': total_spread_q2,
        'Total Spread Q3': total_spread_q3,
        'Total Spread Q4': total_spread_q4,
        'Winner': winner
    }
    game_data.append(game_stats)

q1_odds_map={}
q2_odds_map={}
q3_odds_map={}
q4_odds_map={}

max_spread= 0
min_spread = 0
max_game=0
min_game=0
counter = 0
for game in game_data:
    if(game['Total Spread Q1']>max_spread):
        max_spread = game['Total Spread Q1']
        max_game = counter
    if(game['Total Spread Q2']>max_spread):
        max_spread = game['Total Spread Q2']
        max_game = counter 
    if(game['Total Spread Q3']>max_spread):
        max_spread = game['Total Spread Q3']
        max_game = counter 
    if(game['Total Spread Q4']>max_spread):
        max_spread = game['Total Spread Q4']
        max_game = counter 

    if(game['Total Spread Q1']<min_spread):
        min_spread = game['Total Spread Q1']
        min_game = counter
    if(game['Total Spread Q2']<min_spread):
        min_spread = game['Total Spread Q2']
        min_game = counter 
    if(game['Total Spread Q3']<min_spread):
        min_spread = game['Total Spread Q3']
        min_game = counter 
    if(game['Total Spread Q4']<min_spread):
        min_spread = game['Total Spread Q4']
        min_game = counter 
    counter+=1
print(max_spread)
print(min_spread)

#tuple value is comebacks, games total, percentage
#for(0 spread) home team winning is tracked
all_odds_maps=[]
for i in range(0,4):
    odds_map = {}
    for j in range(min_spread,max_spread+1):
        odds_map[str(j)] = (float(0),float(0),float(0))
    all_odds_maps.append(odds_map)
for game in game_data:
    for i in range (1,5):
        (comebacks,games_occured,percentage) = all_odds_maps[i-1][str(game['Total Spread Q'+str(i)])]
        games_occured+=1
        comebacks+=1 if comeback(game,'Q'+str(i)) else 0
        all_odds_maps[i-1][str(game['Total Spread Q'+str(i)])] = (comebacks,games_occured,comebacks/games_occured)


for i in range(1,5):    
    with open('q'+str(i)+'_odds_map.json', 'w') as file:
        file.write(json.dumps(all_odds_maps[i-1]))


#validation
# total_games=0
# for spread in q2_odds_map:
#     (comebacks,games_occured,percentage) = q1_odds_map[spread]
#     total_games+=games_occured
# print(total_games)
# print(df['Game_ID'].max())



i = 544
print(game_data[i])
print(df[df['Game_ID']==game_data[i]['Game']])
print(comeback(game_data[i],'Q1'))
print(comeback(game_data[i],'Q2'))
print(comeback(game_data[i],'Q3'))
print(comeback(game_data[i],'Q4'))