import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

import references as refr
import helpers

import streamlit as st



normalized_data = pd.read_csv('data/normalized_all_outfield_player_data.csv', index_col=0)

compare_matrix_non_adjusted = pd.read_csv('data/tax_compare_matrix_non_adjusted.csv', index_col='League')
num_datapts = pd.read_csv('data/tax_num_datapoints.csv', index_col='League')
age_diff = pd.read_csv('data/tax_age_diff.csv', index_col='League')
min_played_diff = pd.read_csv('data/tax_min_played_diff.csv', index_col='League')                      

df_master_figure = compare_matrix_non_adjusted.copy()
df_master_figure['Rank'] = df_master_figure['Rank'].astype(int).astype(str)

curr_best_league = compare_matrix_non_adjusted['Total Tax'].idxmin()
curr_tax_best_league = round(compare_matrix_non_adjusted['Total Tax'].min() * 100, 2)

curr_worst_league = compare_matrix_non_adjusted['Total Tax'].idxmax()
curr_tax_worst_league = round(compare_matrix_non_adjusted['Total Tax'].max() * 100, 2)


master_fig = px.bar(df_master_figure.reset_index().sort_values(by='Total Tax', ascending = False), 
       x = 'Total Tax', 
       y = 'League', 
       color = 'Rank',
       #labels= dict('Total Tax'="Total Bill ($)", tip="Tip ($)", sex="Payer Gender")
       )
master_fig.layout.xaxis.tickformat = ',.0%'
master_fig.update_yaxes(type='category')
# family='Rockwell', 
master_fig.update_yaxes(tickfont=dict(size=18,), title = '', showgrid=False)
master_fig.update_xaxes(tickfont=dict(size=18,), title = '', showgrid=True)
# paper_bgcolor="#FFCCCB",
master_fig.update_layout(showlegend=False)

combo_labels = [f"{combo[0]} vs {combo[1]}" for combo in refr.league_combos]
position_labels = [refr.tax_position_labels_mapper[pos] for pos in refr.tax_positions]


#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################  FUNCTIONS  ###################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################


def style_negative(v, props=''):
    return props if v < 0 else None
def style_pos(v, props=''):
    return props if v > 0 else None

#@st.cache_data()
def get_chunk(combo, players, pos, min_played):


    chunk = normalized_data[(normalized_data.Player.isin(players)) & 
                                    (normalized_data.Comp.isin(list(combo))) &
                                    (normalized_data.position == pos) &
                                    (normalized_data['Playing Time - Min'] > min_played)
                                ]
    
    return chunk

def make_position_tax_figure(data, pos_label):
    
    fig = px.bar(data, y = 'Stat', x = 'Mean Percentile',
                 color='Comp', title=pos_label, 
                 barmode="group")
    fig.layout.yaxis.tickformat = ',.0%'
    
    return fig

#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################  Layout  ######################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################

#st.set_page_config()

st.set_page_config(
    page_title="Tax",
    layout="wide",
    initial_sidebar_state="collapsed",
)
################### 

# Create an in-memory buffer

st.title("League Difficulty Tax")

#st.divider()

tabs = st.tabs(['Main', 'Positional Breakdown'])


message = f"""On average, players performed about {abs(curr_tax_best_league)}% worse in the {curr_best_league} compared to other top 5 leagues they played in. 
            Conversely, players who played in {curr_worst_league} played {abs(curr_tax_worst_league)}% worse that they did in other top 5 leagues."""

with tabs[0]:

    contain = st.container(border = True)
    
    with contain:
        cols_main = st.columns(2)
        
        cols_main[0].subheader('Total Tax per League')
        cols_main[0].plotly_chart(master_fig)
        
        cols_main[1].subheader('Pairwise League Comparison')
        cols_main[1].caption(message)
        cols_main[1].dataframe(compare_matrix_non_adjusted.drop('Rank', axis = 1).style.map(style_negative, 
                                                props='color:red;').map(style_pos, 
                                                props='color:green;'
                                                ).format("{:.2%}"), use_container_width=True)
        
    
    
    sub_cols = st.columns(3)
    sub_cols[0].subheader('Number of Datapoints')
    sub_cols[0].dataframe(num_datapts.fillna(0).astype(int))
    
    sub_cols[1].subheader('Age Differences')
    sub_cols[1].dataframe(age_diff.fillna(0).astype(int))
    
    sub_cols[2].subheader('Minutes Played Differences')
    sub_cols[2].dataframe(min_played_diff.style.format("{:.2%}"))
    
    
    



with tabs[1]:
    
    cols = st.columns(5)
    
    curr_combo_label = cols[1].selectbox('Choose Leagues to Compare', options = combo_labels)
    pos_label = cols[2].selectbox('Select Position', options = position_labels)
    min_played = cols[3].number_input('Minimum Min Played', min_value=0, max_value=90*30, step=90, value=90)
    
    curr_combo = [c.strip() for c in curr_combo_label.replace('vs', ',').split(',')]
    players = refr.multiple_league_players[curr_combo_label]
    
    #if pos_label != 'All':
    curr_pos = refr.tax_position_labels_mapper_r[pos_label]
    loc = [(curr_combo[0], curr_pos),(curr_combo[1], curr_pos)]
    groupby = ['Comp', 'position']
    #else:
        #curr_pos = None
        #loc = [curr_combo[0], curr_combo[1]]
        #groupby = 'Comp'
    
    temp_data = get_chunk(combo=curr_combo, players=players, pos=curr_pos, min_played=min_played)
    
    temp_data = temp_data[refr.tax_stats + ['Age', 'Comp', 'position', 'Playing Time - Min']]
    
    st.subheader(f'{curr_combo_label} - {pos_label}')
    
    cols2 = st.columns(2)
    cols3 = st.columns(2)
    
    # .loc[loc][refr.tax_stats_grouped['Defensive']].T
    
    if curr_pos != 'GK':
        output_fig_df = temp_data.groupby(groupby
                    ).mean().loc[loc][refr.tax_stats_grouped['Output']].T.droplevel(1,1).stack().reset_index()
        output_fig_df.columns = ['Stat', 'Comp', 'Mean Percentile']
        creation_fig_df = temp_data.groupby(groupby
                    ).mean().loc[loc][refr.tax_stats_grouped['Creation']].T.droplevel(1,1).stack().reset_index()
        creation_fig_df.columns = ['Stat', 'Comp', 'Mean Percentile']
        defending_fig_df = temp_data.groupby(groupby
                    ).mean().loc[loc][refr.tax_stats_grouped['Defending']].T.droplevel(1,1).stack().reset_index()
        defending_fig_df.columns = ['Stat', 'Comp', 'Mean Percentile']
        
        output_fig = make_position_tax_figure(data=output_fig_df, pos_label='Output')
        creation_fig = make_position_tax_figure(data=creation_fig_df, pos_label='Creation')
        defending_fig = make_position_tax_figure(data=defending_fig_df, pos_label='Defending')
        
    else:
        gk_fig_df = temp_data.groupby(groupby
                    ).mean().loc[loc][refr.tax_stats_grouped['Goalkeeping']].T.droplevel(1,1).stack().reset_index()
        gk_fig_df.columns = ['Stat', 'Comp', 'Mean Percentile']
        gk_fig = make_position_tax_figure(data=gk_fig_df, pos_label='Goalkeeping')
    
    if curr_pos == 'GK':
        st.plotly_chart(gk_fig)
    else:
        cols2[0].plotly_chart(output_fig)
        cols2[1].plotly_chart(creation_fig)
        cols3[0].plotly_chart(defending_fig)
    
    #st.dataframe(fig_df)
    

    #contain = st.container(border = True)
    #with contain:



