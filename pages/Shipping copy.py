import streamlit as st
import pandas as pd
import plotly.express as px
from sharepoint_manager import get_sharepoint_list_items, sharepoint_urls, sharepoint_lists

url = sharepoint_urls["Plant Operations"]
list_name = sharepoint_lists["Loading Times"]

# Access SharePoint list items
items = get_sharepoint_list_items(url, list_name)

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
fig.update_layout(xaxis=dict(dtick="3"), xaxis_tickangle=45)
st.plotly_chart(fig)

st.subheader("Data")

df = df.set_index('Date', drop=True)

# Display DataFrame
st.dataframe(df, use_container_width=True)