import streamlit as st
import pandas as pd
import plotly.express as px

# App Layout
st.set_page_config(
    page_title="KPI | OTD",
    page_icon="assets/MSP_Favicon.png",
)

st.title("Work Order On-time Delivery")
st.subheader("Summary")

df_OTD = pd.read_csv("data/wo.csv")

# Plot the on-time delivery percentage
otd = px.line(df_OTD, x="Month", y="Percentage")

st.plotly_chart(otd)

st.subheader("Data")

tabAll, tab2023, tab2024 = st.tabs(["All", "2023", "2024"])

df_2023 = df_OTD[df_OTD["Year"] == 2023]
df_2024 = df_OTD[df_OTD["Year"] == 2024]

with tabAll:
    st.dataframe(df_OTD, use_container_width=True)
with tab2023:
    st.dataframe(df_2023.drop(columns=["Year"]), use_container_width=True)
with tab2024:
    st.dataframe(df_2024.drop(columns=["Year"]), use_container_width=True)
