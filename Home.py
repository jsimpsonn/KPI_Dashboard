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
st.caption("Values in this dashboard are managaged through SharePoint data and do not currently offer realtime information. However, if SharePoint values are updated, the dashboard will reflect those changes.")

st.sidebar.success("Select a KPI above.")