from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui
import toml

st.set_page_config(page_title="KPI • Lead Times",page_icon="assets/MSP_Favicon.png", layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title("Lead Times")

# Read SharePoint credentials
sharepoint_secrets = st.secrets["sharepoint"]
client_id = sharepoint_secrets["client_id"]
client_secret = sharepoint_secrets["client_secret"]
subsite_url = sharepoint_secrets["customer_satisfaction_subsite_url"]
list_name = sharepoint_secrets["lead_times_list_name"]

# Authenticate with SharePoint
context_auth = AuthenticationContext(url=subsite_url)  # Use subsite URL for authentication
context_auth.acquire_token_for_app(client_id, client_secret)
ctx = ClientContext(subsite_url, context_auth)

# Access SharePoint list items with paging
def get_sharepoint_list_items(ctx, list_name):
    try:
        sp_lists = ctx.web.lists
        s_list = sp_lists.get_by_title(list_name)
        list_items = s_list.items.paged(500).get().execute_query()
        return list_items
    except Exception as e:
        st.error(f"Error retrieving list items: {e}")
        return None

if ctx:
    # Get SharePoint list items with paging
    items = get_sharepoint_list_items(ctx, list_name)

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
        chart_column, metrics_column = st.columns([3, 1])  # Adjust the width ratio as needed
        with chart_column:
            st.plotly_chart(fig)

        # Display most recent values for Braner, Stamco, and Red Bud along with change since previous row
        with metrics_column:
            st.subheader("Current")
            latest_values = df.iloc[-1]  # Get the last row which contains the most recent values
            for column in ["Braner", "Stamco", "Red Bud"]:
                value_str = f"{latest_values[column]} days"  # Add "days" after the value
                ui.metric_card(title=f"{column}", content=value_str, description="", key=f"card_{column}")

        st.subheader("Data")

        # Display DataFrame with mm/dd/yyyy format for the date column
        st.dataframe(df_display, use_container_width=True)