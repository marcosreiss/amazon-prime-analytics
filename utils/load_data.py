from pathlib import Path
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df_path = Path("data/amazon_prep_with_release_year.csv")
    df = pd.read_csv(df_path)
    df['duration_minutes'] = pd.to_numeric(df.get('duration_minutes'), errors='coerce')
    return df
