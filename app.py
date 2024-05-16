import streamlit as st
import pandas as pd


df = pd.read_csv("Data/clean_finished.csv")

st.dataframe(df)