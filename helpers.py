from sklearn.preprocessing import StandardScaler, MinMaxScaler
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import references as refr



### maps.py ###
def get_CountryData(df, stat, mean_or_sum):
    
    sc = StandardScaler()
    mm = MinMaxScaler()
    
    if mean_or_sum == 'Mean':
        temp_df = df.groupby('Nation').mean()[stat]
    elif mean_or_sum == 'Sum':
        temp_df = df.groupby('Nation').sum()[stat]
    else:
        temp_mean = df.groupby('Nation').mean()[stat]
        temp_sum = df.groupby('Nation').sum()[stat]
        scaled_mean = pd.Series(sc.fit_transform(np.array(temp_mean).reshape(-1,1)).ravel(), index = temp_mean.index)
        scaled_sum = pd.Series(sc.fit_transform(np.array(temp_sum).reshape(-1,1)).ravel(), index = temp_sum.index)
        
        temp_df = pd.concat([scaled_mean, scaled_sum], axis = 1)
        temp_df.columns = ['mean', 'sum']
        temp_df[stat] = temp_df.sum(axis=1)
    
    temp_df = pd.DataFrame(temp_df).reset_index()
    
    if mean_or_sum != 'Standardized Mean-Sum Optimization':
        temp_df = temp_df.loc[ temp_df[stat] > 0]
    
    temp_df.index = temp_df['Nation']
    
    temp_df['Number of Players'] = df['Nation'].value_counts()
    temp_df = temp_df.loc[temp_df['Number of Players'] > 3]
    temp_df = temp_df.reset_index(drop=True)
    temp_df['Country Name'] = temp_df.Nation.map(refr.iso_codes)
    temp_df['Country Name'] = temp_df['Country Name'].map(refr.country_names)
    
    return temp_df


### performance.py, player_comparison.py ###
def get_player_pos(player_name, frame):
    
    if ('FW' in frame.loc[frame.Player == player_name]['Pos'].values[0] or 
        ('MF' in frame.loc[frame.Player == player_name]['Pos'].values[0] and 
         'FW' in frame.loc[frame.Player == player_name]['Pos'].values[0])): 

        return "Attacking"
    
    if 'MW' == frame.loc[frame.Player == player_name]['Pos'].values[0]:
        
        return "Pure Midfield"
    
    if 'DF' == frame.loc[frame.Player == player_name]['Pos'].values[0]:
        
        return "Defensive"
    
    if 'GK' in frame.loc[frame.Player == player_name]['Pos'].values[0]:
        return 'Goalkeeper'
    
    
### Possible Update for the above function - get_player_pos() ###
def UPDATE_get_player_pos(player_name, frame):
    
    if 'FW' == frame.loc[frame.Player == player_name]['Pos'].values[0]: 

        return "Pure Attacker"
    
    if ('MF' in frame.loc[frame.Player == player_name]['Pos'].values[0] and 
         'FW' in frame.loc[frame.Player == player_name]['Pos'].values[0]):
    
        return "Attacking Midfield"
    
    if ('DF' in frame.loc[frame.Player == player_name]['Pos'].values[0] and 
        'MF' in frame.loc[frame.Player == player_name]['Pos'].values[0]):
        
        return "Defensive Midfield"
    
    if 'MF' == frame.loc[frame.Player == player_name]['Pos'].values[0]:
        
        return "Pure Midfield"
    
    if 'DF' == frame.loc[frame.Player == player_name]['Pos'].values[0]:
        
        return "Defensive"
    
    if 'GK' in frame.loc[frame.Player == player_name]['Pos'].values[0]:
        return 'Goalkeeper'    


### Possible Update for the above functions - get_player_pos() and UPDATE_get_player_pos() ###
### No Frame Required -- could be used to initial bucket position types ###
def INITAL_get_player_pos(player_pos):
    
    if isinstance(player_pos, type(None)):
        return np.nan
        
    if 'FW' == player_pos: 
        return "Pure Attacker"
    
    if 'MF' in player_pos and 'FW' in player_pos:
        return "Attacking Midfield"
    
    if 'DF' in player_pos and 'MF' in player_pos:
        return "Defensive Midfield"
    
    if 'DF' in player_pos and 'FW' in player_pos:
        return "Attacking Defender"
    
    if 'MF' == player_pos:
        return "Pure Midfield"
    
    if 'DF' == player_pos:
        return "Pure Defender"
    
    if 'GK' == player_pos:
        return 'Goalkeeper'   
    
    return ''


### all compares ###
def normalize(temp_df, leave_outs=None):
    """
    Normalize the numerical columns of the data
    to get player percentiles for the given stats!
    """
    
    mm = MinMaxScaler()
    
    temp_df = temp_df.dropna(axis = 1, how = 'all')
    
    #print(temp_df)
    
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

    # invert
    return norm_df

def scale(temp_df, dex):
    
    sc = StandardScaler()
    
    scaled_df = pd.concat([temp_df.iloc[:,:dex], 
                            pd.DataFrame(sc.fit_transform(temp_df.iloc[:,dex:]), index = temp_df.index, 
                                         columns = temp_df.columns[dex:])], axis = 1)

    scaled_df = scaled_df.round(2)

    return scaled_df

def rank(df, cols):

    temp_df = df.copy()

    temp_df[cols] = (temp_df[cols].rank(ascending = False) / len(temp_df)).round(2)

    return temp_df

def invert(row):
    
    
    if row['stats'] in refr.inverse_cols:
        return 1 - row['Percentile']
    return row['Percentile']

#def invert(df, type_of_stat):
    
    #for col in df.columns:
        #if refr.new_grouped_stats_player_comparison[type_of_stat]
    

### performance.py, player_comparison.py ###
def player_performance(player_name, season,
                       temp_df, type_of_stat, per_90):
    
    #if not per_90:
        #stat_cols = list(i['normal_name'] for i in references.new_grouped_stats_player_comparison[type_of_stat].values())
    #else:
        #stat_cols = list(i['per_90_name'] for i in references.new_grouped_stats_player_comparison[type_of_stat].values())
    
    #stat_names = list(references.new_grouped_stats_player_comparison[type_of_stat].keys())
    
    leave_out = ['Player', 'Squad', 
                 'Season', 'Comp',
                 'Nation', 'Pos']
    
    season_df = temp_df.groupby('Season').get_group(season).copy()
    
    #print(season_df)
    
    if player_name not in season_df.Player.unique():
        print(f'\n\nPLAYER {player_name} NOT IN SEASON INDEX !!!\n\n')
        return 'None'
    
    normalized_df = normalize(season_df, leave_out)
    
    #normalized_df = normalized_df.apply(invert, axis = 1)
    
    #print(normalized_df)
    
    chunk = normalized_df.groupby(['Player']).get_group(player_name).T
    
    temp_player_df = pd.DataFrame(chunk).round(2).sum(axis = 1)
    
    #temp_player_df = temp_player_df.loc[stat_cols]
    #temp_player_df.index = stat_names
    temp_player_df = temp_player_df.reset_index() 
    
    temp_player_df.columns = [refr.theta_column_name, refr.radii_column_name]
    
    #print(temp_player_df)
    #print('\n\nPOOP\n\n')
    #first_stat_percentile = temp_player_df['Percentile'].iloc[0]
    
    #temp_player_df.loc[-1] = [stat_names[0], first_stat_percentile]
    
    #print(temp_player_df)
    
    return temp_player_df



### team_performance.py ###
def team_performance(squad_name, season,
                       temp_team_df, type_of_stat):
    
    leave_out = [col for n, col in enumerate(temp_team_df.columns) if temp_team_df.dtypes.iloc[n] == 'O']
    
    #stat_cols = list(refr.grouped_stats_player_comparison[type_of_stat].values())
    #stat_names = list(refr.grouped_stats_player_comparison[type_of_stat].keys())
    
    #temp_team_df = (norm_df.loc[(norm_df['Squad'] == team_name)].T).round(2)
    
    season_df = temp_team_df.groupby('Season').get_group(season).copy()
    
    normalized_df = normalize(season_df, leave_out)
    
    chunk = normalized_df.groupby(['Squad']).get_group(squad_name).T
    
    temp_team_df = pd.DataFrame(chunk).round(2).sum(axis = 1)
    #temp_team_df = temp_team_df.loc[stat_cols]
    #temp_team_df.index = stat_names
    temp_team_df = temp_team_df.reset_index() 
    
    temp_team_df.columns = [refr.theta_column_name, refr.radii_column_name]
    
    #first_stat_percentile = temp_team_df['Percentile'].iloc[0]
    #temp_team_df.loc[-1] = [stat_names[0], first_stat_percentile]
    
    return temp_team_df


### progression.py ###
def get_progression(player_name, stat_type, is_player=True):
    
    #leave_out = ['Squad', 
                 #'Season', 'Comp',
                 #'Nation', 'Pos']
    
    all_years_player = pd.DataFrame()
    years_active = []

    for year in range(2017,2024):
        
        #print(f'{year}_{year+1}')
        #print(player)
        if is_player:
            temp_df = pd.read_csv(f"data/{year}_{year+1}_all_outfield_players.csv", 
                              index_col = 'Player'
                              )
        else:
            temp_df = pd.read_csv(f"data/Squads_{year}_{year+1}_all_stats.csv", 
                              index_col = 'Squad'
                              )
        
        leave_out = [col for n, col in enumerate(temp_df.columns) if temp_df.dtypes.iloc[n] == 'O']
        
        stats_of_interest = list(refr.grouped_stats_player_comparison[stat_type].values())
        
        if player_name in temp_df.index.unique():
            
            years_active.append(f'{year}-{year+1}')
            
            # ['Player']
            norm_df = normalize(temp_df, leave_out)
            #norm_df = rank(temp_df, stats_of_interest)
            
            #print(norm_df[stats_of_interest])
            player = norm_df.loc[player_name]
            
            if isinstance(player, pd.core.frame.DataFrame):
                player = player.mean(numeric_only=True)
            
            all_years_player = pd.concat([all_years_player, player.T], axis = 1)

    all_years_player.columns = years_active

    #print(temp_df)
    all_years_player = all_years_player.loc[stats_of_interest]
    #all_years_player = all_years_player.drop(index = ['index','Nation', 'Pos', 'Age', 'Born', 'Squad', 'Comp', 'Pos'])

    all_years_player = all_years_player.reset_index()

    all_years_player = all_years_player.rename(columns = {'index' : 'stats'})
    
    return {'data' : all_years_player, 'years active' : years_active}