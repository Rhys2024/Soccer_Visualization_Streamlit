import streamlit as st


##### CONFIG ###### 
st.set_page_config(
    page_title="Welcome",
    layout="centered",
    #initial_sidebar_state="collapsed",
)
################### 


st.title('Home Page')
st.markdown("""Welcome to the Sanso-Visuals App!""")
st.markdown("This app was created by Twitter User @NapoliSansone")
#st.markdown('Here, you will learn about how to leverage this app to get the most out of it!')

st.divider()

st.subheader('Contact')
st.markdown("""Do you have a suggested improvement or added functionality that you would like to see??""")

st.markdown("""Please, contact us!""")


st.markdown("""
            ##### Contact Information:
            """)

st.markdown('Email: napolisansone@gmail.com')
st.markdown('Twitter: NapoliSansone')
st.markdown('Github: Rhys2024')