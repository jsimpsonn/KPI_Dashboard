import streamlit as st
from sharepoint_manager import get_sharepoint_list_items, sharepoint_urls, sharepoint_lists
from sharepoint_manager import read_secrets, authenticate_user
import plotly.express as px
import pandas as pd
import streamlit_shadcn_ui as ui
import datetime

st.set_page_config(page_title="Print",layout="wide", page_icon="assets/MSP_Favicon.png")

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
# Setting up headers and global containers
    st.markdown(
    """
    <style>
    @media print {
        @page {
            size: landscape;
            margin: 0;
        }
        body {
            -webkit-print-color-adjust: exact;
            margin-left: -50px;
            padding-top: 25px;
            padding-left: 55px;
        }
        .reportview-container .main .block-container {
            max-width: 100%;
            padding-right: 10px;
            padding-left: 10px;
        }
        .element-container {
            display: flex;
            flex-wrap: wrap;
        }
        .stChart, .stDataFrame, .stTable {
            width: 100% !important;
        }
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div:nth-child(2) {
        margin-top: 0px;
        margin-right: 0px;
        margin-left: 0px;
        padding-top: 0px;
        padding-right: 0px;
        padding-left: 0px;
        }
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-vk3wp9.eczjsme11 {
        display: none;
        }
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div:nth-child(4) {
        padding-top: 20px;
        }
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div:nth-child(5), #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div:nth-child(6) {
        padding-top: 50px;
        }
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div:nth-child(6) {
        padding-top: 30px;
        }
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 {
        padding-bottom: 100px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)
    today_date = datetime.datetime.now().strftime('%m/%d/%Y')
    st.header(f"KPI Summary - {today_date}", divider='orange')
    # Define columns for OTD and Shipping containers
    row1 = st.columns(2)
    row2 = st.columns(3)
    row3 = st.columns(3)
    row4 = st.columns(3)

    lead_times_container = row1[0].container(border=True)
    with lead_times_container:
        # Lead Times Chart
        lead_times_data = get_sharepoint_list_items(
            sharepoint_urls["Customer Satisfaction"],
            sharepoint_lists["Lead Times"],
            read_secrets()["client_id"],
            read_secrets()["client_secret"]
        )
        if lead_times_data:
            df_lead_times = pd.DataFrame({
                "Date": [x.properties.get("Date") for x in lead_times_data],
                "Braner": [x.properties.get("Braner") for x in lead_times_data],
                "Stamco": [x.properties.get("Stamco1") for x in lead_times_data],
                "Red Bud": [x.properties.get("Red_x0020_Bud") for x in lead_times_data]
            })
            df_lead_times['Date'] = pd.to_datetime(df_lead_times['Date']).dt.strftime('%m/%d/%Y')
            lead_times_chart = px.line(df_lead_times, x="Date", y=["Braner", "Stamco", "Red Bud"], labels={"value": "Lead Time (days)"})
            lead_times_chart.update_layout(xaxis=dict(dtick="14"),xaxis_tickangle=45)
            st.plotly_chart(lead_times_chart, use_container_width=True)


    # Equipment Status Metrics in the second column container of row1
    equipment_status_container = row1[1].container(border=False)
    with equipment_status_container:
        if lead_times_data:  # Ensure this data is already loaded
            st.subheader("Current Lead Times")
            for equipment in ["Braner", "Stamco", "Red Bud"]:
                latest_values = df_lead_times.iloc[-1]  # Get the last row which contains the most recent values
                value_str = f"{latest_values[equipment]} days"  # Add "days" after the value
                ui.metric_card(title=f"{equipment}", content=value_str, description="", key=f"card_{equipment}")

    ###### Production
    stamco_production_container = row2[0].container(border=True)
    with stamco_production_container:
        df_stamco_tonnage = pd.read_csv("data/production/stamco.csv")
        stamco_production = px.line(df_stamco_tonnage, x="Month", y=["1st", "2nd", "3rd"], title="Stamco Production")
        stamco_production.update_layout(yaxis_title="TPH",xaxis=dict(dtick="3"),xaxis_tickangle=45)
        st.plotly_chart(stamco_production, use_container_width=True)

    braner_production_container = row2[1].container(border=True)
    with braner_production_container:
        df_braner_tonnage = pd.read_csv("data/production/braner.csv")
        braner_production = px.line(df_braner_tonnage, x="Month", y=["1st", "2nd"], title="Braner Production")
        braner_production.update_layout(yaxis_title="TPH",xaxis=dict(dtick="3"),xaxis_tickangle=45)
        st.plotly_chart(braner_production, use_container_width=True)

    redbud_production_container = row2[2].container(border=True)
    with redbud_production_container:
        df_redbud_tonnage = pd.read_csv("data/production/redbud.csv")
        redbud_production = px.line(df_redbud_tonnage, x="Month", y=["1st", "2nd"], title="Redbud Production")
        redbud_production.update_layout(yaxis_title="TPH",xaxis=dict(dtick="3"),xaxis_tickangle=45)
        st.plotly_chart(redbud_production, use_container_width=True)

    ###### Downtime
    stamco_downtime_container = row3[0].container(border=True)
    with stamco_downtime_container:
        df_stamco_tonnage = pd.read_csv("data/downtime/stamco.csv")
        stamco_downtime = px.line(df_stamco_tonnage, x="Month", y=["MR", "NMR"], title="Stamco Downtime")
        stamco_downtime.update_layout(yaxis_title="Hours",xaxis=dict(dtick="3"),xaxis_tickangle=45)
        st.plotly_chart(stamco_downtime, use_container_width=True)

    braner_downtime_container = row3[1].container(border=True)
    with braner_downtime_container:
        df_braner_tonnage = pd.read_csv("data/downtime/braner.csv")
        braner_downtime = px.line(df_braner_tonnage, x="Month", y=["MR", "NMR"], title="Braner Downtime")
        braner_downtime.update_layout(yaxis_title="Hours",xaxis=dict(dtick="3"),xaxis_tickangle=45)
        st.plotly_chart(braner_downtime, use_container_width=True)

    redbud_downtime_container = row3[2].container(border=True)
    with redbud_downtime_container:
        df_redbud_tonnage = pd.read_csv("data/downtime/redbud.csv")
        redbud_downtime = px.line(df_redbud_tonnage, x="Month", y=["MR", "NMR"], title="Redbud Downtime")
        redbud_downtime.update_layout(yaxis_title="Hours",xaxis=dict(dtick="3"),xaxis_tickangle=45)
        st.plotly_chart(redbud_downtime, use_container_width=True)

    # OTD Chart in the first column container
    otd_container = row4[0].container(border=True)
    with otd_container:
        otd_data = get_sharepoint_list_items(
            sharepoint_urls["Customer Satisfaction"],
            sharepoint_lists["Work Order On-time Delivery"],
            read_secrets()["client_id"],
            read_secrets()["client_secret"]
        )
        if otd_data:
            df_otd = pd.DataFrame({
                "Date": [x.properties.get("Date") for x in otd_data],
                "Percent": [x.properties.get("Percent") * 100 for x in otd_data]
            })
            df_otd['Date'] = pd.to_datetime(df_otd['Date']).dt.strftime("%B %Y")
            otd_chart = px.line(df_otd, x='Date', y='Percent', title="Work Order On-time Delivery")
            st.plotly_chart(otd_chart, use_container_width=True)

    # Shipping Chart in the second column container
    shipping_container = row4[1].container(border=True)
    with shipping_container:
        shipping_data = get_sharepoint_list_items(
            sharepoint_urls["Plant Operations"],
            sharepoint_lists["Loading Times"],
            read_secrets()["client_id"],
            read_secrets()["client_secret"]
        )
        if shipping_data:
            df_shipping = pd.DataFrame({
                "Date": [x.properties.get("Date") for x in shipping_data],
                "Percent": [x.properties.get("OData__x0025_") * 100 for x in shipping_data]
            })
            df_shipping['Date'] = pd.to_datetime(df_shipping['Date'])
            df_shipping = df_shipping.sort_values(by='Date', ascending=True)
            df_shipping['Date'] = pd.to_datetime(df_shipping['Date']).dt.strftime('%B %Y')
            shipping_chart = px.line(df_shipping, x="Date", y="Percent", title="Shipping - Trucks Loaded in One Hour or Less")
            shipping_chart.update_layout(xaxis=dict(dtick="3"),xaxis_tickangle=45)
            st.plotly_chart(shipping_chart, use_container_width=True)

    ######## Safety
    shipping_container = row4[2].container(border=False)
    with shipping_container:
        df_safety = pd.read_csv("data/safety.csv")
        # Convert 'Date' column to datetime
        df_safety['Date'] = pd.to_datetime(df_safety['Date'])
        # Format 'Date' column as "mm/dd/yyyy"
        df_safety['Date'] = df_safety['Date'].dt.strftime('%m/%d/%Y')
        df_safety['Year'] = df_safety['Date'].str[-4:]
        df_grouped_recordable = df_safety[df_safety['Recordable'] == 'Y'].groupby('Year').size().reset_index(name='Recordables')
        df_grouped_total = df_safety.groupby('Year').size().reset_index(name='Total Incidents')
        df_combined = df_grouped_total.merge(df_grouped_recordable, how='left', on='Year').fillna(0)
        st.subheader("Safety")
        st.dataframe(df_combined.set_index('Year'), use_container_width=False)