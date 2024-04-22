import os
import streamlit as st
import toml
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

st.cache_resource()
def read_secrets():
    # Get the path to the secrets TOML file
    streamlit_home = os.environ.get("STREAMLIT_HOME", "")
    secrets_path = os.path.join(streamlit_home, ".streamlit", "secrets.toml")
    
    # Load SharePoint credentials from TOML file
    sharepoint_credentials = toml.load(secrets_path)["sharepoint"]
    return sharepoint_credentials

def authenticate_sharepoint(subsite_url, client_id, client_secret):
    # Authenticate with SharePoint
    context_auth = AuthenticationContext(url=subsite_url)
    context_auth.acquire_token_for_app(client_id, client_secret)
    ctx = ClientContext(subsite_url, context_auth)
    return ctx

def get_sharepoint_list_items(subsite_url, list_name, client_id, client_secret):
    ctx = authenticate_sharepoint(subsite_url, client_id, client_secret)
    list_obj = ctx.web.lists.get_by_title(list_name)
    try:
        # Retrieve list items with paging
        list_items = list_obj.items.top(500).get().execute_query()
        return list_items
    except Exception as e:
        st.error(f"Error retrieving list items: {e}")
        return None

# Read SharePoint credentials from TOML file
sharepoint_secrets = read_secrets()
client_id = sharepoint_secrets["client_id"]
client_secret = sharepoint_secrets["client_secret"]

# Define SharePoint URLs and Lists
sharepoint_urls = {
    "Home Site": sharepoint_secrets["main_site_url"],
    "Plant Operations": sharepoint_secrets["plant_operations_subsite_url"],
    "Customer Satisfaction": sharepoint_secrets["customer_satisfaction_subsite_url"],
    "Order Entry & Receiving": sharepoint_secrets["order_entry_subsite_url"],
}

sharepoint_lists = {
    "Loading Times": sharepoint_secrets["loading_times_list_name"],
    "Lead Times": sharepoint_secrets["lead_times_list_name"],
    "Customer Surveys": sharepoint_secrets["customer_surveys_list_name"],
    "Work Order On-time Delivery": sharepoint_secrets["otd_list_name"],
}
