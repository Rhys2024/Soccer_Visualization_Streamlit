
from turtle import width
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import io

import references as refr
import helpers

import streamlit as st

######################################################  VARIABLES ######################################################
important_stats_comp = refr.important_stats_comp

#stats_available = refr.stats_available
#stats_of_interest = refr.stats_of_interest
#stats_of_interest_gk = refr.stats_of_interest_gk

all_players = refr.all_players
all_players.sort()

all_clubs = refr.all_clubs
all_clubs.sort()

summary_cols = ['Squad', 'Nation', 'Comp']

max_num_comparisons = 6

max_mins_for_curr_season = refr.data_players.groupby('Season').get_group(refr.curr_season)[refr.min_played_col].max()

config = {
  'toImageButtonOptions': {
    'format': 'svg', # one of png, svg, jpeg, webp
    'filename': 'custom_image',
    'height': 500,
    'width': 700,
    'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
  }
}

######################################################  HELPER FUNCTIONS ######################################################


def get_max_mins_for_curr_year():
    
    curr_season_data = refr.data_players.groupby('Season').get_group(refr.this_season)
    max_mins_played = curr_season_data[refr.min_played_col].dropna().max()
    
    return max_mins_played


def format_fig(fig, per_90, comp_stat):
    
    if per_90:
        plot_title = f"<b>{comp_stat} Stats (Per 90)</b>"
    else:
        plot_title = f"<b>{comp_stat} Stats</b>"
    
    fig_caption = f"With respect to {scale_against} during {scale_to}"
    
    plot_title = plot_title + f'<br><sup>{fig_caption}</sup>'
    
    fig.update_layout(
        title=dict(text=plot_title,
                        font=dict(
                            # Arial Black
                            family="Arial Black",
                            size=28,
                            #color='#000000'
                        )
                        , 
                        yref='paper'
                        ),
                      #template = 'seaborn',
                      #template="plotly_dark",
                      #template="plotly_white",
        legend=dict(
        traceorder='normal',
        font=dict(
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
    #width=850,
    #height=500,
    )
    fig.update_polars(radialaxis=dict(visible=False,
                                      range=[0, 1]))
    


def create_polar_figure(comp_stat, comp_names, temp_data, per_90):
    
    is_against_self = len(comp_names) == 1
    
    if not is_against_self:
        name_colors = {name : color for name, color in zip(comp_names, refr.figure_colors)}
    else:
        name_colors = {tags[1] : color for tags, color in zip(temp_data, refr.figure_colors)}
    
    
    fig = go.Figure()
    
    names_used = {}

    for frame in temp_data:
        
        name = frame[0]
        season = frame[1]
        
        if is_against_self:
            key = season
        else:
            key = name
        
        if key in names_used:
            names_used[key] += 1
        else:
            names_used[key] = 0
        
        if names_used[key] >= len(refr.discrete_palettes[name_colors[key]]):
            st.warning(f'Too many seasons selected for {name}')
            st.stop()
        
        line_col = refr.discrete_palettes[name_colors[key]][names_used[key]]
        
        # Scatterpolar
        # Scatterpolargl
        fig.add_trace(go.Scatterpolar(name = f'{season} {name}', 
                                      r = temp_data[frame][refr.radii_column_name],
                                        theta = temp_data[frame][refr.theta_column_name],
                                        fill = 'toself',
                                        hovertemplate =  f'<b>{season} {name}</b><br>' +
                                                            '<br><b>Percentile</b>: %{r}' +
                                                            '<br><b>Stat</b>: %{theta}<br>',
                                        line_color=line_col),
                      )
    
    format_fig(fig, per_90, comp_stat)
    
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


scale_maps = {'scale_to' : {''}}
    
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
def generate_frames(empty_frames, minimum_mins_played, scalings):
    
    if not st.session_state.show_clubs:
        data = refr.data_players.copy()
    else:
        data = refr.data_squads.copy()
        
    frames = empty_frames
    
    if len(seasons_selected) == 0:
        st.warning('Select Season(s) for Comparison!')
        st.stop()
    
    if refr.curr_season in seasons_selected and max_mins_for_curr_season < minimum_mins_played:
        st.warning(f"""No player in the Current Season has played over {minimum_mins_played}min - Adjusted the 'Minimum Minutes Played'""")
        st.stop()
    
    names_used = {}
    
    for frame in frames:
        
        name = frame[0]
        season = frame[1]
        
        if name in names_used:
            names_used[name] += 1
        else:
            names_used[name] = 1
        
        if not st.session_state.show_clubs:
            frames[frame] = helpers.player_performance(name, season, seasons_selected, 
                                                       data, scalings, minimum_mins_played)
        else:
            frames[frame] = helpers.team_performance(name, season, seasons_selected, data, 
                                                     scalings)
    
    return frames


######################################################  LAYOUT  ######################################################
 

##### CONFIG ###### 
st.set_page_config(
    page_title="Comparisons",
    layout="centered",
    initial_sidebar_state="collapsed",
)
################### 

# Create an in-memory buffer
buffer = io.BytesIO()

st.title("Comparisons")

show_clubs = st.toggle(label='Compare Clubs', 
        value=False, 
        key = 'show_clubs')

st.divider()

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

filter_cols1 = st.columns(2)

comp_stat = filter_cols1[0].selectbox(label='Statistical Category', 
        options=list(refr.new_grouped_stats_player_comparison.keys()),
        key = 'comp_stat')

if not show_clubs:
    min_min_played = filter_cols1[1].number_input(label='Minumum Minutes Played', 
                    min_value=0, 
                    max_value=90*30,
                    step= 90,
                    value=90,
                    key = 'min_played')
else:
    min_min_played = False


filter_cols2 = st.columns(2)

scale_to = filter_cols2[0].selectbox(label='Normalize To',
        options = refr.scale_to_options,
        key = 'scale_to')

scale_against = filter_cols2[1].selectbox(label='Normalize Against',
        options = refr.scale_against_options,
        key = 'scale_against')


if scale_against == 'Age Group':
    specs = filter_cols2[1].slider(label='Within How Many Years?',
        min_value = 0,
        max_value = 25,
        value = 2,
        )
else:
    specs = None


################## For Normalize against functionality ##################
scalings = {'to' : scale_to, 'against' : scale_against, 'specs' : specs}



if not show_clubs:
    per_90 = st.toggle(label='Show per 90 Stats', 
        value=False, 
        key = 'per_90')
else:
    per_90 = False


if not st.session_state.comp_stat:
    st.warning('Pick a Statistical Category')
    st.stop()


cols_and_names = get_stat_cols_and_names(per_90, comp_stat)


empty_frames = {(name, season) : [] for name in names_for_comp for season in st.session_state[f'{name}_seasons']}

seasons_selected = list({key[1] for key in empty_frames})

frames = generate_frames(empty_frames, min_min_played, scalings)

frames = get_relevant_stats(frames)

fig = create_polar_figure(comp_stat=st.session_state.comp_stat, 
                          comp_names = st.session_state.comp_names,
                            temp_data=frames, per_90=per_90)


fig_format = 'png'

fig.write_image(file=buffer, format=fig_format, engine="kaleido", scale=3, 
                width=1000, 
                height = 600)


st.download_button(
    label="Download PDF",
    data=buffer,
    file_name=f"figure.{fig_format}",
    mime=f"application/{fig_format}",
)

st.plotly_chart(fig)


st.divider()


show_true = st.toggle('Show True Data', value = False)

if not show_clubs and show_true:
    
    selecteds = list(frames.keys())
    
    data_to_viz = refr.data_players.copy().set_index(['Player', 'Season'])
    summary_cols = ['Age', 'Comp'] 
    data_to_viz = data_to_viz.loc[selecteds][summary_cols + cols_and_names['cols']]  
    data_to_viz.columns = summary_cols + cols_and_names['names']


    data_to_viz = data_to_viz.reset_index().set_index(['Player', 'Season'] + summary_cols)

    st.markdown("""##### True Data """)
    st.dataframe(data_to_viz)
    
