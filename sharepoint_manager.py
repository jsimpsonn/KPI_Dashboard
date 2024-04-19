from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from secrets_manager import read_secrets

def authenticate_sharepoint(subsite_url):
    # Read SharePoint credentials
    sharepoint_secrets = read_secrets()

    client_id = sharepoint_secrets["client_id"]
    client_secret = sharepoint_secrets["client_secret"]

    # Authenticate with SharePoint
    context_auth = AuthenticationContext(url=subsite_url)
    context_auth.acquire_token_for_app(client_id, client_secret)
    ctx = ClientContext(subsite_url, context_auth)

    return ctx

def get_sharepoint_list_items(subsite_url, list_name):
    ctx = authenticate_sharepoint(subsite_url)

    list_obj = ctx.web.lists.get_by_title(list_name)
    items = list_obj.items
    ctx.load(items)
    ctx.execute_query()
    
    return items

sharepoint_secrets = read_secrets()
sharepoint_urls = {
    "Home Site": sharepoint_secrets["main_site_url"],
    "Plant Operations": sharepoint_secrets["plant_operations_subsite_url"],
    "Customer Satisfaction": sharepoint_secrets["customer_satisfaction_subsite_url"],
    "Order Entry & Receiving": sharepoint_secrets["order_entry_subsite_url"],
    "Safety": sharepoint_secrets["safety_subsite_url"]
}

sharepoint_lists = {
    "Loading Times": sharepoint_secrets["loading_times_list_name"],
    "Lead Times": sharepoint_secrets["lead_times_list_name"],
    "Customer Surveys": sharepoint_secrets["customer_surveys_list_name"],
    "Work Order On-time Delivery": sharepoint_secrets["otd_list_name"],
    "Safety Corrective Actions": sharepoint_secrets["safety_2023_list_name"],
    "2024 Safety OFI's": sharepoint_secrets["safety_2024_list_name"],
    "Scrap Pricing": sharepoint_secrets["scrap_pricing_list_name"]
}
