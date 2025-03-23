import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
  return pd.read_csv("https://github.com/dataprofessor/population-dashboard/raw/master/data/us-population-2010-2019-reshaped.csv", index_col=0)


st.header("1. Inspect the data 🔍")
st.write("`st.data_editor` allows us to display AND edit data")

df = load_data()
st.data_editor(df)