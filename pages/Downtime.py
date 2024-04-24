import streamlit as st
import pandas as pd
import plotly.express as px
from sharepoint_manager import authenticate_user

st.set_page_config(
    page_title="KPI • Downtime",
    page_icon="assets/MSP_Favicon.png",
)

# Check if the user is already authenticated
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    access_token = authenticate_user()
    if access_token:
        st.session_state['authenticated'] = True
        st.session_state['access_token'] = access_token
    else:
        st.error("You must be authenticated to access this dashboard.")
        st.stop()  # Stop the app if not authenticated

if st.session_state['authenticated']:
    # App Layout
    st.set_page_config(
        page_title="KPI • Downtime",
        page_icon="assets/MSP_Favicon.png",
    )

    st.title("Downtime")

    df_stamco_downtime = pd.read_csv("data/downtime/stamco.csv")
    df_braner_downtime = pd.read_csv("data/downtime/braner.csv")
    df_redbud_downtime = pd.read_csv("data/downtime/redbud.csv")

    # Convert "Year" column to integers, remove decimals, and then to string
    df_stamco_downtime["Year"] = df_stamco_downtime["Year"].astype(int).astype(str)

    # Remove commas from the "Year" column
    df_stamco_downtime["Year"] = df_stamco_downtime["Year"].str.replace(",", "")

    # Render charts
    stamco_downtime = px.line(df_stamco_downtime, x="Month", y=["MR", "NMR"], title="Stamco Downtime")
    braner_downtime = px.line(df_braner_downtime, x="Month", y=["MR", "NMR"], title="Braner Downtime")
    redbud_downtime = px.line(df_redbud_downtime, x="Month", y=["MR", "NMR"], title="Redbud Downtime")

    stamco_downtime.update_layout(yaxis_title="Hours",xaxis=dict(dtick="1"),xaxis_tickangle=45)
    braner_downtime.update_layout(yaxis_title="Hours",xaxis=dict(dtick="1"),xaxis_tickangle=45)
    redbud_downtime.update_layout(yaxis_title="Hours",xaxis=dict(dtick="1"),xaxis_tickangle=45)

    st.plotly_chart(stamco_downtime)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.plotly_chart(braner_downtime)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.plotly_chart(redbud_downtime)