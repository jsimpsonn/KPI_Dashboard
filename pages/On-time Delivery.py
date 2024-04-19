from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
import streamlit as st
import pandas as pd
import plotly.express as px

# App Layout
st.set_page_config(
    page_title="KPI • OTD",
    page_icon="assets/MSP_Favicon.png",
)

st.title("Work Order On-time Delivery")
st.subheader("Summary")

# Read SharePoint credentials
sharepoint_secrets = st.secrets["sharepoint"]
client_id = sharepoint_secrets["client_id"]
client_secret = sharepoint_secrets["client_secret"]
subsite_url = sharepoint_secrets["customer_satisfaction_subsite_url"]
list_name = sharepoint_secrets["otd_list_name"]

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

# Plot the on-time delivery percentage
otd = px.line(df_OTD, x=df.index, y="Percent")
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