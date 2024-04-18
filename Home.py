import streamlit as st
import pandas as pd
import plotly.express as px

# App Layout
st.set_page_config(
    page_title="MSP KPI Dashboard",
    page_icon="assets/MSP_Favicon.png",
)

st.subheader('KPI Dashboard 📈')
st.header('Mississippi Steel Processing',divider='blue')

st.markdown(
    """
            The KPI Dashboard provides a comprehensive overview of critical performance metrics across different departments or areas of MSP. It serves as a centralized platform for monitoring key performance indicators, allowing employees and stakeholders to assess the health and progress of various operations
    """
    )

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.caption("Values in this dashboard are managed through a combination of CSV files and SharePoint data. While some data is still sourced from CSV files, efforts are underway to migrate all data retrieval to SharePoint. Please note that the information provided here may not be real-time. However, any updates made to the SharePoint data will be reflected in the dashboard.")

st.sidebar.success("Select a KPI above.")