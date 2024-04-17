import streamlit as st
import pandas as pd
import plotly.express as px

# App Layout
st.set_page_config(
    page_title="KPI | Shipping",
    page_icon="assets/MSP_Favicon.png",
)

# Read the shipping data
df_shipping = pd.read_csv("data/shipping.csv")

# Convert the 'Date' column to datetime if it's not already
df_shipping['Date'] = pd.to_datetime(df_shipping['Date'], format='%m/%d/%Y')

# Sort the DataFrame by the 'Date' column in ascending order
df_shipping_sorted = df_shipping.sort_values(by='Date')

# Create the plot
shipping = px.line(df_shipping_sorted, x="Date", y="Percent", title="Shipping - % of Trucks Loaded in One Hour or Less")

# Display the plot
st.header("Shipping")
st.plotly_chart(shipping)