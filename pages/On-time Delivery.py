from sharepoint_manager import get_sharepoint_list_items, sharepoint_urls, sharepoint_lists
from sharepoint_manager import read_secrets
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