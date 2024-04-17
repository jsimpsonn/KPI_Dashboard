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
st.plotly_chart(shipping)

@st.cache_data
def convert_df(df_shipping):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df_shipping.to_csv().encode('utf-8')

csv = convert_df(df_shipping)

st.download_button(
    label="Download loading times data",
    data=csv,
    file_name='Shipping.csv',
    mime='text/csv',
)