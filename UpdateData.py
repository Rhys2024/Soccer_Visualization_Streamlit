import datetime as dt

from unidecode import unidecode
import pandas as pd
import numpy as np
import json

import references
    
def set_year(override_year = None):
    
    if override_year:
        return override_year
    
    month = dt.datetime.now().month
    year = dt.datetime.now().year

    if month <= 6:
        year = year - 1
    
    return year


stats_available = ['stats', 'shooting', 'passing', 'passing_types', 'gca', 
          'defense', 'possession', 'playingtime', 'misc', 'keepers']
stat_type_names = {"stats" : "Standard Stats", 'shooting' : "Shooting Stats",
                   'passing' : "Passing Stats", 'passing_types' : "Pass Type Stats",
                   'gca' : "Shot and Goal Creation Stats", 'defense' : "Defensive Stats",
                   'possession' : "Possession Stats", 'playingtime' : "Playing Time Stats",
                   'misc' : "Misc Stats", 'keepers' : "Goalkeeping Stats"}

tables = ['stats', 'shooting', 'passing', 'passing_types', 'gca', 'defense', 'possession', 
                  'playingtime', 'misc', 'keepers']
deletes = ['Matches', 'Rk']
summary_cols = ['Squad', 'Nation', 'Comp', 'Pos', 'Age', 'Born']

remove_cols = [ 'Nation', 'Comp', 'Pos', 'Age', 'Born']

###### Helper Functions ######
def handle_league(league):
    
    if pd.isna(league):
        return 'NULL'
    
    try:
        real_name = league[league.index(' ') + 1 : ]
    except:
        print(league)
    
    return real_name



def handle_age(age):
    
    if pd.isna(age):
        return 'NULL'
    
    try:
        int(age)
        return age
    except:
        return age[:age.index('-')]


def handle_nation(name):
    if not pd.isna(name):
        return name[:2].upper()
    return 'NULL'


def handle_name(name):
    if not pd.isna(name):
        return unidecode(name)
    return None


def handle_pos(fbref_pos):
    """
    
    Given an FBRef position, return more intuitive position label
    
    """
    
    if 'MF' in fbref_pos and 'FW' in fbref_pos:
        return 'AM'
    if 'MF' in fbref_pos and 'DF' in fbref_pos:
        return 'FB'
    if 'DF' in fbref_pos and 'FW' in fbref_pos:
        return 'WB'
    if 'FW' in fbref_pos:
        return 'FW'
    if 'DF' in fbref_pos:
        return 'DF'
    if 'MF' in fbref_pos:
        return 'MF'
    if 'GK' in fbref_pos:
        return 'GK'

def validate_frame(frame, f_name):
    
    # .drop(columns = ['Player'])
    try:
        old_frame = pd.read_csv(f_name, index_col='Unnamed: 0')
    except:
        return True
    
    different_cols = set(frame.columns).difference(set(old_frame.columns))
    print(f'Different Columns: {list(different_cols)}')
    print(f'Column Lengths: \n\tOld: {len(old_frame.columns)}\nNew: {len(frame.columns)}')
    return len(different_cols) == 0

def remove_unnamed_cols(df):
    return df.drop(columns = [col for col in df.columns 
                              if 'Unnamed' in col]
                   )

def sort_frame_levels(df):
    
    new_cols = []
        
    for col in df.columns:
        if 'Unnamed' in col[0]:
            new_cols.append(col[1])
        else:
            new_cols.append(f"{col[0]} - {col[1]}")
    
    df.columns = new_cols
    
    return df

def handle_index_duplicates(data, duplicate_index):
    
    #playing_time_df.loc[('Alberto Lopez', 'Sevilla')].drop(columns = ['Unnamed: 0']).T
    
    pass


###### Helper Functions ######



def fetch_and_store_data(year, test=False):
    
    test_frames = {}

    for stat in tables:
        
        print(year)
        print(type(year))
        # {year}-{year+1}
        print(f"{year}, {stat_type_names[stat]}")
        
        # {year}-{year+1}
        url = f"https://fbref.com/en/comps/Big5/{year}/{stat}/players/{year}-Big-5-European-Leagues-Stats"
        
        temp_first = pd.read_html(url)[0]
        
        temp = sort_frame_levels(temp_first)
        
        temp = temp.drop(columns = references.deletes).drop_duplicates()
        
        # .dropna()
        temp = temp.loc[temp.Player != "Player"]
        
        temp['Player'] = temp['Player'].apply(handle_name) 
        
        if stat != 'stats':
            
            temp = temp.drop(columns=[col for col in temp.columns if col in remove_cols])
        
        else:
            
            temp['Comp'] = temp['Comp'].apply(handle_league)
            temp['Nation'] = temp['Nation'].apply(handle_nation)
            temp['Age'] = temp['Age'].apply(handle_age)
            
            temp = temp[ (temp['Age'] != 'NULL') | (temp['Comp'] != 'NULL') | (temp['Nation'] != 'NULL') ]
        
        temp = temp.fillna(0.0)
        
        file_name = f'data/{year}_{stat_type_names[stat]}.csv'
        
        #if validate_frame(temp, file_name):
        
        if test:
            test_frames[stat_type_names[stat]] = temp
        else:
            temp.to_csv(file_name)

    if test:
        return test_frames

def concantenate_subframes(year, test=False):
    
    #season = f"{year}_{year+1}"
    #season = year.replace('-', '_')
    
    if year != '2023-2024' and year != '2024-2025':
        season = year.replace('-', '_')
    else:
        season = year
    
    df = pd.DataFrame()
    
    for stat in references.important_stats_player:
        
        temp = pd.read_csv(f"data/{season}_{stat}.csv")
        
        temp['Player'] = temp['Player'].apply(handle_name)
        
        temp.set_index(['Player', 'Squad'], inplace = True)
        
        if len(temp.index[temp.index.duplicated()]) > 0:
            print(f"NUMBER OF DUPLICATED INDEXES = {len(temp.index[temp.index.duplicated()])}")
            temp = temp.loc[~temp.index.duplicated(keep='first')]
        
        #try:
        df = pd.concat([df, temp], axis = 1)
        #except:
           # if len(temp.index[temp.index.duplicated()]) > 0:
             #   print("ERROR will be throw because there is ")
            #else:
               # break
            
        df = df.loc[:,~df.columns.duplicated()]
    
    df = remove_unnamed_cols(df)
    df['Season'] = year.replace('_', '-')

    if test:
        return df
    
    df.to_csv(f"data/{season}_all_outfield_players.csv")
    print(df)
    print("Data Sucessfully Updated")


def concantenate_season_frames():
    
    # concantenate_subframes(year).reset_index()
    # pd.read_csv(f"data/{season.replace('-', '_')}_all_outfield_players.csv")
    data_players = pd.concat([concantenate_subframes(season, test=True).reset_index() for season in references.years], 
                             axis = 0).dropna(subset = ['Player', 
                                                        'Squad', 'Pos', 
                                                        'Comp'])
    
    for stat_type in references.new_grouped_stats_player_comparison:

        for name, col_name in references.new_grouped_stats_player_comparison[stat_type].items():

            normal_name = col_name['normal_name']
            per_90_name = col_name['per_90_name']
            
            data_players[per_90_name] = (data_players[normal_name].copy() / 90).round(3)
    
    data_players['position'] = data_players['Pos'].copy().apply(handle_pos)
    # 24_25_all_outfield_player_data
    data_players.to_csv('data/24_25_all_outfield_player_data.csv')


def update_player_info():
    
    data_groups = pd.read_csv('data/24_25_all_outfield_player_data.csv', index_col=0).groupby(['Player'])
    
    keys = data_groups.groups

    summary_cols = ['Player', 'Squad', 
                    'Season', 'Comp',
                    'Age', 'Pos',
                    'Nation']

    player_per_season_info = {}

    for key in keys:

        temp_data = data_groups.get_group(key)[summary_cols + [references.min_played_col]
                                               ].sort_values(by = 'Season'
                                                             ).set_index('Player')
        
        player_per_season_info[key] = {}
        
        for season in temp_data.Season.unique():
            
            season_temp = temp_data[temp_data.Season == season].sort_values(by=references.min_played_col, 
                                                                            ascending = False
                                                                        ).drop_duplicates(subset = ['Season'], 
                                                                                            keep = 'first'
                                                                                            ).set_index('Season')
            temp_info = season_temp.T.to_dict()[season]
            player_per_season_info[key][season] = temp_info
    
    with open("data/player_per_season_info.json", "w") as outfile:
        json.dump(player_per_season_info, outfile, indent = 4)
    print("PLAYER INFO SUCCESSFULLY SAVED!!!")


def data_update(weight='light'):
    #fetch_and_store_data(references.curr_season)
    #concantenate_subframes(references.curr_season)
    
    #update_player_info()
    
    if weight == 'light':
        fetch_and_store_data(references.curr_season)
        concantenate_subframes(references.curr_season)
        concantenate_season_frames()
        #update_seasons_played(2024)
        #update_player_per_season_info()
    
    



def update_seasons_played(year):
    
    beginning_year = 2017
    
    years = [year for year in range(beginning_year,year+1)]
    seasons_played_per_player = {}

    for year in years:
        
        stat = 'Standard Stats'
        
        season = f"{year}_{year+1}"
        try:
            temp = pd.read_csv(f"data/{season}_{stat}.csv")
        except:
            temp = pd.read_csv(f"data/{season.replace('_', '-')}_{stat}.csv")

        for p in temp['Player']:
            
            if p in seasons_played_per_player:
                seasons_played_per_player[p].append(season.replace('_', '-'))
            else:
                seasons_played_per_player[p] = [season.replace('_', '-')]

    for p in seasons_played_per_player:
        
        seasons_played_per_player[p] = list(set(seasons_played_per_player[p]))

        seasons_played_per_player[p].sort()
    
    with open("data/seasons_played.json", "w") as outfile:
        json.dump(seasons_played_per_player, outfile, indent = 4)
    print("SEASONS PLAYED SUCCESSFULLY UPDATED")


def update_player_per_season_info():
    
    data_groups = references.data_players.groupby(['Player'])
    keys = data_groups.groups

    player_per_season_info = {}

    for key in keys:

        temp_data = data_groups.get_group(key)[references.summary_cols].sort_values(by = 'Season').set_index('Player')
        
        player_per_season_info[key] = {}
        
        for season in temp_data.Season.unique():
        
            season_temp = temp_data[temp_data.Season == season].set_index('Season')

            temp_info = season_temp.T.to_dict()[season]
            
            player_per_season_info[key][season] = temp_info
    
    with open("data/player_per_season_info.json", "w") as outfile:
        json.dump(player_per_season_info, outfile, indent = 4)
    print("PLAY INFO PER SEASON SUCCESSFULLY UPDATED")


def CLUB_update_seasons_played(year):
    
    beginning_year = 2017
    
    years = [year for year in range(beginning_year,year+1)]
    squads_per_season = {}

    for year in years:
        
        stat = 'Standard Stats'
        
        season = f"{year}_{year+1}"
        temp = pd.read_csv(f"data/Squads_{season}_{stat}.csv")

        for club in temp['Squad']:
            
            if club in squads_per_season:
                squads_per_season[club].append(season.replace('_', '-'))
            else:
                squads_per_season[club] = [season.replace('_', '-')]

    for club in squads_per_season:
        
        squads_per_season[club] = list(set(squads_per_season[club]))
        squads_per_season[club].sort()
    
    with open("data/squads_per_season.json", "w") as outfile:
        json.dump(squads_per_season, outfile, indent = 4)
    
    print("SEASONS PLAYED SUCCESSFULLY UPDATED")


if __name__ == '__main__':
    
    #print(str(sys.stdin))
    #year = int(input('Enter the year:\t'))
    data_update(weight='light')
    #print(references.curr_season)
    #if not isinstance(year, int):
        #print('Year must be a number!!')
        #year = int(input('Enter the year:\t'))
    
    #assert isinstance(year, int), 'try again...'
    #assert year in [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    
    #print('EXIT')
    #year = set_year(override_year=2022)
    #for yr in [2017, 2018, 2019, 2020, 2021, 2022, 2023]:
        #data_update(year=yr)
    #update_seasons_played(2023)
    #CLUB_update_seasons_played(2023)