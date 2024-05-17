from sharepoint_manager import get_sharepoint_list_items, sharepoint_urls, sharepoint_lists
from sharepoint_manager import read_secrets
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="KPI • Customer Surveys",
    page_icon="assets/MSP_Favicon.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

st.title("Customer Surveys")

url = sharepoint_urls["Home Site"]
list_name = sharepoint_lists["Customer Surveys"]

sharepoint_secrets = read_secrets()
client_id = sharepoint_secrets["client_id"]
client_secret = sharepoint_secrets["client_secret"]

items = get_sharepoint_list_items(url, list_name, client_id, client_secret)

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

    # Sort the DataFrame by 'Date' in descending order
    df_customer_surveys.sort_values(by='Date', ascending=False, inplace=True)

    # Display dataframes for different years and maintain new date format
    tabAll, tab2022, tab2023, tab2024 = st.tabs(["All", "2022", "2023", "2024"])
    df_2022 = df_customer_surveys[df_customer_surveys['Date'].dt.year == 2022]
    df_2023 = df_customer_surveys[df_customer_surveys['Date'].dt.year == 2023]
    df_2024 = df_customer_surveys[df_customer_surveys['Date'].dt.year == 2024]

    with tabAll:
        st.dataframe(df_customer_surveys, use_container_width=True, hide_index=True)
    with tab2022:
        st.dataframe(df_2022, use_container_width=True, hide_index=True)
    with tab2023:
        st.dataframe(df_2023, use_container_width=True, hide_index=True)
    with tab2024:
        st.dataframe(df_2024, use_container_width=True, hide_index=True)
    
    numeric_columns = ['On Time Performance', 'Quality of Processing', 'Pricing', 'Customer Service', 'Overall Satisfaction']
    df_customer_surveys[numeric_columns] = df_customer_surveys[numeric_columns].apply(pd.to_numeric, errors='coerce')

    avg_metrics = df_customer_surveys[numeric_columns].mean()

    categories = numeric_columns
    fig = px.line_polar(r=avg_metrics.values, theta=categories, line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                tickmode='array',
                tickvals=[i * 0.1 for i in range(int(50) + 1)],
                ticktext=['{:.1f}'.format(i * 0.1) if i % 5 == 0 else '' for i in range(int(50) + 1)],
                range=[0, 5],
                tickfont=dict(color='black')
            )
        )
    )
    st.plotly_chart(fig, use_container_width=True)