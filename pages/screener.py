import references as refr
import helpers


import streamlit as st


######################################################  VARIABLES ######################################################

#data_players = pd.read_csv(f"data/new_all_outfield_player_data.csv")

summary_cols = ['Player', 'Age', 'Season', refr.pos_col, 
                refr.league_col, 'Squad', refr.min_played_col,
                'Performance - Gls']

unnamed_cols = [col for col in refr.data_players.columns if 'Unnamed' in col]

data = refr.data_players.drop(columns=unnamed_cols).copy()

######################################################  LAYOUT  ######################################################
 
 
 
 
######################################################  HELPER FUNCTIONS  ######################################################


def clip_age(temp_data, lb, ub):
    
    clipped = temp_data[ (temp_data['Age'] >= lb) 
              &
              (temp_data['Age'] <= ub)]
    
    return clipped


def multi_val_parse(data, col, vals):
    
    return data[data[col].isin(vals)]


def handle_percentiles(temp_data, cols):
    
    leave_outs = [col for col in temp_data.columns if col not in cols]
    
    normalized_df = helpers.normalize(temp_data, leave_outs=leave_outs).fillna(0.0)
    normalized_df['Mean Percentile'] = normalized_df[cols].mean(axis =1).round(2)
    
    return normalized_df
 
 
######################################################  FUNCTIONS  ######################################################


def partitionData(data, positions, leagues, age_range, 
                  min_played, seasons):
    
    age_lb, age_ub = age_range
    
    if 'All' not in positions and len(positions) > 0:
        data = multi_val_parse(data, refr.pos_col, positions)
    if 'All' not in leagues and len(leagues) > 0:
        data = multi_val_parse(data, refr.league_col, leagues)
    if 'All' not in seasons and len(seasons) > 0:
        data = multi_val_parse(data, 'Season', seasons)
    
    data = clip_age(data, age_lb, age_ub)
    
    data = data[data[refr.min_played_col] >= min_played]
    
    return data
    


##### CONFIG ###### 
st.set_page_config(
    page_title="Screener",
    # wide
    # centered
    layout="wide",
    initial_sidebar_state="collapsed",
)
################### 


st.title("Player Screener")


st.divider()


#st.markdown("#### Filters")
st.subheader('Filters')

#apply_filters_form = st.form('apply_filters_form')

#with apply_filters_form:
    
cols1 = st.columns(5)

cols1[0].multiselect(label = 'Filter by Position',
                    options = ['All'] + refr.positions,
                    default = 'All',
                    #default = default_vars,
                    key='positions')


cols1[1].multiselect(label = 'Filter by League',
                    options = ['All'] + refr.leagues,
                    default = 'All',
                    #default = default_vars,
                    key='leagues')

cols1[2].slider(
                "Filter by Age",
                min_value=14,
                max_value=50,
                value=(21, 31),
                key='age_range'
                )

cols1[3].number_input(
                "Filter by Min Played",
                min_value=1,
                max_value=90*30,
                value = 90,
                key='min_played'
                )

cols1[4].multiselect(
                "Filter by Season",
                options = ['All'] + list(refr.data_players.Season.unique()),
                default = ['All'],
                key='seasons'
                )


st.divider()


cols2 = st.columns(3)

add_cols = list(refr.screener_available_stats.keys())
add_cols.remove('Goals')
#list(set(refr.data_players.columns).difference(set(summary_cols)))

cols2[0].multiselect(label='Add Extra Columns', 
               options = add_cols,
               key = 'added_cols')


col_names = [refr.screener_available_stats[name] for name in st.session_state.added_cols]

visible_columns = summary_cols + col_names

data = data[visible_columns].copy()

    
partition_data = partitionData(data = data,
                            positions=st.session_state.positions, 
                            leagues=st.session_state.leagues, 
                            age_range=st.session_state.age_range, 
                            min_played=st.session_state.min_played,
                            seasons = st.session_state.seasons)


st.toggle('Show Percentile Data', value = False, key = 'pct_data')

if st.session_state.pct_data:
    partition_data = handle_percentiles(partition_data, cols = ['Performance - Gls'] + col_names)


st.divider()
st.dataframe(partition_data.set_index('Player').sort_values(by='Performance - Gls'))









