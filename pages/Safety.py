import streamlit as st
import pandas as pd

st.set_page_config(page_title="KPI | Safety",page_icon="assets/MSP_Favicon.png", layout="wide", initial_sidebar_state="auto", menu_items=None)

# Read the CSV file
df_safety = pd.read_csv("data/safety.csv")

st.header("Safety")
st.dataframe(df_safety,use_container_width=True)

# Convert 'Date' column to datetime
df_safety['Date'] = pd.to_datetime(df_safety['Date'])
# Extract year from the 'Date' column and convert to integer
df_safety['Year'] = df_safety['Date'].dt.year.astype(int)
# Convert "Year" column to integers, remove decimals, and then to string
df_safety["Year"] = df_safety["Year"].astype(int).astype(str)
# Remove commas from the "Year" column
df_safety["Year"] = df_safety["Year"].str.replace(",", "")
# Group by year and count occurrences
df_grouped = df_safety.groupby('Year').size().reset_index(name='Total Incidents')
# Display the grouped DataFrame
st.dataframe(df_grouped.set_index('Year'), use_container_width=False)