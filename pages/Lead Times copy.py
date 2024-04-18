import streamlit as st
import pandas as pd
import plotly.express as px
import toml

# Read SharePoint credentials from secrets.toml
def read_secrets():
    with open("secrets.toml", "r") as f:
        secrets = toml.load(f)
    return secrets["sharepoint"]




# Read SharePoint credentials
sharepoint_secrets = read_secrets()
client_id = sharepoint_secrets["client_id"]
client_secret = sharepoint_secrets["client_secret"]
subsite_url = sharepoint_secrets["customer_satisfaction_subsite_url"]
list_name = sharepoint_secrets["list_name"]

# App Layout
st.set_page_config(
    page_title="KPI | Lead Times",
    page_icon="assets/MSP_Favicon.png",
)

st.header("Lead Times")

# Read the shipping data
df_lead_times = pd.read_csv("data/LT.csv")

# Convert the 'Date' column to datetime if it's not already
df_lead_times['Date'] = pd.to_datetime(df_lead_times['Date'], format='%m/%d/%Y')

# Sort the DataFrame by the 'Date' column in ascending order
df_lead_times_sorted = df_lead_times.sort_values(by='Date')

# Create the plot
LT = px.line(df_lead_times_sorted, x="Date", y=["Stamco", "Braner", "Red Bud"])

# Update x-axis label
LT.update_yaxes(title_text="Days")

# Display the plot
st.plotly_chart(LT)