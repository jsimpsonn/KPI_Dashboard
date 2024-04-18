from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui

st.set_page_config(
    page_title="KPI • Customer Surveys",
    page_icon="assets/MSP_Favicon.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

st.title("Customer Surveys")

# Read SharePoint credentials
sharepoint_secrets = st.secrets["sharepoint"]
client_id = sharepoint_secrets["client_id"]
client_secret = sharepoint_secrets["client_secret"]
main_site_url = sharepoint_secrets["main_site_url"]
list_name = sharepoint_secrets["customer_surveys_list_name"]

# Authenticate with SharePoint
context_auth = AuthenticationContext(url=main_site_url)  # Use subsite URL for authentication
context_auth.acquire_token_for_app(client_id, client_secret)
ctx = ClientContext(main_site_url, context_auth)

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
        data = []
        for item in items:
            item_data = {
                "Date": pd.to_datetime(item.properties.get("Date")),
                "Company": item.properties.get("Title"),
                "On Time Performance": item.properties.get("On_x0020_Time_x0020_Performance"),
                "Quality of Processing": item.properties.get("Quality_x0020_of_x0020_Processin"),
                "Pricing": item.properties.get("Pricing"),
                "Customer Service": item.properties.get("Customer_x0020_Service"),
                "Overall Satisfaction": item.properties.get("Overall_x0020_Satisfaction"),
                "Comments": item.properties.get("Comments"),
            }
            data.append(item_data)

        df_customer_surveys = pd.DataFrame(data)
        
        st.caption('The form for customers to fill out can be found and shared from [here](https://forms.office.com/r/dvnMP3f8DM)')

        tabAll, tab2022, tab2023, tab2024 =st.tabs(["All", "2022", "2023", "2024"])
        df_2022 = df_customer_surveys[df_customer_surveys["Date"].dt.year == 2022]
        df_2023 = df_customer_surveys[df_customer_surveys["Date"].dt.year == 2023]
        df_2024 = df_customer_surveys[df_customer_surveys["Date"].dt.year == 2024]

        with tabAll:
            st.dataframe(df_customer_surveys,use_container_width=True)
        with tab2022:
            st.dataframe(df_2022,use_container_width=True)
        with tab2023:
            st.dataframe(df_2023,use_container_width=True)
        with tab2024:
            st.dataframe(df_2024,use_container_width=True)
