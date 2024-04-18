from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui
import toml

st.set_page_config(page_title="KPI • Customer Surveys",page_icon="assets/MSP_Favicon.png", layout="wide", initial_sidebar_state="auto", menu_items=None)

# Read the CSV data
df_customer_surveys = pd.read_csv("data/surveys.csv")

# Convert "Year" column to integers, remove decimals, and then to string
df_customer_surveys["Year"] = df_customer_surveys["Year"].astype(int).astype(str)

# Remove commas from the "Year" column
df_customer_surveys["Year"] = df_customer_surveys["Year"].str.replace(",", "")

st.title("Customer Surveys")
st.caption('The form for customers to fill out can be found and shared from [here](https://forms.office.com/r/dvnMP3f8DM)')
st.dataframe(df_customer_surveys, use_container_width=True)

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

average_ratings = df_customer_surveys[["On Time Performance", "Quality of Processing", "Pricing", "Customer Service", "Overall Satisfaction"]].mean()

# Create a DataFrame for the average performance
st.bar_chart(average_ratings,use_container_width=False, width=300)