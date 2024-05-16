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


st.dataframe(df, use_container_width=True)
