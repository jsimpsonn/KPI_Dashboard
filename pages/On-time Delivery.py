import streamlit as st
import pandas as pd
import plotly.express as px

# App Layout
st.set_page_config(
    page_title="KPI | OTD",
    page_icon="assets/MSP_Favicon.png",
)

df_OTD = pd.read_csv("data/wo.csv")

otd = px.line(df_OTD, x="Month", y="Percentage")

st.header("Work Order On-time Delivery")
st.plotly_chart(otd)