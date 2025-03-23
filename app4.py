import altair as alt 
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
  return pd.read_csv("https://github.com/dataprofessor/population-dashboard/raw/master/data/us-population-2010-2019-reshaped.csv", index_col=0)

df = load_data()

st.header("4. How about a line chart? 📈")

st.write("Track changes over time")

df_line_chart = df.copy()
df_line_chart['year'] = df_line_chart['year'].astype(str)

c = (
    alt.Chart(df_line_chart)
     .mark_line()
     .encode(x=alt.X('year'),
             y=alt.Y('population'),
             color='states')
)

st.altair_chart(c, use_container_width=True)