import streamlit as st
import pandas as pd


@st.cache_data
def load_players():

    return pd.read_csv("data/player_data.csv")


@st.cache_data
def load_scenarios():

    return pd.read_csv("data/scenario_choices.csv")
