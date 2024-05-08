import streamlit as st
import pandas as pd
import plotly.express as px
from sharepoint_manager import authenticate_user
import streamlit_shadcn_ui as ui
from st_pages import show_pages_from_config, hide_pages

st.set_page_config(page_title="KPI • Safety", page_icon="assets/MSP_Favicon.png", layout="wide", initial_sidebar_state="auto", menu_items=None)
show_pages_from_config()
hide_pages("Print Summary")
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
    # Read the CSV file
    df_safety = pd.read_csv("data/safety.csv")

    st.title("Safety")
    st.caption(":blue[Recordable (OSHA Recordable) refers to workplace injuries, illnesses, or incidents that meet specific criteria set forth by the Occupational Safety and Health Administration (OSHA) for recording and reporting purposes. OSHA requires employers to maintain records of work-related injuries and illnesses through the OSHA Form 300 Log of Work-Related Injuries and Illnesses.]")
    st.subheader("Summary")
    # Convert 'Date' column to datetime and sort by this date in descending order
    df_safety['Date'] = pd.to_datetime(df_safety['Date'])
    df_safety.sort_values('Date', ascending=False, inplace=True)

    # The most recent incident is now the first row after sorting
    most_recent_incident = df_safety.iloc[0]

    # Create a string with the relevant information from the most recent incident row
    incident_warning = f"Most recent safety incident: {most_recent_incident['Date'].strftime('%m/%d/%Y')} - {most_recent_incident['Description']}"

    # Display the warning
    st.warning(incident_warning)
    st.write("")
    st.write("")
    st.write("")

    col1, col2 = st.columns([3, 7])

    # Convert 'Date' column to datetime
    df_safety['Date'] = pd.to_datetime(df_safety['Date'])

    # Format 'Date' column as "mm/dd/yyyy"
    df_safety['Date'] = df_safety['Date'].dt.strftime('%m/%d/%Y')

    df_safety['Year'] = df_safety['Date'].str[-4:]
    df_grouped_recordable = df_safety[df_safety['Recordable'] == 'Y'].groupby('Year').size().reset_index(name='Recordables')
    df_grouped_total = df_safety.groupby('Year').size().reset_index(name='Total Incidents')
    df_combined = df_grouped_total.merge(df_grouped_recordable, how='left', on='Year').fillna(0)

    with col1:
        st.dataframe(df_combined.set_index('Year'), use_container_width=False)
    with col2:
        fig = px.line(df_combined, x='Year', y='Total Incidents')
        fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=300
    )
        fig.update_yaxes(range=[0, df_combined['Total Incidents'].max()])  # Set x-axis range from 0 to the maximum value
        st.plotly_chart(fig,config={'displayModeBar': False})

    st.subheader("Data")

    tabAll, tab2019, tab2020, tab2021, tab2022, tab2023, tab2024 = st.tabs(["All", "2019", "2020", "2021", "2022", "2023", "2024"])
    df_2019 = df_safety[df_safety["Date"].str.endswith("2019")]
    df_2020 = df_safety[df_safety["Date"].str.endswith("2020")]
    df_2021 = df_safety[df_safety["Date"].str.endswith("2021")]
    df_2022 = df_safety[df_safety["Date"].str.endswith("2022")]
    df_2023 = df_safety[df_safety["Date"].str.endswith("2023")]
    df_2024 = df_safety[df_safety["Date"].str.endswith("2024")]

    with tabAll:
        st.dataframe(df_safety, use_container_width=True)
    with tab2019:
        st.dataframe(df_2019, use_container_width=True)
    with tab2020:
        st.dataframe(df_2020, use_container_width=True)
    with tab2021:
        st.dataframe(df_2021, use_container_width=True)
    with tab2022:
        st.dataframe(df_2022, use_container_width=True)
    with tab2023:
        st.dataframe(df_2023, use_container_width=True)
    with tab2024:
        st.dataframe(df_2024, use_container_width=True)