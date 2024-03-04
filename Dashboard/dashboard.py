!pip install plotly==5.3.1
import plotly.express as px
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; background-color: #f3f3f3; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <div style="text-align: center;">
            <h1 style="margin: 0; font-size: 2em; color: #333;">Dicoding Final Project</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

day_df = pd.read_csv("/Users/laurivasy/Desktop/Bike-Sharing/Dashboard/bike-sharing-cleaned-day.csv")
hour_df = pd.read_csv("/Users/laurivasy/Desktop/Bike-Sharing/Dashboard/bike-sharing-cleaned-hour.csv")
hour_df['date'] = pd.to_datetime(hour_df['date'])
day_df['date'] = pd.to_datetime(day_df['date'])


def create_hourly_users(hour_df):
    hourly_users = hour_df.groupby("hour").agg({
        "casual": "sum",
        "registered": "sum",
        "total": "sum"
    })
    hourly_users = hourly_users.reset_index()
    hourly_users.rename(columns={
        "total": "total",
        "casual": "casual_customers",
        "registered": "registered_customers"
    }, inplace=True)
    
    return hourly_users

def create_monthly_users(hour_df):
    monthly_users = hour_df.resample(rule='M', on='date').agg({
        "casual": "sum",
        "registered": "sum",
        "total": "sum"
    })
    monthly_users.index = monthly_users.index.strftime('%b-%y')
    monthly_users = monthly_users.reset_index()
    monthly_users.rename(columns={
        "date": "yearmonth",
        "total": "total",
        "casual": "casual_customers",
        "registered": "registered_customers"
    }, inplace=True)

    return monthly_users

def create_seasonly_users(hour_df):
    seasonly_users_df = hour_df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "total": "sum"
    })
    seasonly_users = seasonly_users_df.reset_index()
    seasonly_users.rename(columns={
        "total": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    seasonly_users = pd.melt(seasonly_users,
                             id_vars=['season'],
                             value_vars=['casual_rides', 'registered_rides'],
                             var_name='user_status',
                             value_name='total')

    seasonly_users['season'] = pd.Categorical(seasonly_users['season'],
                                              categories=['Spring', 'Summer', 'Fall', 'Winter'])

    seasonly_users = seasonly_users.sort_values('season')

    return seasonly_users

def create_weekday_users(hour_df):
    weekday_users = hour_df.groupby("day").agg({
        "casual": "sum",
        "registered": "sum",
        "total": "sum"
    })
    weekday_users = weekday_users.reset_index()
    weekday_users.rename(columns={
        "total": "total",
        "casual": "casual_customers",
        "registered": "registered_customers"
    }, inplace=True)

    weekday_users = pd.melt(weekday_users,
                            id_vars=['day'],
                            value_vars=['casual_customers', 'registered_customers'],
                            var_name='user_status',
                            value_name='total')

    weekday_users['day'] = pd.Categorical(weekday_users['day'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    weekday_users = weekday_users.sort_values('day')

    return weekday_users

# Sidebar content
selected_view = st.sidebar.selectbox("Select Data View", ["Hourly", "Daily", "Monthly", "Seasonal"])


hourly_users = create_hourly_users(hour_df)
monthly_users = create_monthly_users(hour_df)
seasonly_users= create_seasonly_users(hour_df)
weekday_users = create_weekday_users(hour_df)


# Mainpage Content
st.title("Bike-Sharing Dataset Dashboard")
metrics_container = st.container()

metrics_container.markdown(
    """
    <style>
        .metric-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
        }

        .metric-title {
            font-size: 14px;
            color: black;
            margin-bottom: 5px;
            background-color: white;
            padding: 5px 10px;
            border-radius: 5px;
            text-align: center;
        }

        .metric-value {
            font-size: 2em;
            color: white;
            text.align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = metrics_container.columns(3)

with col1:
    total_all_rides = hour_df['total'].sum()
    st.markdown("<p class='metric-title'>Total Bike Rides</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='metric-value'>{total_all_rides}</p>", unsafe_allow_html=True)

with col2:
    total_casual_rides = hour_df['casual'].sum()
    st.markdown("<p class='metric-title'>Total Casual User Rides</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='metric-value'>{total_casual_rides}</p>", unsafe_allow_html=True)

with col3:
    total_registered_rides = hour_df['registered'].sum()
    st.markdown("<p class='metric-title'>Total Registered User Rides</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='metric-value'>{total_registered_rides}</p>", unsafe_allow_html=True)


st.markdown("---")

col1 = st

if selected_view == "Hourly":
    fig1 = px.line(hourly_users,
                   x='hour',
                   y=['casual_customers', 'registered_customers'],
                   color_discrete_sequence=["skyblue", "lightblue"],
                   title='Hourly Count of Bikeshare Rides').update_layout(xaxis_title='', yaxis_title='Total Rides')
    col1.plotly_chart(fig1, use_container_width=True)
elif selected_view == "Daily":  
    fig2 = px.bar(weekday_users,
                   x='day',
                   y=['total'],
                   color='user_status',
                   barmode='group',
                   color_discrete_sequence=["skyblue", "lightblue"],
                   title='Daily Count of Bikeshare Rides').update_layout(xaxis_title='', yaxis_title='Total Rides')
    col1.plotly_chart(fig2, use_container_width=True)
elif selected_view == "Monthly":
    fig3 = px.line(monthly_users,
                   x='yearmonth',
                   y=['casual_customers', 'registered_customers', 'total'],
                   color_discrete_sequence=["skyblue", "lightblue", "steelblue"],
                   title="Monthly Count of Bikeshare Rides").update_layout(xaxis_title='', yaxis_title='Total Rides')
    col1.plotly_chart(fig3, use_container_width=True)
elif selected_view == "Seasonal":
    fig4 = px.bar(seasonly_users,
                   x='season',
                   y=['total'],
                   color='user_status',
                   color_discrete_sequence=["skyblue", "lightblue", "steelblue"],
                   title='Seasonly Count of Bikeshare Rides').update_layout(xaxis_title='', yaxis_title='Total Rides')
    col1.plotly_chart(fig4, use_container_width=True)
    
st.markdown("---")

# Chart
col1 = st
fig1 = px.line(hourly_users,
               x='hour',
               y=['casual_customers', 'registered_customers'],
               color_discrete_sequence=["skyblue", "lightblue", "steelblue"],
               title='Count of Bikeshare Rides by Hour').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(weekday_users,
               x='day',
               y=['total'],
               color='user_status',
               barmode='group',
               color_discrete_sequence=["skyblue", "lightblue", "steelblue"],
               title='Count of Bikeshare Rides by Day').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig2, use_container_width=True)

fig3 = px.line(monthly_users,
               x='yearmonth',
               y=['casual_customers', 'registered_customers', 'total'],
               color_discrete_sequence=["skyblue", "lightblue", "steelblue"],
               title="Count of Bikeshare Rides by months").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig3, use_container_width=True)

fig4 = px.bar(seasonly_users,
               x='season',
               y=['total'],
               color='user_status',
               color_discrete_sequence=["skyblue", "lightblue", "steelblue"],
               title='Count of Bikeshare Rides by Season').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig4, use_container_width=True)

st.caption('Copyright (c), Laurivasya Gadhing Syahafidh')
