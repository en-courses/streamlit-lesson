import datetime
import random
import sqlite3

import altair as alt
import pandas as pd
import streamlit as st

@st.cache_resource
# Database setup
def init_db():
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    issue TEXT,
                    status TEXT,
                    priority TEXT,
                    date_submitted TEXT)''')
    conn.commit()
    conn.close()


# Populate database with fake tickets
def populate_db():
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    random.seed(42)
    c.execute("SELECT COUNT(*) FROM tickets")
    if c.fetchone()[0] == 0:  # Only populate if the table is empty
        issue_descriptions = [
            "Network connectivity issues in the office",
            "Software application crashing on startup",
            "Printer not responding to print commands",
            "Email server downtime",
            "Data backup failure",
            "Login authentication problems",
            "Website performance degradation",
            "Security vulnerability identified",
            "Hardware malfunction in the server room",
            "Employee unable to access shared files",
            "Database connection failure",
            "Mobile application not syncing data",
            "VoIP phone system issues",
            "VPN connection problems for remote employees",
            "System updates causing compatibility issues",
            "File server running out of storage space",
            "Intrusion detection system alerts",
            "Inventory management system errors",
            "Customer data not loading in CRM",
            "Collaboration tool not sending notifications",
        ]
        
        for _ in range(100):
            issue = random.choice(issue_descriptions)
            status = random.choice(["Open", "In Progress", "Closed"])
            priority = random.choice(["High", "Medium", "Low"])
            date_submitted = datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            c.execute("INSERT INTO tickets (issue, status, priority, date_submitted) VALUES (?, ?, ?, ?)",
                      (issue, status, priority, date_submitted.isoformat()))
    conn.commit()
    conn.close()

# Insert a new ticket
def insert_ticket(issue, priority):
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("INSERT INTO tickets (issue, status, priority, date_submitted) VALUES (?, 'Open', ?, ?)",
              (issue, priority, datetime.date.today().isoformat()))
    conn.commit()
    conn.close()

# Fetch tickets
def fetch_tickets():
    conn = sqlite3.connect("tickets.db")
    df = pd.read_sql("SELECT * FROM tickets", conn)
    conn.close()
    return df

# Update ticket status or priority
def update_ticket(ticket_id, status, priority):
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("UPDATE tickets SET status = ?, priority = ? WHERE id = ?", (status, priority, ticket_id))
    conn.commit()
    conn.close()



st.set_page_config(page_title="Support Tickets", page_icon="🎫",layout="wide")
st.title("🎫 Support Tickets")

# Initialize database
init_db()
populate_db()

# Sidebar
st.sidebar.header('Settings')
oai_key = st.sidebar.text_input('OpenAI Key')
oai_endpoint = st.sidebar.text_input('OpenAI Endpoint')


# Add a new ticket
st.header("Add a Ticket")
with st.form("add_ticket_form"):
    issue = st.text_area("Describe the issue")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Submit")

if submitted and issue:
    insert_ticket(issue, priority)
    st.success("Ticket submitted!")

# Fetch and display tickets
df = fetch_tickets()

st.header("Existing Tickets")
st.write(f"Number of tickets: `{len(df)}`")
st.info("You can edit ticket status and priority directly in the table.")

# Allow user to edit status and priority
edited_df = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "status": st.column_config.SelectboxColumn("Status", options=["Open", "In Progress", "Closed"], required=True),
        "priority": st.column_config.SelectboxColumn("Priority", options=["High", "Medium", "Low"], required=True),
    },
    disabled=["id", "issue", "date_submitted"],
)

# Update database with edited values
for _, row in edited_df.iterrows():
    update_ticket(row["id"], row["status"], row["priority"])

# Display statistics
st.header("Statistics")
col1, col2, col3 = st.columns(3)
num_open_tickets = len(df[df.status == "Open"])
col1.metric(label="Number of open tickets", value=num_open_tickets)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Charts
st.write("##### Ticket Status Per Month")
df["date_submitted"] = pd.to_datetime(df["date_submitted"])
status_plot = (
    alt.Chart(df)
    .mark_bar()
    .encode(x="month(date_submitted):O", y="count():Q", xOffset="status:N", color="status:N")
    .configure_legend(orient="bottom")
)
st.altair_chart(status_plot, use_container_width=True)

st.write("##### Current Ticket Priorities")
priority_plot = (
    alt.Chart(df)
    .mark_arc()
    .encode(theta="count():Q", color="priority:N")
    .properties(height=300)
)
st.altair_chart(priority_plot, use_container_width=True)
