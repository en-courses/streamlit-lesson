import altair as alt 
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
  return pd.read_csv("https://github.com/dataprofessor/population-dashboard/raw/master/data/us-population-2010-2019-reshaped.csv", index_col=0)

df = load_data()

st.header("5. Sprinkle in more interactivity 🪄")

st.write("Use `st.multiselect` and `st.slider` for data filter before chart creation")

states = st.multiselect("Pick your states",
                        list(df.states.unique())[::-1],
                        "California")
date_range = st.slider("Pick your date range",
                       2010, 2019,
                       (2010, 2019))

if states:
    chart_data = df[df['states'].isin(states)]
    chart_data = chart_data[chart_data['year'].between(date_range[0], date_range[1])]
    chart_data['year'] = chart_data['year'].astype(str)

    c = (
        alt.Chart(chart_data)
         .mark_line()
         .encode(x=alt.X('year'),
                 y=alt.Y('population'),
                 color='states')
    )

    st.altair_chart(c, use_container_width=True)