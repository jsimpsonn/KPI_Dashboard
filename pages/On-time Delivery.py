from sharepoint_manager import get_sharepoint_list_items, sharepoint_urls, sharepoint_lists
from sharepoint_manager import read_secrets, authenticate_user
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui

# App Layout
st.set_page_config(
    page_title="KPI • OTD",
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
    st.title("Work Order On-time Delivery")
    st.subheader("Summary")

    # Get SharePoint URLs and Lists
    url = sharepoint_urls["Customer Satisfaction"]
    list_name = sharepoint_lists["Work Order On-time Delivery"]

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
                "Percent": item.properties.get("Percent") * 100  # Convert decimal to percentage
            }
            data.append(item_data)

    # Convert to DataFrame
    df_OTD = pd.DataFrame(data)

    # Convert 'Date' column to datetime for sorting
    df_OTD['Date'] = pd.to_datetime(df_OTD['Date'])

    # Format 'Date' column to display as "January 2023"
    df_OTD['Date'] = df_OTD['Date'].dt.strftime("%B %Y")

    # Format 'Percent' column to display as percentage with two decimal places
    df_OTD['Percent'] = df_OTD['Percent'].map("{:.2f}%".format)

    # Set 'Date' column as index and remove it from columns
    df = df_OTD.set_index('Date', drop=True)

    otd = px.line(df_OTD, x="Date", y="Percent")
    otd.add_hrect(y0=77,y1=100, fillcolor="green", opacity=0.1, annotation_text="Goal = 77%", annotation_position="top left", annotation_font_color='black', annotation_font_size=14)
    otd.add_hrect(y0=70,y1=77, fillcolor="red", opacity=0.1)
    st.plotly_chart(otd)

    st.subheader("Data")

    tabAll, tab2023, tab2024 = st.tabs(["All", "2023", "2024"])
    df_2023 = df[df.index.str.contains("2023")]
    df_2024 = df[df.index.str.contains("2024")]

    with tabAll:
        st.dataframe(df, use_container_width=True)
    with tab2023:
        st.dataframe(df_2023, use_container_width=True)
    with tab2024:
        st.dataframe(df_2024, use_container_width=True)