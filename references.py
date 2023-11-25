import datetime
import pandas as pd
import json



data_players = pd.read_csv(f"data/new_all_outfield_player_data.csv", index_col = 0)
data_squads = pd.read_csv(f"data/Squads_all_data.csv", index_col = 0)
curr_year = datetime.date.today().year
curr_month = datetime.date.today().month

if curr_month >= 7:
  curr_season = f'{curr_year}-{curr_year + 1}'
else:
  curr_season = f'{curr_year - 1}-{curr_year}'
  
years = [year for year in range(2017, 2024)]


######################################################  COMPARISONS PAGE  ######################################################


#### Data Reference ####

min_played_col = 'Playing Time - Min'
league_col = 'Comp'
pos_col = 'Pos'

summary_cols = ['Player', 'Squad', 
                    'Season', 'Comp',
                    'Age', 'Pos',
                    'Nation']

leave_out_player = ['Player', 'Squad', 
                 'Season', 'Comp',
                 'Nation', 'Pos']

#leave_out_club = 

scale_to_options = ['Individual Seasons', 'All Selected Seasons', 'All Seasons']
scale_against_options = ['All Players', 'League', 'Position', 'Age Group']


########################


#### Data Cleaning ####

deletes = ['Matches', 'Rk']

########################


#### UI Reference ####

theta_column_name = 'Stats'
radii_column_name = 'Percentile'

figure_colors = ['blue', 'red', 'green', 'yellow', 'purple', 'brown']

discrete_palettes = { 'blue' : ['blue', '#190482', '#7752FE', '#8E8FFA', '#C2D9FF'],
                    'red' : ['red', '#22092C', '#872341', '#BE3144', '#F05941'],
                    'green' : ['green', '#618264', '#79AC78', '#B0D9B1', '#D0E7D2'],
                    'yellow' : ['yellow', '#FFEECC', '#FFDDCC', '#FFCCCC', '#FEBBCC'],
                    'purple' : ['purple', '#610C9F','#940B92','#DA0C81', '#E95793'],
                     'brown' : ['brown', '#6C3428', '#BA704F', '#DFA878', '#CEE6F3']
                     }

########################



######################################################  SCREENER PAGE  ######################################################

# 'GK' 
positions = list(data_players.Pos.unique())
leagues = list(data_players.Comp.unique())


curr_year = int(datetime.datetime.now().year)
starting_year = 2017


iso_codes = pd.read_json("data/country_iso_codes.json", typ = 'series').to_dict()
iso_codes = dict((y, x) for x, y in iso_codes.items())
country_names = pd.read_json("data/country_names.json", typ = 'series').to_dict()

inverse_cols = ['Challenges Lost', 'PKs conceded', 
                    'Own Goals', 'Errors', 'Miscontrols', 
                    'Dispossessed']

stats_available = ['Standard Stats', 'Shooting Stats', 'Passing Stats',
                    'Pass Type Stats','Shot and Goal Creation Stats',
                    'Defensive Stats','Possession Stats','Playing Time Stats',
                    'Misc Stats','Goalkeeping Stats']


stats_of_interest = ['Standard Stats', 'Shooting Stats', 'Passing Stats',
      'Shot and Goal Creation Stats', 'Possession Stats', 'Defensive Stats']
stats_of_interest_gk = ['Goalkeeping Stats']


important_stats_player = {'Standard Stats' : ['Performance - Gls', 'Performance - Ast',
                                       'Performance - PK', 'Per 90 Minutes - Gls', 'Per 90 Minutes - G+A', 
                                       'Expected - npxG', 'Expected - xAG'],
                   'Shooting Stats' : ["Standard - Gls", 'Standard - SoT', 'Standard - G/SoT',
                                       'Standard - SoT/90', 'Standard - FK',
                                        'Expected - npxG', 'Expected - np:G-xG'],
                   'Passing Stats' : ['Total - Cmp', 'Total - Cmp%', 'Short - Cmp', 'Short - Cmp%',
                                      'Medium - Cmp', 'Medium - Cmp%', 'Long - Cmp', 'Long - Cmp%', 
                                      'Ast', 'xA', 'KP',
                                      '1/3', 'PPA', 'CrsPA', 'PrgP'],
                   'Pass Type Stats' : ['Att', 'Pass Type - Crs', 'Outcomes - Cmp', 
                                        'Outcomes - Off', 'Outcomes - Blocks'],
                   'Shot and Goal Creation Stats' : ['SCA - SCA', 'SCA - SCA90', 'SCA Types - TO',
                                                     'GCA - GCA', 'GCA - GCA90', 'GCA Types - TO', 'GCA Types - Fld',
                                                     'GCA Types - Def'],
                   'Defensive Stats' : ['Tackles - Tkl', 'Tackles - TklW', 'Tackles - Def 3rd', 
                                        'Tackles - Mid 3rd', 'Tackles - Att 3rd', 'Challenges - Tkl',
                                        'Blocks - Blocks', 'Blocks - Sh', 'Int', 'Tkl+Int', 'Clr', 'Err'],
                   'Possession Stats' : ['Touches - Touches', 'Touches - Def 3rd', 'Touches - Mid 3rd', 
                                         'Touches - Att 3rd', 'Take-Ons - Succ', 
                                         'Carries - Mis', 'Carries - Dis', 'Receiving - Rec'],
                   'Playing Time Stats' : ['Playing Time - Min', 'Playing Time - Min%', 'Starts - Starts', 
                         'Starts - Compl', 'Subs - Subs', 'Subs - Mn/Sub', 'Team Success - PPM', 
                         'Team Success - +/-', 'Team Success (xG) - onxG'],
                   'Misc Stats' : ['Performance - CrdY', 'Performance - CrdR', 'Performance - Fls', 
                                   'Performance - PKwon', 'Performance - OG', 'Aerial Duels - Won%'],
                   'Goalkeeping Stats' : ['Performance - GA', 'Performance - GA90', 'Performance - SoTA', 
                                          'Performance - Saves', 'Performance - Save%', 
                                          'Performance - CS', 'Performance - CS%',
                                          'Penalty Kicks - PKatt', 'Penalty Kicks - Save%']}

important_stats_comp = {'Standard Stats' : ['Performance - Gls', 'Performance - Ast',
                                       'Performance - PK', 'Per 90 Minutes - Gls', 'Per 90 Minutes - G+A', 
                                       'Expected - npxG', 'Expected - xAG'],
                   'Shooting Stats' : ["Standard - Gls", 'Standard - SoT', 'Standard - G/SoT',
                                       'Standard - SoT/90', 'Standard - FK',
                                        'Expected - npxG', 'Expected - np:G-xG'],
                   'Passing Stats' : ['Total - Cmp', 'Total - Cmp%', 'Short - Cmp', 'Short - Cmp%',
                                      'Medium - Cmp', 'Medium - Cmp%', 'Long - Cmp', 'Long - Cmp%', 
                                      'Ast', 'xA', 'KP',
                                      '1/3', 'PPA', 'CrsPA', 'PrgP'],
                   'Pass Type Stats' : ['Att', 'Pass Types - Crs', 
                                        'Outcomes - Cmp', 'Pass Types - TB', 'Pass Types - Sw',
                                        'Outcomes - Off', 'Outcomes - Blocks'],
                   'Shot and Goal Creation Stats' : ['SCA - SCA', 'SCA - SCA90', 'SCA Types - Drib',
                                                     'GCA - GCA', 'GCA - GCA90', 'GCA Types - Drib', 'GCA Types - Fld',
                                                     'GCA Types - Def'],
                   'Defensive Stats' : ['Tackles - Tkl', 'Tackles - TklW', 'Tackles - Def 3rd', 
                                        'Tackles - Mid 3rd', 'Tackles - Att 3rd', 'Challenges - Tkl',
                                        'Blocks - Blocks', 'Blocks - Sh', 'Int', 'Tkl+Int', 'Clr', 'Err'],
                   'Possession Stats' : ['Touches - Touches', 'Touches - Def 3rd', 'Touches - Mid 3rd', 
                                         'Touches - Att 3rd', 'Take-Ons - Succ', 
                                         'Carries - Mis', 'Carries - Dis', 'Receiving - Rec'],
                   'Playing Time Stats' : ['Playing Time - Min', 'Playing Time - Min%', 'Starts - Starts', 
                         'Starts - Compl', 'Subs - Subs', 'Subs - Mn/Sub', 'Team Success - PPM', 
                         'Team Success - +/-', 'Team Success (xG) - onxG'],
                   'Misc Stats' : ['Performance - CrdY', 'Performance - CrdR', 'Performance - Fls', 
                                   'Performance - PKwon', 'Performance - OG', 'Aerial Duels - Won%'],
                   'Goalkeeping Stats' : ['Performance - GA', 'Performance - GA90', 'Performance - SoTA',
                                          'Performance - Saves','Performance - Save%', 
                                          'Performance - CS', 'Performance - CS%',
                                          'Penalty Kicks - PKatt', 'Penalty Kicks - Save%']}


important_stats_squad = {'Standard Stats' : ['Performance - Gls', 'Performance - Ast',
                                       'Performance - PK', 'Per 90 Minutes - Gls', 'Per 90 Minutes - G+A', 
                                       'Expected - npxG', 'Expected - xAG'],
                   'Shooting Stats' : ["Standard - Gls", 'Standard - SoT', 'Standard - G/SoT',
                                       'Standard - SoT/90', 'Standard - FK',
                                        'Expected - npxG', 'Expected - np:G-xG'],
                   'Passing Stats' : ['Total - Cmp', 'Total - Cmp%', 'Short - Cmp', 'Short - Cmp%',
                                      'Medium - Cmp', 'Medium - Cmp%', 'Long - Cmp', 'Long - Cmp%', 
                                      'Ast', 'xA', 'KP',
                                      '1/3', 'PPA', 'CrsPA', 'Prog'],
                   'Pass Type Stats' : ['Att', 'Pass Type - Crs', 'Outcomes - Cmp', 
                                        'Outcomes - Off', 'Outcomes - Blocks'],
                   'Shot and Goal Creation Stats' : ['SCA - SCA', 'SCA - SCA90', 'SCA Types - Drib',
                                                     'GCA - GCA', 'GCA - GCA90', 'GCA Types - Drib', 'GCA Types - Fld',
                                                     'GCA Types - Def'],
                   'Defensive Stats' : ['Tackles - Tkl', 'Tackles - TklW', 'Tackles - Def 3rd', 
                                        'Tackles - Mid 3rd', 'Tackles - Att 3rd', 'Challenges - Tkl',
                                        'Blocks - Blocks', 'Blocks - Sh', 'Int', 'Tkl+Int', 'Clr', 'Err'],
                   'Possession Stats' : ['Poss','Touches - Touches', 'Touches - Def 3rd', 'Touches - Mid 3rd', 
                                         'Touches - Att 3rd', 'Dribbles - Succ', 
                                         'Dribbles - Mis', 'Dribbles - Dis', 'Receiving - Rec'],
                   'Playing Time Stats' : ['Playing Time - Min', 'Playing Time - Min%', 'Starts - Starts', 
                         'Starts - Compl', 'Subs - Subs', 'Subs - Mn/Sub', 'Team Success - PPM', 
                         'Team Success - +/-', 'Team Success (xG) - onxG'],
                   'Misc Stats' : ['Performance - CrdY', 'Performance - CrdR', 'Performance - Fls', 
                                   'Performance - PKwon', 'Performance - OG', 'Aerial Duels - Won%'],
                   'Goalkeeping Stats' : ['Performance - GA', 'Performance - GA90', 'Performance - SoTA',
                                          'Performance - Saves','Performance - Save%', 
                                          'Performance - CS', 'Performance - CS%',
                                          'Penalty Kicks - PKatt', 'Penalty Kicks - Save%']}



screener_available_stats = {
                            ### Goals ###
                            'Goals' : 'Performance - Gls',
                            'Goals per 90' : 'Per 90 Minutes - Gls',
                            'Goals + Assists' : 'Performance - G+A',
                            'Goals + Assists per 90' : 'Per 90 Minutes - G+A',
                            'Penalty Kicks' : 'Performance - PK',
                            'Non-Penalty G+A per 90' : 'Per 90 Minutes - G+A-PK',
                            'Goals per Shot' : 'Standard - G/Sh',
                            'Goals per SoT' : 'Standard - G/SoT',
                            
                            
                            ### Shooting ###
                            'Shots' : 'Standard - Sh',
                            'Shots per 90' : 'Standard - Sh/90',
                            'Shots on Target' : 'Standard - SoT',
                            'SoT per 90' : 'Standard - SoT/90',
                            'SoT %' : 'Standard - SoT%',
                            'Avg Shot Distance' : 'Standard - Dist',
                            'Free Kick Shots' : 'Standard - FK',
                            'Penalty Kicks Attempted' : 'Standard - PKatt',
                            'xG' : 'Expected - xG',
                            'Non-Penalty Expected Goals' : 'Expected - npxG',
                            'Non-Penalty Expected Goals per Shot' : 'Expected - npxG/Sh',
                            'Goals minus xG' : 'Expected - G-xG',
                            'Non-Penalty Goals - npxG' : 'Expected - np:G-xG',
                            
                            
                            ### Passing ###
                            'Assists' : 'Ast',
                            'Assists per 90' : 'Per 90 Minutes - Ast',
                            'Total Passing Distance' : 'Total - TotDist',
                            'Progressive Passing Distance' : 'Total - PrgDist',
                            'Passes Completed' : 'Total - Cmp',
                            'Pass Completion %' : 'Total - Cmp%',
                            'Crosses' : 'Performance - Crs',
                            'Short Passes Completed' : 'Short - Cmp',
                            'Short Pass Completion %' : 'Short - Cmp%',
                            'Medium Passes Completed' : 'Medium - Cmp',
                            'Medium Pass Completion %' : 'Medium - Cmp%',
                            'Long Passes Completed' : 'Long - Cmp',
                            'Long Pass Completion %' : 'Long - Cmp%',
                            'Expected Assists' : 'xA',
                            'Assists - xA' : 'A-xAG',
                            'Key Passes' : 'KP',
                            'Passes into Final 3rd' : '1/3',
                            'Passes into PA' : 'PPA',
                            'Crosses into PA' : 'CrsPA',
                            'Progressive Passes' : 'PrgP',
                            'Through-Balls' : 'Pass Types - TB',
                            'Switches' : 'Pass Types - Sw',
                            'Corners Taken' : 'Pass Types - CK',
                            'In-Swinging Corners' : 'Corner Kicks - In',
                            'Out-Swinging Corners' : 'Corner Kicks - Out',
                            'Passes Blocked' : 'Outcomes - Blocks',
                            
                            
                            ### Shot and Goal Creation Stats ###
                            'Shot-Creating Actions' : 'SCA - SCA',
                            'Shot-Creating Actions per 90' : 'SCA - SCA90',
                            'Liveball Pass leading to Shot' : 'SCA Types - PassLive',
                            'Deadball Pass leading to Shot' : 'SCA Types - PassDead',
                            'Take-ons leading to Shot' : 'SCA Types - TO',
                            'Shots leading to Shot' : 'SCA Types - Sh',
                            'Defensive Actions leading to Shot' : 'SCA Types - Def',
                            'Liveball Pass leading to Goals' : 'GCA Types - PassLive',
                            'Deadball Pass leading to Goals' : 'GCA Types - PassDead',
                            'Take-ons leading to Goals' : 'GCA Types - TO',
                            'Shots leading to Goals' : 'GCA Types - Sh',
                            'Defensive Actions leading to Goals' : 'GCA Types - Def',
                            
                            
                            ### Possession Stats ###
                            'Touches' : 'Touches - Touches',
                            'Touches - Def Pen' : 'Touches - Def Pen',
                            'Touches - Def 3rd' : 'Touches - Def 3rd',
                            'Touches - Mid 3rd' : 'Touches - Mid 3rd',
                            'Touches - Att 3rd' : 'Touches - Att 3rd',
                            'Touches - Att Pen' : 'Touches - Att Pen',
                            'Take-Ons - Att' : 'Take-Ons - Att',
                            'Successful Take-Ons' : 'Take-Ons - Succ',
                            'Take-Ons - Succ%' : 'Take-Ons - Succ%',
                            'Take-Ons - Tackled' : 'Take-Ons - Tkld',
                            'Carries' : 'Carries - Carries',
                            'Carries - TotDist' : 'Carries - TotDist',
                            'Carries - PrgDist' : 'Carries - PrgDist',
                            'Progressive Carries' : 'Carries - PrgC',
                            'Carries into Final 3rd' : 'Carries - 1/3',
                            'Carries into PA' : 'Carries - CPA',
                            'Miscontrols' : 'Carries - Mis',
                            'Dispossessed' : 'Carries - Dis',
                            'Passes Received' : 'Receiving - Rec',
                            'Progressive Passes Received' : 'Receiving - PrgR',
                            'PKs won' : 'Performance - PKwon',
                            
                            
                            ### Defensive Stats ###
                            'Tackles Attempted' : 'Tackles - Tkl',
                            'Tackles Won' : 'Tackles - TklW',
                            'Tackles - Def 3rd' : 'Tackles - Def 3rd',
                            'Tackles - Mid 3rd' : 'Tackles - Mid 3rd',
                            'Tackles - Att 3rd' : 'Tackles - Att 3rd',
                            'Dribblers Tackled' : 'Challenges - Tkl',
                            'Dribbles Challenged' : 'Challenges - Att',
                            'Challenges Lost' : 'Challenges - Lost',
                            '% of Dribblers Tackled' : 'Challenges - Tkl%',
                            'Interceptions' : 'Int',
                            'Tackles + Interceptions' : 'Tkl+Int',
                            'Blocks' : 'Blocks - Blocks',
                            'Shots Blocked' : 'Blocks - Sh',
                            'Passes Blocked' : 'Blocks - Pass',
                            'PKs conceded' : 'Performance - PKcon',
                            'Own Goals' : 'Performance - OG',
                            'Clearances' : 'Clr',
                            'Errors' : 'Err',
                            'Aerial Duels - Won' : 'Aerial Duels - Won',
                            'Aerial Duels - Lost' : 'Aerial Duels - Lost',
                            '% Aerial Duels Won' : 'Aerial Duels - Won%',
                            
                            
                            ### Playing Time Stats ###
                            'Starts' : 'Starts - Starts',
                            'Minutes Played' : 'Playing Time - Min', 
                            'Minutes per Start' : 'Starts - Mn/Start',
                            'Substitute Appearances' : 'Subs - Subs',
                            'Minutes per Sub' : 'Subs - Mn/Sub',
                            'Team Points per Appearance' : 'Team Success - PPM',
                            'Team Goals while on Pitch' : 'Team Success - onG',
                            'Team GA while on Pitch' : 'Team Success - onGA',
                            'Plus/Minus Goals while on Pitch' : 'Team Success - +/-',
                            'Team xG while on Pitch' : 'Team Success (xG) - onxG',
                            
                            
                            ### Misc Stats ###
                            'Yellow Cards' : 'Performance - CrdY',
                            'Second Yellows' : 'Performance - 2CrdY',
                            'Red Cards' : 'Performance - CrdR',
                            'Fouls' : 'Performance - Fls',
                            'Foul Drawn' : 'Performance - Fld'
                            
                            }


positions = ['FW', 'MF', 'DF', 'GK']

pos = ['Pure Forward', 'Attacker', 
       'Pure Midfielder', 'Flex Forward',
       'Pure Defender', 'Attacking Defender', 
       'Goalkeeper']
available_competitions = ['Premier League', 'Ligue 1', 'Serie A', 'La Liga', 'Bundesliga']


grouped_stats_player_comparison = {
                            ### Goals ###
                            
                            'Goalscoring':
                                  {'Goals' : 'Performance - Gls',
                                    'Goals per 90' : 'Per 90 Minutes - Gls',
                                    'Penalty Kicks' : 'Performance - PK',
                                    'Non-Penalty G+A per 90' : 'Per 90 Minutes - G+A-PK',
                                    'Goals per Shot' : 'Standard - G/Sh',
                                    'Goals per SoT' : 'Standard - G/SoT',
                                    'xG' : 'Expected - xG',
                                    'Goals minus xG' : 'Expected - G-xG',
                                    'Non-Penalty Expected Goals' : 'Expected - npxG',
                                    'Non-Penalty Goals - npxG' : 'Expected - np:G-xG'},
                            
                            ### Shooting ###
                            'Shooting' : 
                                  {'Shots' : 'Standard - Sh',
                                    'Shots per 90' : 'Standard - Sh/90',
                                    'Shots on Target' : 'Standard - SoT',
                                    'SoT per 90' : 'Standard - SoT/90',
                                    'SoT %' : 'Standard - SoT%',
                                    'Avg Shot Distance' : 'Standard - Dist',
                                    'Non-Penalty Expected Goals per Shot' : 'Expected - npxG/Sh',},
                            
                            
                            
                            ### Passing ###
                            'Passing': 
                                  {'Assists' : 'Ast',
                                    'Assists per 90' : 'Per 90 Minutes - Ast',
                                    'Total Passing Distance' : 'Total - TotDist',
                                    'Progressive Passing Distance' : 'Total - PrgDist',
                                    'Passes Completed' : 'Total - Cmp',
                                    'Pass Completion %' : 'Total - Cmp%',
                                    'Crosses' : 'Performance - Crs',
                                    'Short Passes Completed' : 'Short - Cmp',
                                    'Short Pass Completion %' : 'Short - Cmp%',
                                    'Medium Passes Completed' : 'Medium - Cmp',
                                    'Medium Pass Completion %' : 'Medium - Cmp%',
                                    'Long Passes Completed' : 'Long - Cmp',
                                    'Long Pass Completion %' : 'Long - Cmp%',
                                    'Expected Assists' : 'xA',
                                    'Assists - xA' : 'A-xAG',
                                    'Key Passes' : 'KP',
                                    'Passes into Final 3rd' : '1/3',
                                    'Passes into PA' : 'PPA',
                                    'Crosses into PA' : 'CrsPA',
                                    'Progressive Passes' : 'PrgP',
                                    'Through-Balls' : 'Pass Types - TB',
                                    'Switches' : 'Pass Types - Sw',
                                    },
                            
                            
                            ### Shot and Goal Creation Stats ###
                            'Creation' : 
                                  {'Shot-Creating Actions' : 'SCA - SCA',
                                    'Shot-Creating Actions per 90' : 'SCA - SCA90',
                                    'Liveball Pass leading to Shot' : 'SCA Types - PassLive',
                                    'Deadball Pass leading to Shot' : 'SCA Types - PassDead',
                                    'Take-ons leading to Shot' : 'SCA Types - TO',
                                    'Shots leading to Shot' : 'SCA Types - Sh',
                                    'Defensive Actions leading to Shot' : 'SCA Types - Def',
                                    'Liveball Pass leading to Goals' : 'GCA Types - PassLive',
                                    'Deadball Pass leading to Goals' : 'GCA Types - PassDead',
                                    'Take-ons leading to Goals' : 'GCA Types - TO',
                                    'Shots leading to Goals' : 'GCA Types - Sh',
                                    'Defensive Actions leading to Goals' : 'GCA Types - Def'},
                            
                            
                            ### Possession Stats ###
                            'Skills' : 
                                  {'Touches' : 'Touches - Touches',
                                    'Touches - Def Pen' : 'Touches - Def Pen',
                                    'Touches - Def 3rd' : 'Touches - Def 3rd',
                                    'Touches - Mid 3rd' : 'Touches - Mid 3rd',
                                    'Touches - Att 3rd' : 'Touches - Att 3rd',
                                    'Touches - Att Pen' : 'Touches - Att Pen',
                                    'Take-Ons - Att' : 'Take-Ons - Att',
                                    'Successful Take-Ons' : 'Take-Ons - Succ',
                                    'Take-Ons - Succ%' : 'Take-Ons - Succ%',
                                    'Take-Ons - Tackled' : 'Take-Ons - Tkld',
                                    'Carries' : 'Carries - Carries',
                                    'Carries - TotDist' : 'Carries - TotDist',
                                    'Carries - PrgDist' : 'Carries - PrgDist',
                                    'Progressive Carries' : 'Carries - PrgC',
                                    'Carries into Final 3rd' : 'Carries - 1/3',
                                    'Carries into PA' : 'Carries - CPA',
                                    'Miscontrols' : 'Carries - Mis',
                                    'Dispossessed' : 'Carries - Dis',
                                    'Progressive Passes Received' : 'Receiving - PrgR',
                                    'PKs won' : 'Performance - PKwon'},
                            
                            
                            ### Defensive Stats ###
                            'Defense' : 
                                  {'Tackles Attempted' : 'Tackles - Tkl',
                                    'Tackles Won' : 'Tackles - TklW',
                                    'Tackles - Def 3rd' : 'Tackles - Def 3rd',
                                    'Tackles - Mid 3rd' : 'Tackles - Mid 3rd',
                                    'Tackles - Att 3rd' : 'Tackles - Att 3rd',
                                    'Dribblers Tackled' : 'Challenges - Tkl',
                                    'Dribbles Challenged' : 'Challenges - Att',
                                    'Challenges Lost' : 'Challenges - Lost',
                                    '% of Dribblers Tackled' : 'Challenges - Tkl%',
                                    'Interceptions' : 'Int',
                                    'Tackles + Interceptions' : 'Tkl+Int',
                                    'Blocks' : 'Blocks - Blocks',
                                    'Shots Blocked' : 'Blocks - Sh',
                                    'Passes Blocked' : 'Blocks - Pass',
                                    'PKs conceded' : 'Performance - PKcon',
                                    'Own Goals' : 'Performance - OG',
                                    'Clearances' : 'Clr',
                                    'Errors' : 'Err',
                                    'Aerial Duels - Won' : 'Aerial Duels - Won',
                                    'Aerial Duels - Lost' : 'Aerial Duels - Lost',
                                    '% Aerial Duels Won' : 'Aerial Duels - Won%'},
                            
                            
                            
                            ### Playing Time Stats ###
                            'Playing Time' : 
                                  {'Starts' : 'Starts - Starts',
                                    'Minutes Played' : 'Playing Time - Min', 
                                    'Minutes per Start' : 'Starts - Mn/Start',
                                    'Substitute Appearances' : 'Subs - Subs',
                                    'Minutes per Sub' : 'Subs - Mn/Sub',
                                    'Team Points per Appearance' : 'Team Success - PPM',
                                    'Team Goals while on Pitch' : 'Team Success - onG',
                                    'Team GA while on Pitch' : 'Team Success - onGA',
                                    'Plus/Minus Goals while on Pitch' : 'Team Success - +/-',
                                    'Team xG while on Pitch' : 'Team Success (xG) - onxG'},
                            
                            
                            
                            ### Misc Stats ###
                            'Misc' : 
                                  {'Yellow Cards' : 'Performance - CrdY',
                                    'Second Yellows' : 'Performance - 2CrdY',
                                    'Red Cards' : 'Performance - CrdR',
                                    'Fouls' : 'Performance - Fls',
                                    'Foul Drawn' : 'Performance - Fld'}
                            
                            }


new_grouped_stats_player_comparison = {'Goalscoring': 
      {'Goals': {'normal_name': 'Performance - Gls',
      'per_90_name': 'Performance - Gls per 90',
      'is_inverse': False},
      'Penalty Kicks': {'normal_name': 'Performance - PK',
      'per_90_name': 'Performance - PK per 90',
      'is_inverse': False},
      'Goals per Shot': {'normal_name': 'Standard - G/Sh',
      'per_90_name': 'Standard - G/Sh per 90',
      'is_inverse': False},
      'Goals per SoT': {'normal_name': 'Standard - G/SoT',
      'per_90_name': 'Standard - G/SoT per 90',
      'is_inverse': False},
      'xG': {'normal_name': 'Expected - xG',
      'per_90_name': 'Expected - xG per 90',
      'is_inverse': False},
      'Goals minus xG': {'normal_name': 'Expected - G-xG',
      'per_90_name': 'Expected - G-xG per 90',
      'is_inverse': False},
      'Non-Penalty Expected Goals': {'normal_name': 'Expected - npxG',
      'per_90_name': 'Expected - npxG per 90',
      'is_inverse': False},
      'Non-Penalty Goals - npxG': {'normal_name': 'Expected - np:G-xG',
      'per_90_name': 'Expected - np:G-xG per 90',
      'is_inverse': False}},
  'Shooting': 
    {'Shots': {'normal_name': 'Standard - Sh',
    'per_90_name': 'Standard - Sh per 90',
    'is_inverse': False},
    'Shots on Target': {'normal_name': 'Standard - SoT',
    'per_90_name': 'Standard - SoT per 90',
    'is_inverse': False},
    'SoT %': {'normal_name': 'Standard - SoT%',
    'per_90_name': 'Standard - SoT% per 90',
    'is_inverse': False},
    'Avg Shot Distance': {'normal_name': 'Standard - Dist',
    'per_90_name': 'Standard - Dist per 90',
    'is_inverse': False},
    'Non-Penalty Expected Goals per Shot': {'normal_name': 'Expected - npxG/Sh',
    'per_90_name': 'Expected - npxG/Sh per 90',
    'is_inverse': False}},
 'Passing': 
    {'Assists': {'normal_name': 'Ast',
    'per_90_name': 'Ast per 90',
    'is_inverse': False},
    'Total Passing Distance': {'normal_name': 'Total - TotDist',
    'per_90_name': 'Total - TotDist per 90',
    'is_inverse': False},
    'Progressive Passing Distance': {'normal_name': 'Total - PrgDist',
    'per_90_name': 'Total - PrgDist per 90',
    'is_inverse': False},
    'Passes Completed': {'normal_name': 'Total - Cmp',
    'per_90_name': 'Total - Cmp per 90',
    'is_inverse': False},
    'Pass Completion %': {'normal_name': 'Total - Cmp%',
    'per_90_name': 'Total - Cmp% per 90',
    'is_inverse': False},
    'Crosses': {'normal_name': 'Performance - Crs',
    'per_90_name': 'Performance - Crs per 90',
    'is_inverse': False},
    'Short Passes Completed': {'normal_name': 'Short - Cmp',
    'per_90_name': 'Short - Cmp per 90',
    'is_inverse': False},
    'Short Pass Completion %': {'normal_name': 'Short - Cmp%',
    'per_90_name': 'Short - Cmp% per 90',
    'is_inverse': False},
    'Medium Passes Completed': {'normal_name': 'Medium - Cmp',
    'per_90_name': 'Medium - Cmp per 90',
    'is_inverse': False},
    'Medium Pass Completion %': {'normal_name': 'Medium - Cmp%',
    'per_90_name': 'Medium - Cmp% per 90',
    'is_inverse': False},
    'Long Passes Completed': {'normal_name': 'Long - Cmp',
    'per_90_name': 'Long - Cmp per 90',
    'is_inverse': False},
    'Long Pass Completion %': {'normal_name': 'Long - Cmp%',
    'per_90_name': 'Long - Cmp% per 90',
    'is_inverse': False},
    'Expected Assists': {'normal_name': 'Expected - xA',
    'per_90_name': 'xA per 90',
    'is_inverse': False},
    'Assists - xA': {'normal_name': 'Expected - A-xAG',
    'per_90_name': 'A-xAG per 90',
    'is_inverse': False},
    'Key Passes': {'normal_name': 'KP',
    'per_90_name': 'KP per 90',
    'is_inverse': False},
    'Passes into Final 3rd': {'normal_name': '1/3',
    'per_90_name': '1/3 per 90',
    'is_inverse': False},
    'Passes into PA': {'normal_name': 'PPA',
    'per_90_name': 'PPA per 90',
    'is_inverse': False},
    'Crosses into PA': {'normal_name': 'CrsPA',
    'per_90_name': 'CrsPA per 90',
    'is_inverse': False},
    'Progressive Passes': {'normal_name': 'PrgP',
    'per_90_name': 'PrgP per 90',
    'is_inverse': False},
    'Through-Balls': {'normal_name': 'Pass Types - TB',
    'per_90_name': 'Pass Types - TB per 90',
    'is_inverse': False},
    'Switches': {'normal_name': 'Pass Types - Sw',
    'per_90_name': 'Pass Types - Sw per 90',
    'is_inverse': False}},
 'Creation': 
    {'Shot-Creating Actions': {'normal_name': 'SCA - SCA',
    'per_90_name': 'SCA - SCA per 90',
    'is_inverse': False},
    'Liveball Pass leading to Shot': {'normal_name': 'SCA Types - PassLive',
    'per_90_name': 'SCA Types - PassLive per 90',
    'is_inverse': False},
    'Deadball Pass leading to Shot': {'normal_name': 'SCA Types - PassDead',
    'per_90_name': 'SCA Types - PassDead per 90',
    'is_inverse': False},
    'Take-ons leading to Shot': {'normal_name': 'SCA Types - TO',
    'per_90_name': 'SCA Types - TO per 90',
    'is_inverse': False},
    'Shots leading to Shot': {'normal_name': 'SCA Types - Sh',
    'per_90_name': 'SCA Types - Sh per 90',
    'is_inverse': False},
    'Defensive Actions leading to Shot': {'normal_name': 'SCA Types - Def',
    'per_90_name': 'SCA Types - Def per 90',
    'is_inverse': False},
    'Liveball Pass leading to Goals': {'normal_name': 'GCA Types - PassLive',
    'per_90_name': 'GCA Types - PassLive per 90',
    'is_inverse': False},
    'Deadball Pass leading to Goals': {'normal_name': 'GCA Types - PassDead',
    'per_90_name': 'GCA Types - PassDead per 90',
    'is_inverse': False},
    'Take-ons leading to Goals': {'normal_name': 'GCA Types - TO',
    'per_90_name': 'GCA Types - TO per 90',
    'is_inverse': False},
    'Shots leading to Goals': {'normal_name': 'GCA Types - Sh',
    'per_90_name': 'GCA Types - Sh per 90',
    'is_inverse': False},
    'Defensive Actions leading to Goals': {'normal_name': 'GCA Types - Def',
    'per_90_name': 'GCA Types - Def per 90',
    'is_inverse': False}},
 'Skills': 
    {'Touches': {'normal_name': 'Touches - Touches',
    'per_90_name': 'Touches - Touches per 90',
    'is_inverse': False},
    'Touches - Def Pen': {'normal_name': 'Touches - Def Pen',
    'per_90_name': 'Touches - Def Pen per 90',
    'is_inverse': False},
    'Touches - Def 3rd': {'normal_name': 'Touches - Def 3rd',
    'per_90_name': 'Touches - Def 3rd per 90',
    'is_inverse': False},
    'Touches - Mid 3rd': {'normal_name': 'Touches - Mid 3rd',
    'per_90_name': 'Touches - Mid 3rd per 90',
    'is_inverse': False},
    'Touches - Att 3rd': {'normal_name': 'Touches - Att 3rd',
    'per_90_name': 'Touches - Att 3rd per 90',
    'is_inverse': False},
    'Touches - Att Pen': {'normal_name': 'Touches - Att Pen',
    'per_90_name': 'Touches - Att Pen per 90',
    'is_inverse': False},
    'Take-Ons - Att': {'normal_name': 'Take-Ons - Att',
    'per_90_name': 'Take-Ons - Att per 90',
    'is_inverse': False},
    'Successful Take-Ons': {'normal_name': 'Take-Ons - Succ',
    'per_90_name': 'Take-Ons - Succ per 90',
    'is_inverse': False},
    'Take-Ons - Succ%': {'normal_name': 'Take-Ons - Succ%',
    'per_90_name': 'Take-Ons - Succ% per 90',
    'is_inverse': False},
    'Take-Ons - Tackled': {'normal_name': 'Take-Ons - Tkld',
    'per_90_name': 'Take-Ons - Tkld per 90',
    'is_inverse': False},
    'Carries': {'normal_name': 'Carries - Carries',
    'per_90_name': 'Carries - Carries per 90',
    'is_inverse': False},
    'Carries - TotDist': {'normal_name': 'Carries - TotDist',
    'per_90_name': 'Carries - TotDist per 90',
    'is_inverse': False},
    'Carries - PrgDist': {'normal_name': 'Carries - PrgDist',
    'per_90_name': 'Carries - PrgDist per 90',
    'is_inverse': False},
    'Progressive Carries': {'normal_name': 'Carries - PrgC',
    'per_90_name': 'Carries - PrgC per 90',
    'is_inverse': False},
    'Carries into Final 3rd': {'normal_name': 'Carries - 1/3',
    'per_90_name': 'Carries - 1/3 per 90',
    'is_inverse': False},
    'Carries into PA': {'normal_name': 'Carries - CPA',
    'per_90_name': 'Carries - CPA per 90',
    'is_inverse': False},
    'Miscontrols': {'normal_name': 'Carries - Mis',
    'per_90_name': 'Carries - Mis per 90',
    'is_inverse': True},
    'Dispossessed': {'normal_name': 'Carries - Dis',
    'per_90_name': 'Carries - Dis per 90',
    'is_inverse': True},
    'Progressive Passes Received': {'normal_name': 'Receiving - PrgR',
    'per_90_name': 'Receiving - PrgR per 90',
    'is_inverse': False},
    'PKs won': {'normal_name': 'Performance - PKwon',
    'per_90_name': 'Performance - PKwon per 90',
    'is_inverse': False}},
 'Defense': 
    {'Tackles Attempted': {'normal_name': 'Tackles - Tkl',
    'per_90_name': 'Tackles - Tkl per 90',
    'is_inverse': False},
    'Tackles Won': {'normal_name': 'Tackles - TklW',
    'per_90_name': 'Tackles - TklW per 90',
    'is_inverse': False},
    'Tackles - Def 3rd': {'normal_name': 'Tackles - Def 3rd',
    'per_90_name': 'Tackles - Def 3rd per 90',
    'is_inverse': False},
    'Tackles - Mid 3rd': {'normal_name': 'Tackles - Mid 3rd',
    'per_90_name': 'Tackles - Mid 3rd per 90',
    'is_inverse': False},
    'Tackles - Att 3rd': {'normal_name': 'Tackles - Att 3rd',
    'per_90_name': 'Tackles - Att 3rd per 90',
    'is_inverse': False},
    'Dribblers Tackled': {'normal_name': 'Challenges - Tkl',
    'per_90_name': 'Challenges - Tkl per 90',
    'is_inverse': False},
    'Dribbles Challenged': {'normal_name': 'Challenges - Att',
    'per_90_name': 'Challenges - Att per 90',
    'is_inverse': False},
    'Challenges Lost': {'normal_name': 'Challenges - Lost',
    'per_90_name': 'Challenges - Lost per 90',
    'is_inverse': True},
    '% of Dribblers Tackled': {'normal_name': 'Challenges - Tkl%',
    'per_90_name': 'Challenges - Tkl% per 90',
    'is_inverse': False},
    'Interceptions': {'normal_name': 'Int',
    'per_90_name': 'Int per 90',
    'is_inverse': False},
    'Tackles + Interceptions': {'normal_name': 'Tkl+Int',
    'per_90_name': 'Tkl+Int per 90',
    'is_inverse': False},
    'Blocks': {'normal_name': 'Blocks - Blocks',
    'per_90_name': 'Blocks - Blocks per 90',
    'is_inverse': False},
    'Shots Blocked': {'normal_name': 'Blocks - Sh',
    'per_90_name': 'Blocks - Sh per 90',
    'is_inverse': False},
    'Passes Blocked': {'normal_name': 'Blocks - Pass',
    'per_90_name': 'Blocks - Pass per 90',
    'is_inverse': False},
    'PKs conceded': {'normal_name': 'Performance - PKcon',
    'per_90_name': 'Performance - PKcon per 90',
    'is_inverse': True},
    'Own Goals': {'normal_name': 'Performance - OG',
    'per_90_name': 'Performance - OG per 90',
    'is_inverse': True},
    'Clearances': {'normal_name': 'Clr',
    'per_90_name': 'Clr per 90',
    'is_inverse': False},
    'Errors': {'normal_name': 'Err',
    'per_90_name': 'Err per 90',
    'is_inverse': True},
    'Aerial Duels - Won': {'normal_name': 'Aerial Duels - Won',
    'per_90_name': 'Aerial Duels - Won per 90',
    'is_inverse': False},
    'Aerial Duels - Lost': {'normal_name': 'Aerial Duels - Lost',
    'per_90_name': 'Aerial Duels - Lost per 90',
    'is_inverse': False},
    '% Aerial Duels Won': {'normal_name': 'Aerial Duels - Won%',
    'per_90_name': 'Aerial Duels - Won% per 90',
    'is_inverse': False}},
 'Playing Time': 
    {'Starts': {'normal_name': 'Starts - Starts',
    'per_90_name': 'Starts - Starts per 90',
    'is_inverse': False},
    'Minutes Played': {'normal_name': 'Playing Time - Min',
    'per_90_name': 'Playing Time - Min per 90',
    'is_inverse': False},
    'Minutes per Start': {'normal_name': 'Starts - Mn/Start',
    'per_90_name': 'Starts - Mn/Start per 90',
    'is_inverse': False},
    'Substitute Appearances': {'normal_name': 'Subs - Subs',
    'per_90_name': 'Subs - Subs per 90',
    'is_inverse': False},
    'Minutes per Sub': {'normal_name': 'Subs - Mn/Sub',
    'per_90_name': 'Subs - Mn/Sub per 90',
    'is_inverse': False},
    'Team Points per Appearance': {'normal_name': 'Team Success - PPM',
    'per_90_name': 'Team Success - PPM per 90',
    'is_inverse': False},
    'Team Goals while on Pitch': {'normal_name': 'Team Success - onG',
    'per_90_name': 'Team Success - onG per 90',
    'is_inverse': False},
    'Team GA while on Pitch': {'normal_name': 'Team Success - onGA',
    'per_90_name': 'Team Success - onGA per 90',
    'is_inverse': False},
    'Plus/Minus Goals while on Pitch': {'normal_name': 'Team Success - +/-',
    'per_90_name': 'Team Success - +/- per 90',
    'is_inverse': False},
    'Team xG while on Pitch': {'normal_name': 'Team Success (xG) - onxG',
    'per_90_name': 'Team Success (xG) - onxG per 90',
    'is_inverse': False}},
 'Misc': {'Yellow Cards': {'normal_name': 'Performance - CrdY',
   'per_90_name': 'Performance - CrdY per 90',
   'is_inverse': False},
  'Second Yellows': {'normal_name': 'Performance - 2CrdY',
   'per_90_name': 'Performance - 2CrdY per 90',
   'is_inverse': False},
  'Red Cards': {'normal_name': 'Performance - CrdR',
   'per_90_name': 'Performance - CrdR per 90',
   'is_inverse': False},
  'Fouls': {'normal_name': 'Performance - Fls',
   'per_90_name': 'Performance - Fls per 90',
   'is_inverse': False},
  'Foul Drawn': {'normal_name': 'Performance - Fld',
   'per_90_name': 'Performance - Fld per 90',
   'is_inverse': False}}}

with open('data/seasons_played.json', 'r') as j:
      seasons_played_per_player = json.loads(j.read())
      all_players = list(set(list(seasons_played_per_player.keys())))

with open('data/squads_per_season.json', 'r') as j:
      squads_per_season = json.loads(j.read())
      all_clubs = list(set(list(squads_per_season.keys())))


with open('data/player_per_season_info.json', 'r') as j:
      player_per_season_info = json.loads(j.read())

