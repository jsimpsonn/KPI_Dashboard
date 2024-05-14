import os
import toml
import streamlit as st
from msal import ConfidentialClientApplication
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

def read_secrets():
    """
    Reads SharePoint credentials from a TOML file located in the Streamlit home directory.
    """
    streamlit_home = os.getenv("STREAMLIT_HOME", "")
    secrets_path = os.path.join(streamlit_home, ".streamlit", "secrets.toml")
    sharepoint_credentials = toml.load(secrets_path)["sharepoint"]
    return sharepoint_credentials

def authenticate_sharepoint(subsite_url, client_id, client_secret):
    """
    Authenticates and returns a SharePoint client context for given credentials and subsite URL.
    """
    context_auth = AuthenticationContext(url=subsite_url)
    context_auth.acquire_token_for_app(client_id, client_secret)
    return ClientContext(subsite_url, context_auth)

def get_sharepoint_list_items(subsite_url, list_name, client_id, client_secret):
    """
    Retrieves SharePoint list items from specified list on the given subsite.
    """
    ctx = authenticate_sharepoint(subsite_url, client_id, client_secret)
    list_obj = ctx.web.lists.get_by_title(list_name)
    try:
        list_items = list_obj.items.top(500).get().execute_query()
        return list_items
    except Exception as e:
        st.error(f"Error retrieving list items: {e}")
        return None

def authenticate_user():
    """
    Authenticates with Azure AD and returns an access token or None if authentication fails.
    """
    app = ConfidentialClientApplication(
        st.secrets["azure"]["client_id"],
        authority=f'https://login.microsoftonline.com/{st.secrets["azure"]["tenant_id"]}',
        client_credential=st.secrets["azure"]["client_secret"]
    )
    token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in token_response:
        return token_response['access_token']
    elif "error" in token_response:
        st.error(f"Authentication failed: {token_response['error_description']}")
    else:
        st.error("Authentication failed. No access token returned.")
    return None

# Initialize app by reading secrets and authenticating user
sharepoint_secrets = read_secrets()
sharepoint_urls = {
    "Home Site": sharepoint_secrets["main_site_url"],
    "Plant Operations": sharepoint_secrets["plant_operations_subsite_url"],
    "Customer Satisfaction": sharepoint_secrets["customer_satisfaction_subsite_url"],
    "Order Entry & Receiving": sharepoint_secrets["order_entry_subsite_url"]
}
sharepoint_lists = {
    "Loading Times": sharepoint_secrets["loading_times_list_name"],
    "Lead Times": sharepoint_secrets["lead_times_list_name"],
    "Customer Surveys": sharepoint_secrets["customer_surveys_list_name"],
    "Work Order On-time Delivery": sharepoint_secrets["otd_list_name"],
    "Requests for Disposition 2024": sharepoint_secrets["concessions_list_name_2024"],
    "Requests for Disposition": sharepoint_secrets["concessions_list_name_2023"]
}
access_token = authenticate_user()