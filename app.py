# Imports

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_dynamic_filters import DynamicFilters 

# Setting up page configuration

st.set_page_config(page_title="Streamlit Metrics Demo",
                   page_icon=":brain:",
                   layout='wide')

# Reading df from pathway

df = pd.read_csv("Data/clean_finished.csv")
time_df= pd.read_csv("Data/time_df.csv")

# Filter Sidebar

# Sidebar Inights

with st.sidebar:
    st.header("**Quick Inisghts**")
    st.markdown(" ●  **70%** of Active Users come from a single country (USA)")
    st.markdown(" ● **30%** of Opportunities won never become active platform users")
    st.markdown(" ● **25%** of Active Accounts have zero platform interaction")
    st.markdown(" ● Average turnover from 'opportunity won' to 'active' status is **7 days** and varies wildly")

st.sidebar.header("Filter Options")

dynamic_filters = DynamicFilters(df, filters=["Country", "CSM Status Stage", "Highest Product", "# delivery partners"])

with st.sidebar:
    dynamic_filters.display_filters()

# Introduction and Header

st.header("Customer Onboarding Metrics")

st.text("")

st.write("This project is solely for demonstration purposes, all code and frameworks are available via the repository.")

st.write("We have already discovered some valuable insights following the initial exploration.")

st.write("The analysis is available via the repository and titled **'Exploration.ipynb'** ")

st.write("")

# LogIn Metrics

st.header("LogIn Metrics")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Daily LogIns", 878, f"-75.3% since yesterday")

with col2:
    st.metric("Weekly LogIns", 12476, f"+177.7 vs Previous Week")

with col3:
    st.metric("Monthly LogIns", 6504, f"+455.4 vs Previous Month")

with col4:
    st.metric("Daily Average LogIns", 402.8)

# dynamic_filters.display_df()  # st.dataframe(df, use_container_width=True)

# 

st.header("LogIn Graph")

daily_users = df[df['Activation Date'].notna()].groupby('Activation Date')['Account ID'].nunique().reset_index()

fig_growth = px.line(daily_users, x='Activation Date', y='Account ID', title="<b>Daily Active Users</b>")
fig_growth.update_yaxes(rangemode="tozero")
fig_growth.update_layout(
    xaxis=dict(
        range=['2021-08-31', '2022-01-15'],
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=3,
                     label="3m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=False),
        type="date"

    )
)
st.plotly_chart(fig_growth, use_container_width=True)
