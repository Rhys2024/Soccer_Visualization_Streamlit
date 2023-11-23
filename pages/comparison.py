
from json.tool import main
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import references as refr
import helpers
import plotly.express as px

import streamlit as st


import UpdateData as up



######################################################  VARIABLES ######################################################
important_stats_comp = refr.important_stats_comp

stats_available = refr.stats_available
stats_of_interest = refr.stats_of_interest
stats_of_interest_gk = refr.stats_of_interest_gk

all_players = refr.all_players
all_players.sort()

all_clubs = refr.all_clubs
all_clubs.sort()

summary_cols = ['Squad', 'Nation', 'Comp']

max_num_comparisons = 6

#data_players = refr.data_players
#data_squads = refr.data_squads

curr_season = '2023-2024'

######################################################  HELPER FUNCTIONS ######################################################


def get_max_mins_for_curr_year():
    
    curr_season_data = refr.data_players.groupby('Season').get_group(curr_season)
    max_mins_played = curr_season_data[refr.min_played_col].dropna().max()
    
    return max_mins_played

def create_polar_figure(comp_stat, temp_data, per_90):
    
    fig = go.Figure()
    
    comp_names = st.session_state.comp_names
    is_against_self = len(comp_names) == 1
    
    if not is_against_self:
        name_colors = {name : color for name, color in zip(comp_names, refr.figure_colors)}
    else:
        name_colors = {tags[1] : color for tags, color in zip(temp_data, refr.figure_colors)}
    
    names_used = {}
    
    for frame in temp_data:
        
        name = frame[0]
        season = frame[1]
        
        if name in names_used:
            names_used[name] += 1
        else:
            names_used[name] = 0
        
        if is_against_self:
            key = season
        else:
            key = name
        
        if names_used[name] >= len(refr.discrete_palettes[name_colors[key]]):
            st.warning(f'Too many seasons selected for {name}')
            st.stop()
        
        line_col = refr.discrete_palettes[name_colors[key]][names_used[name]]
        
        fig.add_trace(go.Scatterpolargl(name = f'{season} {name}', 
                                      r = temp_data[frame][refr.radii_column_name],
                                        theta = temp_data[frame][refr.theta_column_name],
                                        fill = 'toself',
                                        hovertemplate =  f'<b>{season} {name}</b><br>' +
                                                            '<br><b>Percentile</b>: %{r}' +
                                                            '<br><b>Stat</b>: %{theta}<br>',
                                        line_color=line_col),
                      )
    
    if per_90:
        plot_title = f"(Per 90) {comp_stat} Stats"
    else:
        plot_title = f"{comp_stat} Stats"
    
    fig.update_layout(title=dict(text=plot_title,
                                 font=dict(
                                        # Arial Black
                                        family="Arial Black",
                                        size=30,
                                        #color='#000000'
                                    )
                                 , yref='paper'
                                 ), 
                      #template = 'seaborn',
                      #template="plotly_dark",
                      #template="plotly_white",
                      legend=dict(
        traceorder='normal',
        font=dict(
            # sans-serif
            family='Arial Black',
            size=14,
            color='#000000'
        ),
        bgcolor='#E2E2E2',
        bordercolor='#FFFFFF',
        borderwidth=2
        
    ),
    showlegend = True,
    autosize=False,
    width=900,
    height=400
    )
    fig.update_polars(radialaxis=dict(visible=False,
                                      range=[0, 1]))
    
    return fig


def get_relevant_stats(frames):
    
    for frame in frames:
        
        temp_df = frames[frame].copy()
        
        temp_df = temp_df[temp_df[refr.theta_column_name].isin(cols_and_names['cols'])]
        temp_df[refr.theta_column_name] = cols_and_names['names']
        
        first_stat_percentile = temp_df[refr.radii_column_name].iloc[0]
        temp_df.loc[-1] = [cols_and_names['names'][0], first_stat_percentile]
        
        temp_df[refr.radii_column_name] = temp_df.apply(lambda row: helpers.invert(row, st.session_state.comp_stat),
                                                        axis = 1)
        
        frames[frame] = temp_df
    
    return frames


def check_mins_played(empty_frames):
    
    # st.session_state.min_played
    minimum_mins_played = min_min_played
    
    
    is_error = False
    
    if show_clubs:
        temp_data = refr.data_squads
        temp_name = 'Squad'
    else:
        temp_data = refr.data_players
        temp_name = 'Player'
    
    for descr in empty_frames:
        
        name, season = descr
        
        name_chunk = temp_data.groupby([temp_name, 'Season']).get_group((name, season))
        
        mins_played = name_chunk[refr.min_played_col].values[0]
        
        if mins_played < minimum_mins_played:
            is_error = True
            st.warning(f"{name} has not played more than 'Minimum Minutes Played'")
    
    if is_error:       
        st.stop()


def get_stat_cols_and_names(per_90, comp_stat):
    
    if not per_90:
        stat_cols = list(i['normal_name'] for i in refr.new_grouped_stats_player_comparison[comp_stat].values())
    else:
        stat_cols = list(i['per_90_name'] for i in refr.new_grouped_stats_player_comparison[comp_stat].values())
    stat_names = list(refr.new_grouped_stats_player_comparison[comp_stat].keys())
    
    return {'cols' : stat_cols, 'names' : stat_names}



######################################################  LAYOUT FUNCTIONS ######################################################

def write_seasons(seasons_data):
    
    #with main_form:
    max_names_per_row = 3
    num_names = len(seasons_data)
    
    if num_names > max_names_per_row:
        layered = True
    else:
        layered = False
    
    if not layered:
        subs = st.columns(num_names)
    
        for n, name in enumerate(seasons_data):
            
            temp_years = seasons_data[name]
            
            subs[n].multiselect(label=name, 
                        options = temp_years,
                        default = temp_years[-1],
                        placeholder="Select a season",
                        key = f'{name}_seasons'
                        )
    else:
        subs1 = st.columns(max_names_per_row)
        subs2 = st.columns(max_names_per_row)
        
        for n, name in enumerate(seasons_data):
            
            temp_years = seasons_data[name]
            
            if n < max_names_per_row:
                subs1[n].multiselect(label=name, 
                        options = temp_years,
                        default = temp_years[-1],
                        placeholder="Select a season",
                        key = f'{name}_seasons'
                        )
            else:
                subs2[n - max_names_per_row].multiselect(label=name, 
                        options = temp_years,
                        default = temp_years[-1],
                        placeholder="Select a season",
                        key = f'{name}_seasons'
                        )
    
    
    
############################# CACHED FUNCTIONS #############################


@st.cache_data()
def get_seasons_data(comp_names):
    
    #comp_names = st.session_state.comp_names
    
    warning_insert = 'Clubs' if st.session_state.show_clubs else 'Players'
    
    if len(comp_names) < 1:
        st.warning(f'Must Select a {warning_insert[:-1]} for Comparison')
        st.stop()
    
    if len(comp_names) > max_num_comparisons:
        st.warning(f'Must Select at MOST 5 {warning_insert} for Comparison')
        st.stop()
    
    if not st.session_state.show_clubs:
        season_played = refr.seasons_played_per_player
    else:
        season_played = refr.squads_per_season
    
    seasons_per_player = {name : season_played[name] 
                          for name in comp_names}
    
    return seasons_per_player


@st.cache_data()
def generate_frames(empty_frame, minimum_mins_played):
    
    if not st.session_state.show_clubs:
        data = refr.data_players.copy()
    else:
        data = refr.data_squads.copy()
        
    frames = empty_frame
    
    seasons_selected = list({key[1] for key in frames})
    
    check_mins_played(frames)
    
    max_mins = data[refr.min_played_col].max()
    
    if max_mins < minimum_mins_played:
        st.warning('CAPPP')
        st.stop()
    
    temp_data = data[data[refr.min_played_col] > minimum_mins_played].copy()
    
    for frame in frames:
        
        name = frame[0]
        season = frame[1]
        
        if not st.session_state.show_clubs:
            frames[frame] = helpers.player_performance(name, season, seasons_selected, temp_data)
        else:
            frames[frame] = helpers.team_performance(name, season, temp_data)
    
    return frames




######################################################  LAYOUT  ######################################################
 

##### CONFIG ###### 
st.set_page_config(
    page_title="Comparisons",
    layout="centered",
    initial_sidebar_state="collapsed",
)
################### 


st.title("Comparisons")

show_clubs = st.toggle(label='Compare Clubs', 
        value=False, 
        key = 'show_clubs')

st.divider()

#main_form = st.form(key = "main_form")

#with main_form:

if not st.session_state.show_clubs:
    club_or_player = 'Player'
    st.markdown(f'#### {club_or_player} Selection')
    names_for_comp = st.multiselect(label = 'Pick Players for Comparison',
                    options = all_players,
                    default = ['Kylian Mbappe', 'Vinicius Junior'],
                    key='comp_names')
else:
    club_or_player = 'Club'
    st.markdown(f'#### {club_or_player} Selection')
    names_for_comp = st.multiselect(label = 'Pick Clubs for Comparison',
                    options = all_clubs,
                    default = ['Real Madrid', 'Barcelona'],
                    key='comp_names')


seasons_data = get_seasons_data(names_for_comp)

write_seasons(seasons_data)


st.divider()


st.markdown("#### Filters")

col1, col2, col3 = st.columns(3)

if not show_clubs:
    per_90 = st.toggle(label='Show per 90 Stats', 
        value=False, 
        key = 'per_90')
    min_min_played = col2.number_input(label='Minumum Minutes Played', 
                    min_value=0, 
                    max_value=90*30,
                    step= 90,
                    value=90,
                    key = 'min_played')
else:
    per_90 = False
    min_min_played = 0

comp_stat = col1.selectbox(label='Statistical Category', 
        options=list(refr.grouped_stats_player_comparison.keys()),
        #default = list(refr.grouped_stats_player_comparison.keys())[0],
        key = 'comp_stat')

scale_to = col3.selectbox(label='Normalize Against',
        options= ['Season', 'All Seasons Selected', 'All Seasons Available'],
        #default = list(refr.grouped_stats_player_comparison.keys())[0],
        key = 'scale_to')


cols_and_names = get_stat_cols_and_names(per_90, comp_stat)


if not st.session_state.comp_stat:
    st.warning('Pick a Statistical Category')
    st.stop()

## For Normalize against functionality

empty_frame = {(name, season) : [] for name in names_for_comp for season in st.session_state[f'{name}_seasons']}


frames = generate_frames(empty_frame, min_min_played)

frames = get_relevant_stats(frames)

fig = create_polar_figure(comp_stat=st.session_state.comp_stat,
                            temp_data=frames, per_90=per_90)


st.plotly_chart(fig)


if not show_clubs:
    
    selecteds = list(frames.keys())
    
    data_to_viz = refr.data_players.copy().set_index(['Player', 'Season'])
    summary_cols = ['Age', 'Comp'] 
    data_to_viz = data_to_viz.loc[selecteds][summary_cols + cols_and_names['cols']]  
    data_to_viz.columns = summary_cols + cols_and_names['names']


    data_to_viz = data_to_viz.reset_index().set_index(['Player', 'Season'] + summary_cols)

    st.markdown("""##### True Data """)
    st.dataframe(data_to_viz)
    
