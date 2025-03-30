import streamlit as st
import sqlite3
from openai import AzureOpenAI
import pandas as pd
import altair as alt

# Function to initialize the database
def init_db():
    conn = sqlite3.connect("seder_guests.db")
    cursor = conn.cursor()
    
    # Create guests table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dish TEXT NOT NULL,
        dish_type TEXT NOT NULL
    )
    """)
    conn.commit()
    return conn, cursor

# Function to add a guest
def add_guest(conn, cursor, name, dish, dish_type):
    cursor.execute("INSERT INTO guests (name, dish, dish_type) VALUES (?, ?, ?)", (name, dish, dish_type))
    conn.commit()

# Function to fetch all guests
def get_guests(cursor):
    cursor.execute("SELECT id, name, dish, dish_type FROM guests")
    return cursor.fetchall()

# Function to display dish type distribution as a pie chart
def display_pie_chart(cursor):
    cursor.execute("SELECT dish_type, COUNT(*) as count FROM guests GROUP BY dish_type")
    dish_counts = cursor.fetchall()
    
    # Prepare the data for Altair chart
    dish_data = pd.DataFrame(dish_counts, columns=["dish_type", "count"])
    
    st.write("##### Current Dish Distribution")
    
    # Create Altair pie chart
    pie_chart = (
        alt.Chart(dish_data)
        .mark_arc()
        .encode(
            theta="count:Q",
            color="dish_type:N",
            tooltip=["dish_type:N", "count:Q"]
        )
        .properties(height=300)
    )
    
    # Display the pie chart
    st.altair_chart(pie_chart, use_container_width=True)


# Function to update a guest's dish
def update_guest_dish(conn, cursor, guest_id, new_dish, new_dish_type):
    cursor.execute("UPDATE guests SET dish = ?, dish_type = ? WHERE id = ?", (new_dish, new_dish_type, guest_id))
    conn.commit()

# Function to remove a guest
def remove_guest(conn, cursor, guest_id):
    cursor.execute("DELETE FROM guests WHERE id = ?", (guest_id,))
    conn.commit()

# Function to display most popular dish category
def most_popular_dish_category(cursor):
    cursor.execute("SELECT dish_type, COUNT(*) FROM guests GROUP BY dish_type ORDER BY COUNT(*) DESC LIMIT 1")
    popular_category = cursor.fetchone()
    
    if popular_category:
        st.write(f"The most popular dish category is: **{popular_category[0]}** with {popular_category[1]} dishes!")
    else:
        st.write("No guests yet, so no category is popular!")

# Chatbot Function
def ask_chatbot(client, question):
    """Ask OpenAI GPT for a dish recommendation."""
    stream = client.chat.completions.create(
        model="gpt-35-turbo-16k",
        messages=[{"role": "system", "content": "You are a friendly chatbot helping guests pick a Passover Seder dish."},
                  {"role": "user", "content": question}],
        temperature=0.7,
        stream=True
    )
    # Stream the response to the app using `st.write_stream`.
    st.write_stream(stream)

# Streamlit UI

# Initialize the database connection
conn, cursor = init_db()


st.set_page_config(layout="wide")
# Set page title
st.title("🍷 Passover Seder Guest List & Chatbot 🕎")
st.write("Track who's coming and what they're bringing!")

## Sidebar for OpenAI API Key
st.sidebar.header('Settings')
openai_api_key = st.sidebar.text_input('OpenAI API Key')
openai_api_endpoint = st.sidebar.text_input('OpenAI API Endpoint')

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    #client = OpenAI(api_key=openai_api_key)
    client = AzureOpenAI(
        api_key=openai_api_key,  
        api_version="2024-02-15-preview",
        azure_endpoint = openai_api_endpoint
    )


# Input Form for Adding Guests
with st.form("guest_form"):
    name = st.text_input("Guest Name")
    dish = st.text_input("Dish They Are Bringing")
    dish_type = st.selectbox("Type of Dish", ["Appetizer", "Main Course", "Salad", "Soup", "Dessert"])
    submit_button = st.form_submit_button("Add Guest")

    if submit_button and name and dish:
        add_guest(conn, cursor, name, dish, dish_type)
        st.success(f"{name} added to the guest list with {dish} ({dish_type})!")

# Display Guest List Using st.data_grid
st.header("Guest List")
guests = get_guests(cursor)

if guests:
    # Convert guests data to a pandas DataFrame
    guest_df = pd.DataFrame(guests, columns=["ID", "Name", "Dish", "Dish Type"])
    
    # Display the DataFrame using st.data_grid
    st.data_editor(guest_df, 
                   use_container_width=True,
                   column_config={
                        "Dish Type": st.column_config.SelectboxColumn("Dish Type", options=["Appetizer", "Main Course", "Salad", "Soup", "Dessert"], required=True),
                     })
else:
    st.write("No guests yet! Someone has to bring the brisket! 🍖")

# Display Most Popular Dish Category
st.header("🥇 Most Popular Dish Category")
most_popular_dish_category(cursor)

# Display Who’s Bringing What (Pie Chart)
st.header("🍽️ Who’s Bringing What?")
display_pie_chart(cursor)

# Chatbot Section
st.header("🤖 Chat with the Passover Chatbot!")
user_input = st.text_input("Ask the chatbot for a dish suggestion:")

if st.button("Get Suggestion") and user_input:
    st.write(f"💬 Chatbot:")
    response = ask_chatbot(client, user_input)
    

# Update or Remove Guest
st.header("📝 Update or Remove a Guest's Dish")
guest_names = [guest[1] for guest in get_guests(cursor)]

guest_to_edit = st.selectbox("Select a guest to update their dish", guest_names)
if guest_to_edit:
    new_dish = st.text_input(f"New dish for {guest_to_edit}")
    new_dish_type = st.selectbox("New type of dish", ["Appetizer", "Main Course", "Salad", "Soup", "Dessert"])
    guest_id = [guest[0] for guest in get_guests(cursor) if guest[1] == guest_to_edit][0]
    
    if st.button("Update Dish"):
        update_guest_dish(conn, cursor, guest_id, new_dish, new_dish_type)
        st.success(f"{guest_to_edit}'s dish has been updated!")

    # Option to remove guest
    if st.button(f"Remove {guest_to_edit} from the list"):
        remove_guest(conn, cursor, guest_id)
        st.success(f"{guest_to_edit} has been removed from the list.")

