import streamlit as st


##### CONFIG ###### 
st.set_page_config(
    page_title="User Guide",
    layout="centered",
    #initial_sidebar_state="collapsed",
)
################### 


st.title('Home Page')
st.markdown("""Welcome to the STAT-SO App Home Page!""")
st.markdown("This app was created by Twitter User @NapoliSansone")
st.markdown('Here, you will learn about how to leverage this app to get the most out of it!')

st.divider()

#### Player and Club Comparisons
st.header('Player and Club Comparisons')
st.markdown("""
            #### Basics
            The polar Comparisons are a unique way to compare players or clubs over a number of different
            statistical categories.  Players and clubs can be compared over different seasons and can even 
            be compared with themselves from different seasons!
            """)

st.markdown(""" The polar graphs are created by taking a player or club's, say, 'Goal' statistics and normalizing 
            against every other player/club (respectively) from the chosen season which emits a percentile value from 0 to 1.
            These values can be presented on the polar system, where components (theta) is a given statistical category and
            the radii are the percentile for the corresponding category.
            """)

st.markdown("""Here is a basic example:""")

# , caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto"
cols = st.columns(2)
cols[0].image(image = 'media/example_image_1.png')
cols[0].caption("""This is an example of the comparison between Cristiano Ronaldo and Lionel Messi in the 2017-2018 season""")


cols[1].image(image = 'media/example_image_2.png')
cols[1].caption("""This is an example of the comparison between Lionel Messi and himself over multiple seasons as
                shown on the legend""")

st.markdown("""Both of the above examples can be done for clubs as well as players via the "Show Clubs" toggle on the top of the
            Comparisons page.  You can add up to 5 different players or clubs for Comparison.""")

st.markdown("""You can compare players and clubs over multiple pre-set statistical categories: Goalscoring, Shooting,
            Passing, Creation, Skills, Defense, Playing Time, and Misc.  Each category has sub-statistics that attempt
            to exemplify the pre-set categories.
            """)

st.markdown("""
            ##### Minimum Minutes Played
            As mentioned above, player or club stats are normalized against the stats of the other players/clubs during the
            same season.  Sometimes, this can provide confusing results if you allow the dataset to contain players who have 
            played a very short number of minutes.  For example, if a player has only played 10 minutes and scored, then that 
            player will likely have the highest percentile of Goals per 90, which a user might not want.
            """)

st.markdown("""
            To side-step this possible issue, a user can allow there to be a minimum minutes played.  This will cut players out
            of the dataset who have played less than a certain number of minutes (to be decided by the user).  This, as well as the
            aforementioned statistical category filter and under the header of 'Filters' on the Comparisons page of the app.
            """)

st.markdown("""
            ##### Per 90 Minutes Stats
            A user can also decide to view only the per 90 minute statistics.  This will show the Per 90 minute versions of 
            the stats that are on the default polar coordinates.  This can be toggled on and off via the 'Show Per 90' switch
            above the polar graphic!
            """)


st.divider()


st.header('Player Screener')
st.markdown("""
            #### Basics
            The player screener is an intuitive screener that lets one parse for the types of players that they want to see.
            Whether this person be scouting or simply interested which players fit a certain criteria, the screener has you covered.
            The screener can also help users view the player's strengths across a given set of stats!
            """)

st.markdown("""
            ##### Adding Extra Columns
            Users can choose to add extra columns for the stats that they are interested in looking at.  This is best to do
            after you have already filtered the data to the subset that you want to see!  Select however many columns you want
            to be added to your dataset, and they will populate!
            """)

st.markdown("""
            ##### Showing Percentile Data and Sorting
            This is where the screener really shines!  After adding columns of statistics you want to see, you can switch the
            'Show Percentile Data' toggle to On which will show the user a the percentiles for each statistical columns added!
            """)

st.markdown("""
            ##### The Mean Percentile Column
            In addition to the scaled columns, the 'Show Percentile Data' toggle will also add a 'Mean Percentile' column, which
            is defined as the mean of all the percentiles of the statistical columns that the user added!  This will show users
            the average of how highly rated players are across the statistics that the chose to add!
            """)


st.divider()


st.header('Contact')
st.markdown("""Do you have a suggested improvement or added functionality that you would like to see??""")

st.markdown("""Please, contact us!""")



#form = st.form("my_form")

st.markdown("""
            ##### Contact Information:
            """)

st.markdown('Email: napolisansone@gmail.com')
st.markdown('Twitter: NapoliSansone')
st.markdown('Github: Rhys 2024')