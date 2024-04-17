import streamlit as st
import pandas as pd
import numpy as np

# Read the CSV data
df_customer_surveys = pd.read_csv("data/customer surveys.csv")

# Convert "Year" column to integers, remove decimals, and then to string
df_customer_surveys["Year"] = df_customer_surveys["Year"].astype(int).astype(str)

# Remove commas from the "Year" column
df_customer_surveys["Year"] = df_customer_surveys["Year"].str.replace(",", "")

st.header("Customer Surveys")
st.caption('The form for customers to fill out can be found and shared from [here](https://forms.office.com/r/dvnMP3f8DM)')
st.dataframe(df_customer_surveys, use_container_width=True)

@st.cache_data
def convert_df(df_stamco_downtime):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df_stamco_downtime.to_csv().encode('utf-8')

csv = convert_df(df_customer_surveys)

st.download_button(
    label="Download customer surveys data",
    data=csv,
    file_name='Customer_Surveys.csv',
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

average_ratings = df_customer_surveys[["On Time Performance", "Quality of Processing", "Pricing", "Customer Service", "Overall Satisfaction"]].mean()

# Create a DataFrame for the average performance
st.bar_chart(average_ratings)
