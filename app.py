# Imports

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_dynamic_filters import DynamicFilters 
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Setting up page configuration

st.set_page_config(page_title="Streamlit Metrics Demo",
                   page_icon=":brain:",
                   layout='wide')

# Reading df from pathway

df = pd.read_csv("Data/clean_finished.csv")
time_df= pd.read_csv("Data/time_df.csv")

# Introduction and Header

st.header("Customer Onboarding Metrics")

st.text("")

st.write("This project is solely for demonstration purposes, all code and frameworks are available via the repository(**business_insights_analysis**).")

st.write("The analysis and dataframes that are used here are available via the repository, titled **'Exploration.ipynb'** ")

# Filter Sidebar

# Sidebar Inights

with st.sidebar:
    st.header("**Quick Insights**")
    st.markdown(" ●  **70%** of Active Users come from a single country (USA)")
    st.markdown(" ● **30%** of Opportunities won never become active platform users")
    st.markdown(" ● **25%** of Active Accounts have zero platform interaction")
    st.markdown(" ● Average turnover from 'opportunity won' to 'active' status is **7 days** and and varies wildly")

st.divider()
st.sidebar.header("Filter Options")

dynamic_filters = DynamicFilters(df, filters=["Country", "CSM Status Stage", "Highest Product", "# delivery partners"])

df = dynamic_filters.filter_df()

with st.sidebar:
    dynamic_filters.display_filters()

# LogIn Metrics

st.header("LogIn Metrics")

# alignment = 

col00, col0, col1, col2, col3, col4, col5, col6 = st.columns(8)

with col1:
    st.metric("Daily LogIns", 878, f"-75.3% since yesterday")

with col2:
    st.metric("Weekly LogIns", 6504, f"+177.7 vs Previous Week")

with col3:
    st.metric("Monthly LogIns", 12476, f"+455.4 vs Previous Month")

with col4:
    st.metric("Daily Average LogIns", 402.8)


st.divider()
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

# CHURN ANALYTICS

st.divider()
st.header("Churn Graphs")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('### Churn by Region')
    churn_by_region = df[df['CSM Status Stage'] == 'Churned'].groupby(['Region']).count()[
        'Account ID'].reset_index().rename(columns={'Account ID': 'total_users_churned'})
    not_churn_by_region = df.groupby(['Region']).nunique()['Account ID'].reset_index().rename(
        columns={'Account ID': 'total_users'}).iloc[0:4]
    churn_by_region['total_users'] = not_churn_by_region['total_users']

    fig_churn_by_region = make_subplots(specs=[[{"secondary_y": True}]])
    fig_churn_by_region.add_trace(
        go.Bar(x=churn_by_region['Region'], y=churn_by_region['total_users_churned'], name="Churned"),
        secondary_y=False)
    fig_churn_by_region.add_trace(
        go.Scatter(x=churn_by_region['Region'], y=churn_by_region['total_users'], name="Total users", mode="lines"),
        secondary_y=True)
    fig_churn_by_region.update_xaxes(title_text="Region")
    fig_churn_by_region.update_yaxes(title_text="Churn", secondary_y=False)
    fig_churn_by_region.update_yaxes(title_text="Total users", secondary_y=True)
    st.plotly_chart(fig_churn_by_region, use_container_width=True)
with c2:
    st.markdown('### Churn Rate by Product')
    churn_by_product = df[df['CSM Status Stage'] == 'Churned'].groupby(['Highest Product', 'CSM Status Stage']).count()[
        'Account ID'].reset_index()
    fig_churn_by_product = px.bar(churn_by_product, x='Highest Product', y='Account ID')
    st.plotly_chart(fig_churn_by_product, use_container_width=True)
with c3:
    st.markdown('### Churn by Number of Partners')
    churn_by_partners = df[df['CSM Status Stage'] == 'Churned'].groupby(['# delivery partners']).count()[
        'Account ID'].reset_index()
    fig_churn_by_partners = px.bar(churn_by_partners, x='# delivery partners', y='Account ID')
    st.plotly_chart(fig_churn_by_partners, use_container_width=True)

st.divider()