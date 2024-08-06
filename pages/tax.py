import plotly.graph_objects as go
import pandas as pd
import numpy as np

import references as refr
import helpers

import streamlit as st



normalized_data = pd.read_csv('data/normalized_all_outfield_player_data.csv')



###################################################################################################################################
###################################################################################################################################
################################################################  LAYOUT  #########################################################
###################################################################################################################################
###################################################################################################################################


st.set_page_config(
    page_title="Tax",
    layout="centered",
    initial_sidebar_state="collapsed",
)
################### 

# Create an in-memory buffer

st.title("League Difficulty")

st.divider()


#filter_cols1 = st.columns(2)




