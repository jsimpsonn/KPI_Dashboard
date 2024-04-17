import streamlit as st
import pandas as pd
import plotly.express as px

# App Layout
st.set_page_config(
    page_title="KPI | Downtime",
    page_icon="assets/MSP_Favicon.png",
)

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
@st.cache_data
def convert_df(df_stamco_downtime):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df_stamco_downtime.to_csv().encode('utf-8')

csv = convert_df(df_stamco_downtime)

st.download_button(
    label="Download stamco downtime data",
    data=csv,
    file_name='Stamco_Downtime.csv',
    mime='text/csv',
)
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

st.plotly_chart(braner_downtime)
@st.cache_data
def convert_df(df_braner_downtime):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df_braner_downtime.to_csv().encode('utf-8')

csv = convert_df(df_braner_downtime)

st.download_button(
    label="Download braner downtime data",
    data=csv,
    file_name='Braner_Downtime.csv',
    mime='text/csv',
)
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

st.plotly_chart(redbud_downtime)
@st.cache_data
def convert_df(df_redbud_downtime):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df_redbud_downtime.to_csv().encode('utf-8')

csv = convert_df(df_redbud_downtime)

st.download_button(
    label="Download redbud downtime data",
    data=csv,
    file_name='Redbud_Downtime.csv',
    mime='text/csv',
)