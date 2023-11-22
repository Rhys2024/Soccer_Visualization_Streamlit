import sys

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

def validate_frame(frame, f_name):
    
    # .drop(columns = ['Player'])
    try:
        old_frame = pd.read_csv(f_name, index_col='Unnamed: 0')
    except:
        return True
    
    different_cols = set(frame.columns).difference(set(old_frame.columns))
    print(different_cols)
    return len(different_cols) == 0

def remove_unnamed_cols(df):
    return df.drop(columns = [col for col in df.columns if 'Unnamed' in col])

def sort_frame_levels(df):
    
    new_cols = {}
        
    for col in df.columns:
        if 'Unnamed' in col[0]:
            new_cols.append(col[1])
        else:
            new_cols.append(f"{col[0]} - {col[1]}")
    
    df.columns = new_cols
    
    return df

###### Helper Functions ######



def fetch_and_store_data(year):

    for stat in tables:
        
        print(f"{year}-{year+1}, {stat_type_names[stat]}")
        
        url = f"https://fbref.com/en/comps/Big5/{year}-{year+1}/{stat}/players/{year}-{year+1}-Big-5-European-Leagues-Stats"
        
        temp_first = pd.read_html(url)[0]
        
        temp = sort_frame_levels(temp_first)
        
        temp = temp.drop(columns = deletes)
        temp = temp.loc[temp.Player != "Player"].dropna()
        
        temp['Player'] = temp['Player'].apply(handle_name)
        
        if stat != 'stats':
            
            temp = temp.drop(columns=[col for col in temp.columns if col in summary_cols])
        
        else:
            
            temp['Comp'] = temp['Comp'].apply(handle_league)
            temp['Nation'] = temp['Nation'].apply(handle_league)
            temp['Age'] = temp['Age'].apply(handle_age)
            
            temp = temp[ (temp['Age'] != 'NULL') | (temp['Comp'] != 'NULL') | (temp['Nation'] != 'NULL') ]
        
        file_name = f'data/{year}_{year+1}_{stat_type_names[stat]}.csv'
        
        if validate_frame(temp, file_name):
            temp.to_csv(file_name)


def concantenate_subframes(year):
    
    season = f"{year}_{year+1}"
    
    df = pd.DataFrame()
    
    for n, stat in enumerate(references.important_stats_player):
        
        temp = pd.read_csv(f"data/{season}_{stat}.csv")
        temp = temp.drop_duplicates('Player', keep='first')
        
        if n == 0:
            yuh = list(temp.Player.values)
            print(len(yuh))
            
        temp.set_index('Player', inplace = True)
        
        if n != 0:
            try:
                temp = temp.loc[yuh]
            except:
                print(stat)
        
        df = pd.concat([df, temp], axis = 1)
        df = df.loc[:,~df.columns.duplicated()]   
    
    
    #df = df.reset_index()
    #df['Player'] = df['Player'].apply(handle_name)
    #df = df.set_index('Player')
    df = remove_unnamed_cols(df)
    df.index = [handle_name(player) for player in df.index]
    df.index.name = 'Player'
    
    df.to_csv(f"data/{season.replace('-', '_')}_all_outfield_players.csv")
    print(df)
    print("Data Sucessfully Updated")


def data_update(year):
    fetch_and_store_data(year)
    concantenate_subframes(year)


def update_seasons_played(year, is_test):
    
    beginning_year = 2017
    
    years = [year for year in range(beginning_year,year+1)]
    seasons_played_per_player = {}

    for year in years:
        
        stat = 'Standard Stats'
        
        season = f"{year}_{year+1}"
        temp = pd.read_csv(f"data/{season}_{stat}.csv")

        for p in temp['Player']:
            
            if p in seasons_played_per_player:
                seasons_played_per_player[p].append(season.replace('_', '-'))
            else:
                seasons_played_per_player[p] = [season.replace('_', '-')]

    for p in seasons_played_per_player:
        
        seasons_played_per_player[p] = list(set(seasons_played_per_player[p]))

        seasons_played_per_player[p].sort()
    
    if not is_test:
        try:
            with open("data/seasons_played.json", "w") as outfile:
                json.dump(seasons_played_per_player, outfile, indent = 4)
            print("SEASONS PLAYED SUCCESSFULLY UPDATED")
        except:
            return seasons_played_per_player
            #print("SEASONS PLAYED SUCCESSFULLY UPDATED")


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
    year = int(input('Enter the year:\t'))
    
    if not isinstance(year, int):
        print('Year must be a number!!')
        year = int(input('Enter the year:\t'))
    
    assert isinstance(year, int), 'try again...'
    assert year in [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    
    #print('EXIT')
    #year = set_year(override_year=2022)
    #for yr in [2017, 2018, 2019, 2020, 2021, 2022, 2023]:
        #data_update(year=yr)
    #update_seasons_played(2023)
    #CLUB_update_seasons_played(2023)