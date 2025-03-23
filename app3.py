import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
  return pd.read_csv("https://github.com/dataprofessor/population-dashboard/raw/master/data/us-population-2010-2019-reshaped.csv", index_col=0)

df = load_data()

st.header("3. Now make it interactive 🪄")
st.write("It's your turn to select a year")

# Using st.selectbox
selected_year = st.selectbox("Select a year",
                             list(df.year.unique())[::-1])

# Using st.slider
#selected_year = st.slider("Select a year", 2010, 2019)

# Using st.number_input
#selected_year = st.number_input("Enter a year",
 #                               placeholder="Enter a year from 2010-2019",
 #                               value=2019)

if selected_year:
    df_selected_year = df[df.year == selected_year]

    # Display chart
    st.bar_chart(df_selected_year,
                 x='states',
                 y='population')