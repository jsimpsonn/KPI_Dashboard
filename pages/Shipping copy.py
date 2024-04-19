import os
from dotenv import load_dotenv
import toml
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
import streamlit as st
import pandas as pd
import plotly.express as px

# Load environment variables from .env file
load_dotenv()

def read_secrets():
    return {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "plant_operations_subsite_url": os.getenv("PLANT_OPERATIONS_SUBSITE_URL"),
        "loading_times_list_name": os.getenv("LOADING_TIMES_LIST_NAME")
    }

# Check if running in local environment
is_local = "streamlit" not in os.environ.get("SERVER_SOFTWARE", "")

# App Layout
st.set_page_config(
    page_title="KPI • Shipping",
    page_icon="assets/MSP_Favicon.png",
)

st.title("Shipping")
st.subheader("Summary")

if is_local:
    # Read credentials from local secrets.toml file
    sharepoint_secrets = read_secrets()
else:
    # Read credentials from Streamlit Secrets
    sharepoint_secrets = st.secrets["sharepoint"]

client_id = sharepoint_secrets["client_id"]
client_secret = sharepoint_secrets["client_secret"]
subsite_url = sharepoint_secrets["plant_operations_subsite_url"]
list_name = sharepoint_secrets["loading_times_list_name"]

# Authenticate with SharePoint
context_auth = AuthenticationContext(url=subsite_url)  # Use subsite URL for authentication
context_auth.acquire_token_for_app(client_id, client_secret)
ctx = ClientContext(subsite_url, context_auth)

# Access SharePoint list items
def get_sharepoint_list_items():
    list_obj = ctx.web.lists.get_by_title(list_name)
    items = list_obj.items
    ctx.load(items)
    ctx.execute_query()
    return items

# Get SharePoint list items
items = get_sharepoint_list_items()

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

# Sort DataFrame by 'Date' column from oldest to newest
df = df.sort_values(by='Date', ascending=True)

# Convert 'Date' column to mm/YYYY format
df['Date'] = df['Date'].dt.strftime('%B %Y')

# Plotly line chart
fig = px.line(df, x="Date", y="Percent", title="Trucks Loaded in One Hour or Less")
fig.update_layout(xaxis=dict(dtick="3"),xaxis_tickangle=45)
st.plotly_chart(fig)

st.subheader("Data")

df = df.set_index('Date', drop=True)

# Display DataFrame
st.dataframe(df, use_container_width=True)
