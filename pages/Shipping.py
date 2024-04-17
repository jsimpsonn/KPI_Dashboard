import streamlit as st
import pandas as pd
import plotly.express as px

# App Layout
st.set_page_config(
    page_title="KPI | Shipping",
    page_icon="assets/MSP_Favicon.png",
)

st.title("Shipping")
st.subheader("Summary")

# Read the shipping data
df_shipping = pd.read_csv("data/shipping.csv")

# Convert the 'Date' column to datetime if it's not already
df_shipping['Date'] = pd.to_datetime(df_shipping['Date'], format='%m/%d/%Y')

# Sort the DataFrame by the 'Date' column in ascending order
df_shipping_sorted = df_shipping.sort_values(by='Date')

# Create the plot
shipping = px.line(df_shipping_sorted, x="Date", y="Percent")

# Display the plot
st.plotly_chart(shipping)

st.subheader("Data")

tabAll, tab2021, tab2022, tab2023, tab2024 =st.tabs(["All", "2021", "2022", "2023", "2024"])

df_2021 = df_shipping[df_shipping["Date"].dt.year == 2021]
df_2022 = df_shipping[df_shipping["Date"].dt.year == 2022]
df_2023 = df_shipping[df_shipping["Date"].dt.year == 2023]
df_2024 = df_shipping[df_shipping["Date"].dt.year == 2024]

with tabAll:
    st.dataframe(df_shipping,use_container_width=True)
with tab2021:
    st.dataframe(df_2021,use_container_width=True)
with tab2022:
    st.dataframe(df_2022,use_container_width=True)
with tab2023:
    st.dataframe(df_2023,use_container_width=True)
with tab2024:
    st.dataframe(df_2024,use_container_width=True)