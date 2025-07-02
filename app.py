import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

import preprocessor,helper

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("SUMMER OLYMPIC ANALYSIS")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", caption="Olympic Games")


user_menu=st.sidebar.radio(
    'SELECT AN OPTION',
    ('MEDAL TALLY','OVERALL ANALYSIS','COUNTRY-WISE ANALYSIS','ATHELETE-WISE ANALYSIS')
)


if user_menu=='MEDAL TALLY':
    st.sidebar.header('MEDAL TALLY')
    years,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)

    if(selected_year=='Overall' and selected_country=='Overall'):
        st.title("Overall Medal Tally")
    if(selected_year!='Overall' and selected_country=='Overall'):
        st.title("Overall Medal Tally in : " + str(selected_year) )
    if (selected_year=='Overall' and selected_country!='Overall'):
        st.title("Overall Medal Tally of : " + selected_country )
    if (selected_year!='Overall' and selected_country!='Overall'):
        st.title("Overall Medal Tally of " + selected_country + " in the year " + str(selected_year) )
    st.table(medal_tally)


if user_menu=='OVERALL ANALYSIS':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    atheletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.title("TOP STATISTICS")

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(atheletes)
    with col3:
        st.header("Athletes")
        st.title(nations)


    nations_overtime=helper.data_overtime(df,'region')
    fig = px.line(nations_overtime, x="Year", y="count", markers=True)
    fig.update_layout(
        title="Number of Nations Participating Over the Years",
        xaxis_title="Year",
        yaxis_title="Number of Nations"
    )
    st.plotly_chart(fig)

    events_overtime=helper.data_overtime(df,'Event')
    fig = px.line(events_overtime, x="Year", y="count", markers=True)
    fig.update_layout(
        title="Number of Events Over the Years",
        xaxis_title="Year",
        yaxis_title="Number of Events"
    )
    st.plotly_chart(fig)

    athletes_overtime = helper.data_overtime(df, 'Name')
    fig = px.line(athletes_overtime, x="Year", y="count", markers=True)
    fig.update_layout(
        title="Number of Athletes Over the Years",
        xaxis_title="Year",
        yaxis_title="Number of Athletes"
    )
    st.plotly_chart(fig)

    st.title("No. of Events over time(EVERY SPORT)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)

    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select a Sport',sport_list)

    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='COUNTRY-WISE ANALYSIS':

    st.sidebar.title("Country-Wise Analysis")

    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('Select a Country',country_list)

    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal", markers=True)
    fig.update_layout(
        title= selected_country + " Medal Tally Over the Years",
        xaxis_title="Year",
        yaxis_title="Number of Medals"
    )
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following Sports")
    pt=helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)

    st.pyplot(fig)

    st.title("Top 15 Athletes of " + selected_country)
    top15_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top15_df)

if user_menu=='ATHELETE-WISE ANALYSIS':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalsit', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)

    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age w.r.t Sports (Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=50)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


