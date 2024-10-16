from cProfile import label
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

import references as refr
import helpers

import streamlit as st



normalized_data = pd.read_csv('data/normalized_all_outfield_player_data.csv', index_col=0)
normalized_data.columns.name = 'Stat'

compare_matrix_non_adjusted = pd.read_csv('data/tax_compare_matrix_non_adjusted.csv', index_col='League')
num_datapts = pd.read_csv('data/tax_num_datapoints.csv', index_col='League')
age_diff = pd.read_csv('data/tax_age_diff.csv', index_col='League')
min_played_diff = pd.read_csv('data/tax_min_played_diff.csv', index_col='League')                      

df_master_figure = compare_matrix_non_adjusted.copy()
df_master_figure['Rank'] = df_master_figure['Rank'].astype(int).astype(str)

df_master_figure = df_master_figure.reset_index().sort_values(by='Total Tax', ascending = False)

curr_best_league = compare_matrix_non_adjusted['Total Tax'].idxmin()
curr_tax_best_league = round(compare_matrix_non_adjusted['Total Tax'].min() * 100, 2)

curr_worst_league = compare_matrix_non_adjusted['Total Tax'].idxmax()
curr_tax_worst_league = round(compare_matrix_non_adjusted['Total Tax'].max() * 100, 2)

xlim = helpers.get_lims(df_master_figure, 'Total Tax')


master_fig = px.bar(df_master_figure, 
       x = 'Total Tax', 
       y = 'League', 
       color = 'Rank',
       #labels= dict('Total Tax'="Total Bill ($)", tip="Tip ($)", sex="Payer Gender")
       )


master_fig.layout.xaxis.tickformat = ',.0%'
master_fig.update_yaxes(type='category')
# family='Rockwell', 
master_fig.update_yaxes(tickfont=dict(size=18,), title = '', showgrid=True, tickson="boundaries",)
master_fig.update_xaxes(tickfont=dict(size=18,), title = '', showgrid=False)
master_fig.update_layout(showlegend=False)
master_fig.update_layout(xaxis_range=[-xlim,xlim])
master_fig.add_shape(type="line", line_dash="dash", 
                  line_color = 'darkgrey',x0=.5,y0=0,x1=.5,y1=1,xanchor='center',xref="paper",yref="paper")


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


def get_figure_dataframe(temp_data, stats, loc):
    
    league_1 = loc[0][0]
    league_2 = loc[1][0]
    
    
    temp1 = temp_data.groupby(groupby
                    ).mean().loc[loc][stats].droplevel(1, 0).T
    
    temp1['Difference'] = temp1[league_1] - temp1[league_2]
    temp1['Better League?'] = temp1['Difference'].apply(lambda val: league_1 if val < 0 else league_2)
    temp1 = temp1.reset_index()
    temp1.columns.name = None
    
    return temp1

def make_position_tax_figure(data, pos_label, loc):
    
    league_1 = loc[0][0]
    league_2 = loc[1][0]
    
    color_one = 'goldenrod'
    # bisque
    color_two = 'darkkhaki'
    #bar_color = 'red'
    
    max_val = data['Difference'].max() + (data['Difference'].max() * .15)
    min_val = data['Difference'].min() + (data['Difference'].min() * .15)
    
    if abs(min_val) > max_val:
        max_val = -min_val
    else:
        min_val = -max_val
    
    fig = px.bar(data, y = 'Stat', x = 'Difference',
                 #title=pos_label,
                 text=data['Difference'].apply(lambda x: '{0:1.0f}%'.format(x*100)),
                 labels={'text' : 'Difference'},
                 #color_discrete_sequence = [bar_color],
                 # ".", "+",
                 #pattern_shape_sequence=["."]
                 #hover_data = {'Difference' : ':.0f%'}
                 )
    fig.add_shape(type="line", line_dash="dash", 
                  line_color = 'black',x0=.5,y0=0,x1=.5,y1=1,xanchor='center',xref="paper",yref="paper")
    
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=60))
    
    fig.add_annotation(dict(font=dict(color='white',size=25, family='verdana'),
                                        x=.5,
                                        y=1.10,
                                        showarrow=False,
                                        #Bar chart
                                        text=f"<b>Better {pos_label}?</b>",
                                        #textsize=15,
                                        textangle=0,
                                        xanchor='center',
                                        align = 'center',
                                        xref="paper",
                                        yref="paper"))
    fig.update_xaxes(title='', showticklabels = False)
    fig.update_yaxes(showgrid=True, tickson="boundaries", title='')
    fig.layout.xaxis.tickformat = ',.0%'
    fig.add_vrect(
    x0=0, x1=max_val,
    fillcolor=color_one, opacity=0.5,
    layer="below", line_width=0,
    )
    fig.add_vrect(
    x0=min_val, x1=0,
    fillcolor=color_two, opacity=0.5,
    layer="below", line_width=0,
    )
    
    fig.add_annotation(dict(font=dict(color=color_two,size=20),
                                        x=.25,
                                        y=-0.12,
                                        showarrow=False,
                                        text=f"{league_1}",
                                        #textsize=15,
                                        textangle=0,
                                        xanchor='center',
                                        align = 'center',
                                        xref="paper",
                                        yref="paper"))
    fig.add_shape(type="line",line_color = color_two,x0=0,y0=-.01,x1=0,y1=-.04,xanchor='center',xref="paper",yref="paper")
    fig.add_shape(type="line",line_color = color_two,x0=0,y0=-.04,x1=.47,y1=-.04,xanchor='center',xref="paper",yref="paper")
    fig.add_shape(type="line",line_color = color_two,x0=.47,y0=-.04,x1=.47,y1=-.01,xanchor='center',xref="paper",yref="paper")
    
    fig.add_annotation(dict(font=dict(color=color_one,size=20),
                                        x=1-.25,
                                        y=-0.12,
                                        showarrow=False,
                                        text=f"{league_2}",
                                        #textsize=15,
                                        textangle=0,
                                        xanchor='center',
                                        align = 'center',
                                        xref="paper",
                                        yref="paper"))
    fig.add_shape(type="line",line_color = color_one,x0=1,y0=-.01,x1=1,y1=-.04,xanchor='center',xref="paper",yref="paper")
    fig.add_shape(type="line",line_color = color_one,x0=1,y0=-.04,x1=1-.47,y1=-.04,xanchor='center',xref="paper",yref="paper")
    fig.add_shape(type="line",line_color = color_one,x0=1-.47,y0=-.04,x1=1-.47,y1=-.01,xanchor='center',xref="paper",yref="paper")
    
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


message = f"""On average, players performed about {abs(int(curr_tax_best_league))}% worse in the {curr_best_league} compared to other top 5 leagues they played in. 
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
    
    st.divider()
    
    curr_combo = [c.strip() for c in curr_combo_label.replace('vs', ',').split(',')]
    players = refr.multiple_league_players[curr_combo_label]

    curr_pos = refr.tax_position_labels_mapper_r[pos_label]
    loc = [(curr_combo[0], curr_pos),(curr_combo[1], curr_pos)]
    groupby = ['Comp', 'position']
    
    temp_data = get_chunk(combo=curr_combo, players=players, pos=curr_pos, min_played=min_played)
    
    sample_of_players = temp_data[['Player', 'Season', 'Squad', 'Age']].copy()
    
    temp_data = temp_data[refr.tax_stats + ['Age', 'Comp', 'position', 'Playing Time - Min']]
    

    cols2 = st.columns(2)
    
    if curr_pos != 'GK':
        output_fig_df = get_figure_dataframe(temp_data, refr.tax_stats_grouped['Output'], loc)
        creation_fig_df = get_figure_dataframe(temp_data, refr.tax_stats_grouped['Creation'], loc)
        defending_fig_df = get_figure_dataframe(temp_data, refr.tax_stats_grouped['Defending'], loc)
        
        output_fig = make_position_tax_figure(data=output_fig_df, 
                                              pos_label='Output', loc=loc)
        creation_fig = make_position_tax_figure(data=creation_fig_df, pos_label='Creation', loc=loc)
        defending_fig = make_position_tax_figure(data=defending_fig_df, pos_label='Defending', loc=loc)
        
    else:
        gk_fig_df = get_figure_dataframe(temp_data, refr.tax_stats_grouped['Goalkeeping'], loc)
        gk_fig = make_position_tax_figure(data=gk_fig_df, pos_label='Goalkeeping', loc=loc)
    
    if curr_pos == 'GK':
        cols2[0].plotly_chart(gk_fig)
        cols2[1].subheader(f'{pos_label}')
        cols2[1].dataframe(sample_of_players, use_container_width=True, hide_index=True)
    else:
        cols2[0].plotly_chart(output_fig)
        cols2[0].plotly_chart(defending_fig)
        cols2[1].plotly_chart(creation_fig)
        cols2[1].subheader(f'{pos_label} in this Sample')
        cols2[1].dataframe(sample_of_players, use_container_width=True, hide_index=True)



