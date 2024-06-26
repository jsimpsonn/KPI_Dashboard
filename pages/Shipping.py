from sharepoint_manager import get_sharepoint_list_items, sharepoint_urls, sharepoint_lists
from sharepoint_manager import read_secrets, authenticate_user
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui

# App Layout
st.set_page_config(
    page_title="KPI • Shipping",
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
    st.title("Shipping")
    st.subheader("Summary")

    # Get SharePoint URLs and Lists
    url = sharepoint_urls["Plant Operations"]
    list_name = sharepoint_lists["Loading Times"]

    # Get SharePoint secrets
    sharepoint_secrets = read_secrets()
    client_id = sharepoint_secrets["client_id"]
    client_secret = sharepoint_secrets["client_secret"]

    # Access SharePoint list items
    items = get_sharepoint_list_items(url, list_name, client_id, client_secret)

    # Function to format decimal to percentage
    def format_percentage(decimal):
        return f"{decimal * 100:.0f}%"

    # Extract item properties
    data = []
    for item in items:
        item_data = {
            "Date": item.properties.get("Date"),
            "Percent": format_percentage(item.properties.get("OData__x0025_")),
            "Goal": format_percentage(item.properties.get("Goal")),
            "No. of Trucks": item.properties.get("Trucks")
        }
        data.append(item_data)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Convert 'Date' column to datetime for sorting
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort DataFrame by 'Date' column from oldest to newest for the chart
    df_chart = df.sort_values(by='Date', ascending=True)

    # Convert 'Date' column to mm/YYYY format for the chart
    df_chart['Date'] = df_chart['Date'].dt.strftime('%B %Y')

    # Plotly line chart
    fig = px.line(df_chart, x="Date", y="Percent", title="Trucks Loaded in One Hour or Less")
    fig.update_layout(xaxis=dict(dtick="3"), xaxis_tickangle=45)
    fig.add_hrect(y0=75,y1=100, fillcolor="green", opacity=0.1, annotation_text="Goal = 75%", annotation_position="top left")
    fig.add_hrect(y0=50,y1=75, fillcolor="red", opacity=0.1)

    st.plotly_chart(fig)

    df = df.sort_values(by='Date', ascending=False)

    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

    with st.expander("Data",expanded=False):
        st.dataframe(df, use_container_width=True)