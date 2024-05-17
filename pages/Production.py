# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from sharepoint_manager import authenticate_user
import streamlit_shadcn_ui as ui
from supabase import create_client, Client

# Cached connection to Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
    key = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

# Function to fetch data from Supabase
def fetch_data(table_name):
    response = supabase.table(table_name).select("*").execute()
    return pd.DataFrame(response.data)

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
    st.title("Production")

    # Fetch data from Supabase tables
    df_lifetime = fetch_data("Lifetime Production")
    df_stamco_tonnage = fetch_data("Stamco Production")
    df_braner_tonnage = fetch_data("Braner Production")
    df_redbud_tonnage = fetch_data("Red Bud Production")

    # Unique years for dropdown options based on lifetime data
    unique_years_lifetime = pd.to_datetime(df_lifetime["Month"]).dt.year.unique()
    all_years_lifetime = ["All"] + [str(year) for year in unique_years_lifetime]

    # Unique years for dropdown options based on Stamco data
    unique_years_stamco = pd.to_datetime(df_stamco_tonnage["Month"]).dt.year.unique()
    all_years_stamco = ["All"] + [str(year) for year in unique_years_stamco]

    # Unique years for dropdown options based on Braner data
    unique_years_braner = pd.to_datetime(df_braner_tonnage["Month"]).dt.year.unique()
    all_years_braner = ["All"] + [str(year) for year in unique_years_braner]

    # Unique years for dropdown options based on Redbud data
    unique_years_redbud = pd.to_datetime(df_redbud_tonnage["Month"]).dt.year.unique()
    all_years_redbud = ["All"] + [str(year) for year in unique_years_redbud]

    # Dropdown for selecting year for lifetime production
    selected_year_lifetime = st.selectbox("Select year for Lifetime Tonnage", all_years_lifetime)

    # Filter lifetime data based on selected year
    if selected_year_lifetime == "All":
        filtered_lifetime = df_lifetime
    else:
        filtered_lifetime = df_lifetime[df_lifetime["Month"].str.contains(selected_year_lifetime)]

    # Lifetime Production Chart
    lifetime_production = px.line(filtered_lifetime, x="Month", y="Tons", title="Lifetime Tonnage")
    lifetime_production.update_layout(yaxis_title="Tons", xaxis=dict(dtick="6"), xaxis_tickangle=45)
    st.plotly_chart(lifetime_production)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    # Dropdown for selecting year for Stamco production
    selected_year_stamco = st.selectbox("Select year for Stamco Production", all_years_stamco)

    # Filter Stamco data based on selected year
    if selected_year_stamco == "All":
        filtered_stamco = df_stamco_tonnage
    else:
        filtered_stamco = df_stamco_tonnage[df_stamco_tonnage["Month"].str.contains(selected_year_stamco)]

    # Stamco Production Chart
    stamco_production = px.line(filtered_stamco, x="Month", y=["1st", "2nd", "3rd"], title="Stamco Production")
    stamco_production.update_layout(yaxis_title="TPH", xaxis=dict(dtick="3"), xaxis_tickangle=45)

    # Render Stamco production chart
    st.plotly_chart(stamco_production)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    # Dropdown for selecting year for Braner production
    selected_year_braner = st.selectbox("Select year for Braner Production", all_years_braner)

    # Filter Braner data based on selected year
    if selected_year_braner == "All":
        filtered_braner = df_braner_tonnage
    else:
        filtered_braner = df_braner_tonnage[df_braner_tonnage["Month"].str.contains(selected_year_braner)]

    # Braner Production Chart
    braner_production = px.line(filtered_braner, x="Month", y=["1st", "2nd"], title="Braner Production")
    braner_production.update_layout(yaxis_title="TPH", xaxis=dict(dtick="3"), xaxis_tickangle=45)

    # Render Braner production chart
    st.plotly_chart(braner_production)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    # Dropdown for selecting year for Redbud production
    selected_year_redbud = st.selectbox("Select year for Redbud Production", all_years_redbud)

    # Filter Redbud data based on selected year
    if selected_year_redbud == "All":
        filtered_redbud = df_redbud_tonnage
    else:
        filtered_redbud = df_redbud_tonnage[df_redbud_tonnage["Month"].str.contains(selected_year_redbud)]

    # Redbud Production Chart
    redbud_production = px.line(filtered_redbud, x="Month", y=["1st", "2nd", "3rd"], title="Redbud Production")
    redbud_production.update_layout(yaxis_title="TPH", xaxis=dict(dtick="3"), xaxis_tickangle=45)

    # Render Redbud production chart
    st.plotly_chart(redbud_production)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
