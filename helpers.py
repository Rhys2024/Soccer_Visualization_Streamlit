from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

import streamlit as st

import references as refr

### all compares ###
def normalize(temp_df, leave_outs=None):
    """
    Normalize the numerical columns of the data
    to get player percentiles for the given stats!
    """
    
    mm = MinMaxScaler()
    
    temp_df = temp_df.dropna(axis = 1, how = 'all')
    
    if not leave_outs:
        
        return pd.DataFrame(mm.fit_transform(temp_df), 
                                         index = temp_df.index,
                                         columns = temp_df.columns)
    
    leave_outs = leave_outs + [col for col in temp_df.columns if 'Unnamed' in col]

    keeps = [col for col in temp_df.columns if col not in leave_outs]

    chunk_for_normalization = temp_df[keeps]

    norm_df = pd.concat([temp_df[leave_outs], 
                            pd.DataFrame(mm.fit_transform(chunk_for_normalization), 
                                         index = chunk_for_normalization.index,
                                         columns = chunk_for_normalization.columns)], 
                        axis = 1).round(2)

    return norm_df



def invert(row, type_of_stat):
    
    stat_names = refr.new_grouped_stats_player_comparison[type_of_stat]
    if row[refr.theta_column_name] in stat_names:
        if stat_names[row[refr.theta_column_name]]['is_inverse']:
            return 1 - row[refr.radii_column_name]
        return row[refr.radii_column_name]
    print("\n\nSOMETHIN AINT RIGHT!!\n\n")
    

def check_mins_played(player, season, minimum_mins_played):
    
    desired_chunk = refr.data_players.groupby(['Player', 'Season']).get_group((player, season))
    
    passes_req = desired_chunk[refr.min_played_col].values[0] > minimum_mins_played
    
    if not passes_req:
        st.warning(f'{player} has less than the Minimum Minutes Played in {season}')
        st.stop()


def partition_df(df, name, season, seasons_selected, scalings, is_squad = False):
    
    normalize_to, normalize_against, specs = scalings.values()
    
    if normalize_to == refr.scale_to_options[0]:
        df_for_normalization = df.groupby('Season').get_group(season)
    elif normalize_to == refr.scale_to_options[1]:
        df_for_normalization = df[df.Season.isin(seasons_selected)]
    elif normalize_to == refr.scale_to_options[2]:
        df_for_normalization = df
    
    if is_squad:
        return df_for_normalization
    
    player_info_for_season = refr.player_per_season_info[name][season]
    
    if normalize_against == 'All Players':
        return df_for_normalization
    if normalize_against == 'League':
        df_for_normalization = df_for_normalization[df_for_normalization.Comp == player_info_for_season['Comp']]
    elif normalize_against == 'Position':
        df_for_normalization = df_for_normalization[df_for_normalization.Pos == player_info_for_season['Pos']]
    elif normalize_against == 'Age Group':
        df_for_normalization = df_for_normalization[df_for_normalization.Age.between(player_info_for_season['Age'] - specs,
                                                                                     player_info_for_season['Age'] + specs)]
    
    return df_for_normalization
    

### player_performance ###
def player_performance(player_name, season, seasons_selected,
                       temp_df, scalings, minimum_mins_played):
    
    #leave_out = ['Player', 'Squad', 
                 #'Season', 'Comp',
                 #'Nation', 'Pos', 'position']
    
    leave_out = [col for n, col in enumerate(temp_df.columns) if temp_df.dtypes.iloc[n] == 'O']
    
    check_mins_played(player_name, season, minimum_mins_played)
    
    temp_df = temp_df[temp_df[refr.min_played_col] > minimum_mins_played]
    
    df_for_normalization = partition_df(temp_df, player_name, season, seasons_selected, scalings)
    
    if player_name not in df_for_normalization.Player.unique():
        print(f'\n\nPLAYER {player_name} NOT IN SEASON INDEX !!!\n\n')
        st.warning('There has been an unknown issue!')
        st.stop()
        return 'None'

    normalized_df = normalize(df_for_normalization.fillna(0.0), leave_out)
    
    normalized_df = normalized_df.groupby('Season').get_group(season)

    chunk = normalized_df.groupby('Player').get_group(player_name).T
    
    temp_player_df = pd.DataFrame(chunk).round(2).sum(axis = 1)
    
    temp_player_df = temp_player_df.reset_index() 
    
    temp_player_df.columns = [refr.theta_column_name, refr.radii_column_name]
    
    
    return temp_player_df



### team_performance ###
def team_performance(squad_name, season, seasons_selected,
                       temp_team_df, scalings):
    
    leave_out = [col for n, col in enumerate(temp_team_df.columns) if temp_team_df.dtypes.iloc[n] == 'O']
    
    
    df_for_normalization = partition_df(temp_team_df, squad_name, 
                                        season, seasons_selected, scalings, is_squad = True)
    
    normalized_df = normalize(df_for_normalization, leave_out)
    
    normalized_df = normalized_df.groupby('Season').get_group(season)
    
    chunk = normalized_df.groupby(['Squad']).get_group(squad_name).T
    
    temp_team_df = pd.DataFrame(chunk).round(2).sum(axis = 1)
    temp_team_df = temp_team_df.reset_index() 
    
    temp_team_df.columns = [refr.theta_column_name, refr.radii_column_name]
    
    return temp_team_df


def played_in_these_comps(df, comp1, comp2, seasons=[]):
    """Returns DataFrame of Players who played in both 'comp1' and 'comp2'

    Args:
        df (pandas.DataFrame): dataframe of players (probably all players data)
        comp1 (str): String of League Name
        comp2 (str): String of League Name
        seasons (list, optional): Seasons to restrict to. Defaults to [].

    Returns:
        pandas.DataFrame: dataframe of players who have played in both 'comp1' and 'comp2'
    """

    relevant_names = df.groupby('Player').apply(lambda player: comp1 in player.Comp.unique() and 
                                                         comp2 in player.Comp.unique()
                                                      )
    relevant_names = list(relevant_names[relevant_names == True].index)

    if seasons != []:
        players_who_played_in_comp1_and_comp2 = df[(df.Player.isin(relevant_names)) &
                                                    (df.Season.isin(seasons))
                                                    & (df.Comp.isin([comp1, comp2]))
        ]
    else:
        players_who_played_in_comp1_and_comp2 = df[(df.Player.isin(relevant_names)) 
                                                   & (df.Comp.isin([comp1, comp2]))
                                                   ]

    return players_who_played_in_comp1_and_comp2


def get_lims(data, col):
    
    max_val = data[col].max() + (data[col].max() * .15)
    min_val = data[col].min() + (data[col].min() * .15)

    if abs(min_val) > abs(max_val):
        return abs(min_val)
    return abs(max_val)