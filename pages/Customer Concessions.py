import streamlit as st
import pandas as pd
from sharepoint_manager import get_sharepoint_list_items, sharepoint_urls, read_secrets, authenticate_user
from st_pages import show_pages_from_config, hide_pages

@st.cache_data()
def load_data():
    # Get SharePoint URLs and Lists
    url = sharepoint_urls["Order Entry & Receiving"]
    list_names = ["Requests for Disposition 2024", "Requests for Disposition"]

    # Get SharePoint secrets
    sharepoint_secrets = read_secrets()
    client_id = sharepoint_secrets["client_id"]
    client_secret = sharepoint_secrets["client_secret"]

    all_data = []  # Initialize empty list to store all data from both lists

    for list_name in list_names:
        items = get_sharepoint_list_items(url, list_name, client_id, client_secret)
        if items:
            data = []
            for item in items:
                try:
                    item_data = {
                        "Date": pd.to_datetime(item.properties.get("Date")).strftime('%m/%d/%Y') if item.properties.get("Date") else None,
                        "Customer": item.properties.get("Customer"),
                        "WO #": str(item.properties.get("WO_x0023_")).replace(',', '') if item.properties.get("WO_x0023_") is not None else None,
                        "PO #": item.properties.get("PO_x0023_"),
                        "Reason for Call": item.properties.get("Reason_x0020_for_x0020_Call_x002"),
                        "Customer Response": item.properties.get("CustomerResponse"),
                        "Can we Ship?": "Yes" if item.properties.get("CanWeShip_x003f_") else "No",
                        "Process Owner": item.properties.get("ProcessOwner"),
                        "Line Order Ran On": item.properties.get("lineorderranon"),
                    }
                except Exception as e:
                    st.error(f"Error processing item: {e}")
                    continue
                data.append(item_data)
            all_data.extend(data)

    # By Customer
    df_customer_concessions = pd.DataFrame(all_data)
    df_customer_concessions['Date'] = pd.to_datetime(df_customer_concessions['Date'])
    years = df_customer_concessions['Date'].dt.year.unique()
    all_years = ["All"] + sorted([str(year) for year in years])

    # By Process Owner
    df_process_owner = pd.DataFrame(all_data)
    df_process_owner['Date'] = pd.to_datetime(df_process_owner['Date'])

    return df_customer_concessions, df_process_owner, all_years

def customer_concessions_total(df_customer_concessions):
    subheader_text = f"Top {st.session_state['top_items']} Customers by # of Concessions - {st.session_state['selected_year']}"
    st.subheader(subheader_text)

    with st.container(border=True):
        row1 = st.columns([1, 2])

        with row1[0]:
            customer_summary = df_customer_concessions.groupby('Customer').agg(
                Total=('Customer', 'size'),
                Shippable=('Can we Ship?', lambda x: (x == 'Yes').sum())
            )
            customer_summary['Percentage Shippable'] = (customer_summary['Shippable'] / customer_summary['Total']).round(4) * 100
            customer_summary = customer_summary.sort_values(by='Total', ascending=False).head(st.session_state['top_items'])
            customer_summary['Percentage Shippable'] = customer_summary['Percentage Shippable'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(customer_summary, use_container_width=True)

        with row1[1]:
            # Ensure the DataFrame has 'Customer' as index before plotting
            chart_data = customer_summary[['Total']]
            chart_data.index = customer_summary.index  # Set 'Customer' as the index
            st.bar_chart(chart_data, use_container_width=True)

def customer_concessions_date(df_process_owner):
    subheader_text = "Process Owner"
    st.subheader(subheader_text)
    with st.container(border=True):
        row1 = st.columns([1, 1])
        with row1[0]:
            # Convert month names to month numbers and sort
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            process_owner_summary = df_process_owner.groupby([df_process_owner['Date'].dt.strftime('%B'), 'Process Owner']).size().unstack(fill_value=0)
            process_owner_summary = process_owner_summary.reindex(month_order, axis=0, fill_value=0)
            
            # Add a last column for total for each month
            process_owner_summary['Total'] = process_owner_summary.sum(axis=1)
            
            st.dataframe(process_owner_summary, use_container_width=True, height=460)

        with row1[1]:
            st.bar_chart(process_owner_summary.drop(columns=['Total']), use_container_width=True)

# Set page configuration
st.set_page_config(
    page_title="KPI • Concessions",
    page_icon="assets/MSP_Favicon.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)
show_pages_from_config()
hide_pages("Print Summary")
# Check if the user is already authenticated
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    access_token = authenticate_user()
    if access_token:
        st.session_state['authenticated'] = True
        st.session_state['access_token'] = access_token
    else:
        st.error("You must be authenticated to access this dashboard.")
        st.stop()  # Stop the app if not authenticated

if st.session_state['authenticated']:
    st.title("Customer Concessions")

    df_customer_concessions, df_process_owner, all_years = load_data()

    st.session_state.selected_year = st.radio("Select year", all_years, key='year', horizontal=True)
    st.session_state.top_items = st.slider("Select the number of customers with the most concessions to show", 1, 50, 10, key='items')

    if st.session_state.selected_year == "All":
        filtered_concessions = df_customer_concessions
        filtered_process_owner = df_process_owner
    else:
        filtered_concessions = df_customer_concessions[df_customer_concessions['Date'].dt.year == int(st.session_state.selected_year)]
        filtered_process_owner = df_process_owner[df_process_owner['Date'].dt.year == int(st.session_state.selected_year)]

    # Display the customer concessions
    customer_concessions_total(filtered_concessions)
    customer_concessions_date(filtered_process_owner)
