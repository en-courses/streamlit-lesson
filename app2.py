import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
  return pd.read_csv("https://github.com/dataprofessor/population-dashboard/raw/master/data/us-population-2010-2019-reshaped.csv", index_col=0)

df = load_data()

st.header("2. Get started with a simple bar chart 📊")

st.write("Let's chart the US state population data from the year 2019")

st.bar_chart(df[['year', 'states', 'population']],
             x='states',
             y='population')