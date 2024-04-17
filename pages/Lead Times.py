import streamlit as st
import pandas as pd
import plotly.express as px

# App Layout
st.set_page_config(
    page_title="KPI Dashboard • Lead Times",
    page_icon="assets/MSP_Favicon.png",
)

# Read the shipping data
df_lead_times = pd.read_csv("data/LT.csv")

# Convert the 'Date' column to datetime if it's not already
df_lead_times['Date'] = pd.to_datetime(df_lead_times['Date'], format='%m/%d/%Y')

# Sort the DataFrame by the 'Date' column in ascending order
df_lead_times_sorted = df_lead_times.sort_values(by='Date')

# Create the plot
LT = px.line(df_lead_times_sorted, x="Date", y=["Stamco", "Braner", "Red Bud"], title="Lead Times")

# Update x-axis label
LT.update_yaxes(title_text="Days")

# Display the plot
st.plotly_chart(LT)

@st.cache_data
def convert_df(df_lead_times):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df_lead_times.to_csv().encode('utf-8')

csv = convert_df(df_lead_times)

st.download_button(
    label="Download lead times data",
    data=csv,
    file_name='Lead Times.csv',
    mime='text/csv',
)