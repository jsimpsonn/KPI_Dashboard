import streamlit as st
import pandas as pd
import plotly.express as px

# App Layout
st.set_page_config(
    page_title="KPI Dashboard • OTD",
        page_icon="assets/MSP_Favicon.png",
)


df_OTD = pd.read_csv("data/OTD/wo.csv")

otd = px.line(df_OTD, x="Month", y="Percentage", title="Work Order OTD")

st.plotly_chart(otd)

@st.cache_data
def convert_df(df_OTD):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df_OTD.to_csv().encode('utf-8')

csv = convert_df(df_OTD)

st.download_button(
    label="Download OTD data",
    data=csv,
    file_name='OTD.csv',
    mime='text/csv',
)