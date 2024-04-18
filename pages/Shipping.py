from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
import streamlit as st
import pandas as pd
import plotly.express as px
import toml

# Read SharePoint credentials from secrets.toml
def read_secrets():
    with open("secrets.toml", "r") as f:
        secrets = toml.load(f)
    return secrets["sharepoint"]

st.title("Shipping")
st.subheader("Summary")

# Read the shipping data
df_shipping = pd.read_csv("data/shipping.csv")

    # Read SharePoint credentials
    sharepoint_secrets = read_secrets()
    client_id = sharepoint_secrets["client_id"]
    client_secret = sharepoint_secrets["client_secret"]
    subsite_url = sharepoint_secrets["subsite_url"]
    list_name = sharepoint_secrets["list_name"]

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

    # Extract item properties
    data = []
    for item in items:
        item_data = {
            "Date": item.properties.get("Date"),
            "Percent": item.properties.get("OData__x0025_"),  # Using OData__x0025_ for Actual
            "Goal": item.properties.get("Goal"),
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
    fig = px.line(df, x="Date", y="Percent", title="Actual Percentage Over Time")
    st.plotly_chart(fig)

    st.subheader("Data")

    df = df.set_index('Date', drop=True)

    # Display DataFrame
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
