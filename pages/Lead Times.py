from sharepoint_manager import get_sharepoint_list_items, sharepoint_urls, sharepoint_lists, read_secrets, authenticate_user
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui

st.set_page_config(
    page_title="KPI • Lead Times",
    page_icon="assets/MSP_Favicon.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
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
    st.title("Lead Times")

    # Get SharePoint URLs and Lists
    url = sharepoint_urls["Customer Satisfaction"]
    list_name = sharepoint_lists["Lead Times"]

    # Get SharePoint secrets
    sharepoint_secrets = read_secrets()
    client_id = sharepoint_secrets["client_id"]
    client_secret = sharepoint_secrets["client_secret"]

    # Access SharePoint list items
    items = get_sharepoint_list_items(url, list_name, client_id, client_secret)

    if items:
        # Extract item properties
        data = []
        for item in items:
            item_data = {
                "Date": item.properties.get("Date"),
                "Braner": item.properties.get("Braner"),
                "Stamco": item.properties.get("Stamco1"),
                "Red Bud": item.properties.get("Red_x0020_Bud")
            }
            data.append(item_data)

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Convert 'Date' column to datetime for sorting
        df['Date'] = pd.to_datetime(df['Date'])

        # Sort DataFrame by 'Date' column from oldest to newest
        df = df.sort_values(by='Date', ascending=True)

        # Change date format to mm/dd/yyyy for display
        df_display = df.copy()
        df_display['Date'] = df_display['Date'].dt.strftime('%m/%d/%Y')

        # Plotly line chart
        fig = px.line(df, x="Date", y=["Stamco", "Braner", "Red Bud"])
        chart_column, metrics_column = st.columns([4, 1])  # Adjust the width ratio as needed
        with chart_column:
            st.plotly_chart(fig, use_container_width=True)

        # Display most recent values for Braner, Stamco, and Red Bud along with change since previous row
        with metrics_column:
            st.subheader("Current")
            latest_values = df.iloc[-1]  # Get the last row which contains the most recent values
            for column in ["Braner", "Stamco", "Red Bud"]:
                value_str = f"{latest_values[column]} days"  # Add "days" after the value
                ui.metric_card(title=f"{column}", content=value_str, description="", key=f"card_{column}")

        st.subheader("Data")

    tabAll, tab2023, tab2024 = st.tabs(["All", "2023", "2024"])
    df_2023 = df_display[df_display["Date"].str.endswith("2023")]
    df_2024 = df_display[df_display["Date"].str.endswith("2024")]

    # Sort DataFrame by 'Date' column from newest to oldest before displaying in tabs
    df_display['Date'] = pd.to_datetime(df_display['Date'])
    df_display = df_display.sort_values(by='Date', ascending=False)

    df_2023['Date'] = pd.to_datetime(df_2023['Date'])
    df_2024['Date'] = pd.to_datetime(df_2024['Date'])

    df_2023 = df_2023.sort_values(by='Date', ascending=False)
    df_2024 = df_2024.sort_values(by='Date', ascending=False)

    # Convert 'Date' column back to 'mm/dd/yyyy' format for display
    df_display['Date'] = df_display['Date'].dt.strftime('%m/%d/%Y')
    df_2023['Date'] = df_2023['Date'].dt.strftime('%m/%d/%Y')
    df_2024['Date'] = df_2024['Date'].dt.strftime('%m/%d/%Y')

    with tabAll:
        st.dataframe(df_display, use_container_width=True)
    with tab2023:
        st.dataframe(df_2023, use_container_width=True)
    with tab2024:
        st.dataframe(df_2024, use_container_width=True)