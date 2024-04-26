import streamlit as st
import pandas as pd
from sharepoint_manager import get_sharepoint_list_items, sharepoint_urls, read_secrets, authenticate_user

def display_customer_concessions(df_customer_concessions, selected_year, top_items):
    subheader_text = f"Top {top_items} Customers by # of Concessions - {selected_year}"
    st.subheader(subheader_text)

    with st.container(border=True):
        row1 = st.columns([1, 2])

        with row1[0]:
            customer_summary = df_customer_concessions.groupby('Customer').agg(
                Total=('Customer', 'size'),
                Shippable=('Can we Ship?', lambda x: (x == 'Yes').sum())
            )
            customer_summary['Percentage Shippable'] = (customer_summary['Shippable'] / customer_summary['Total']).round(4) * 100
            customer_summary = customer_summary.sort_values(by='Total', ascending=False).head(top_items)
            customer_summary['Percentage Shippable'] = customer_summary['Percentage Shippable'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(customer_summary, use_container_width=True)

        with row1[1]:
            # Ensure the DataFrame has 'Customer' as index before plotting
            chart_data = customer_summary[['Total']]
            chart_data.index = customer_summary.index  # Set 'Customer' as the index
            st.bar_chart(chart_data, use_container_width=True)

# Set page configuration
st.set_page_config(
    page_title="KPI • Concessions",
    page_icon="assets/MSP_Favicon.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

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
                        "CSR": item.properties.get("CSR"),
                        "Line Order Ran On": item.properties.get("lineorderranon"),
                    }
                except Exception as e:
                    st.error(f"Error processing item: {e}")
                    continue
                data.append(item_data)
            all_data.extend(data)

    # Assume df_customer_concessions is already created and populated with all necessary data
    df_customer_concessions = pd.DataFrame(all_data)

    # Convert 'Date' to datetime and extract years
    df_customer_concessions['Date'] = pd.to_datetime(df_customer_concessions['Date'])
    years = df_customer_concessions['Date'].dt.year.unique()
    all_years = ["All"] + sorted([str(year) for year in years])

    # Create a select box for year selection
    selected_year = st.radio("Select year", all_years, horizontal=True)

    # Create a slider for selecting the number of top items to show
    top_items = st.slider("Select the number of customers with the most concessions to show", 1, 50, 10)

    # Filter the DataFrame based on the selected year
    if selected_year == "All":
        filtered_concessions = df_customer_concessions
    else:
        filtered_concessions = df_customer_concessions[df_customer_concessions['Date'].dt.year == int(selected_year)]

    # Display the customer concessions
    display_customer_concessions(filtered_concessions, selected_year, top_items)

# with st.expander("Detailed Data", expanded=False):
#     st.dataframe(filtered_concessions, use_container_width=True, hide_index=True)
