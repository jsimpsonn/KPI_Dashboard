import streamlit as st
from sharepoint_manager import get_sharepoint_list_items, sharepoint_urls, sharepoint_lists
from sharepoint_manager import read_secrets, authenticate_user
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import streamlit_shadcn_ui as ui
import datetime
from st_pages import show_pages_from_config, hide_pages

st.set_page_config(page_title="Print",layout="wide", page_icon="assets/MSP_Favicon.png")
show_pages_from_config()
hide_pages("Print Summary")

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    access_token = authenticate_user()
    if access_token:
        st.session_state['authenticated'] = True
        st.session_state['access_token'] = access_token
    else:
        st.error("You must be authenticated to access this dashboard.")
        st.stop()

if st.session_state['authenticated']:
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
        padding-top: 0px;
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

    row1 = st.columns([2,1])
    row2 = st.columns(3)
    row3 = st.columns(2)
    row4 = st.columns(3)

    lead_times_container = row1[0].container(border=True)
    with lead_times_container:
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

    equipment_status_container = row1[1].container(border=False)
    with equipment_status_container:
        if lead_times_data:
            st.subheader("Current Lead Times")
            for equipment in ["Braner", "Stamco", "Red Bud"]:
                latest_values = df_lead_times.iloc[-1]
                value_str = f"{latest_values[equipment]} days"
                ui.metric_card(title=f"{equipment}", content=value_str, description="", key=f"card_{equipment}")

    ###### Production
    stamco_production_container = row2[0].container(border=True)
    with stamco_production_container:
        df_stamco_tonnage = pd.read_csv("data/production/stamco.csv")
        stamco_production = px.line(df_stamco_tonnage, x="Month", y=["1st", "2nd", "3rd"], title="Stamco Production")
        stamco_production.update_layout(yaxis_title="TPH",xaxis=dict(dtick="3"),xaxis_tickangle=45)
        stamco_production.add_hline(y=10, line_dash="dot", annotation_text="Goal", annotation_position="top right")
        st.plotly_chart(stamco_production, use_container_width=True)

    braner_production_container = row2[1].container(border=True)
    with braner_production_container:
        df_braner_tonnage = pd.read_csv("data/production/braner.csv")
        braner_production = px.line(df_braner_tonnage, x="Month", y=["1st", "2nd"], title="Braner Production")
        braner_production.update_layout(yaxis_title="TPH",xaxis=dict(dtick="3"),xaxis_tickangle=45)
        braner_production.add_hline(y=18.5, line_dash="dot", annotation_text="Goal", annotation_position="top right")
        st.plotly_chart(braner_production, use_container_width=True)

    redbud_production_container = row2[2].container(border=True)
    with redbud_production_container:
        df_redbud_tonnage = pd.read_csv("data/production/redbud.csv")
        redbud_production = px.line(df_redbud_tonnage, x="Month", y=["1st", "2nd"], title="Redbud Production")
        redbud_production.update_layout(yaxis_title="TPH",xaxis=dict(dtick="3"),xaxis_tickangle=45)
        redbud_production.add_hline(y=20, line_dash="dot", annotation_text="Goal", annotation_position="top right")
        st.plotly_chart(redbud_production, use_container_width=True)

    # Define colors for each line
    colors = ['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)']

    mr_downtime_data = []
    nmr_downtime_data = []

    # Loop through each line (Stamco, Braner, Redbud)
    for line in ["Stamco", "Braner", "Redbud"]:
        # Read the CSV file for the current line
        df = pd.read_csv(f"data/downtime/{line.lower()}/{line.lower()}.csv")

        # Extract the MR and NMR downtime data
        mr_downtime = df["MR"]
        nmr_downtime = df["NMR"]

        # Append the data to the respective lists
        mr_downtime_data.append(mr_downtime)
        nmr_downtime_data.append(nmr_downtime)

        mr_fig = go.Figure()

    # Add MR downtime traces
    for i, mr_data in enumerate(mr_downtime_data):
        mr_fig.add_trace(go.Scatter(
            x=df["Month"],
            y=mr_data,
            mode='lines',
            name=f"{['Stamco', 'Braner', 'Redbud'][i]} MR",
            fill='tozeroy',
            line=dict(color=colors[i], width=2),
            fillcolor=f'rgba({colors[i][4:-1]}, 0.2)'
        ))

    # Add goal hlines for MR downtime
    mr_fig.add_hline(y=15.5, line_dash="dot", annotation_text="Stamco MR Goal", annotation_position="top right", line_color='rgb(255, 0, 0)')
    mr_fig.add_hline(y=26, line_dash="dot", annotation_text="Braner MR Goal", annotation_position="top right", line_color='rgb(0, 255, 0)')
    mr_fig.add_hline(y=16.5, line_dash="dot", annotation_text="Redbud MR Goal", annotation_position="top left", line_color='rgb(0, 0, 255)')

    # Set chart title and axis labels
    mr_fig.update_layout(
        title="Maintenance Related Downtime",
        xaxis_title="Month",
        yaxis_title="Hours",
        xaxis_tickangle=45
    )

    maint_related = row3[0].container(border=True)
    with maint_related:
        st.plotly_chart(mr_fig, use_container_width=True)

    # Create a chart for NMR downtime
    nmr_fig = go.Figure()

    # Add NMR downtime traces
    for i, nmr_data in enumerate(nmr_downtime_data):
        nmr_fig.add_trace(go.Scatter(
            x=df["Month"],
            y=nmr_data,
            mode='lines',
            name=f"{['Stamco', 'Braner', 'Redbud'][i]} NMR",
            fill='tozeroy',
            line=dict(color=colors[i], width=2),
            fillcolor=f'rgba({colors[i][4:-1]}, 0.2)'
        ))

    # Add goal hlines for NMR downtime
    nmr_fig.add_hline(y=45, line_dash="dot", annotation_text="Stamco NMR Goal", annotation_position="top left", line_color='rgb(255, 0, 0)')
    nmr_fig.add_hline(y=45, line_dash="dot", annotation_text="Braner NMR Goal", annotation_position="top right", line_color='rgb(0, 255, 0)')
    nmr_fig.add_hline(y=12.5, line_dash="dot", annotation_text="Redbud NMR Goal", annotation_position="top right", line_color='rgb(0, 0, 255)')

    # Set chart title and axis labels
    nmr_fig.update_layout(
        title="Non-maintenance Related DT",
        xaxis_title="Month",
        yaxis_title="Hours",
        xaxis_tickangle=45
    )

    nonmaint_related = row3[1].container(border=True)
    with nonmaint_related:
        st.plotly_chart(nmr_fig, use_container_width=True)

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
            otd_chart.add_hline(y=77, line_dash="dot", annotation_text="Goal")
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
            shipping_chart.update_layout(xaxis=dict(dtick="3"))
            shipping_chart.add_hline(y=75, line_dash="dot", annotation_text="Goal")
            st.plotly_chart(shipping_chart, use_container_width=True)

    ######## Safety
    shipping_container = row4[2].container(border=False)
    with shipping_container:
        df_safety = pd.read_csv("data/safety.csv")
        df_safety['Date'] = pd.to_datetime(df_safety['Date'])
        df_safety['Date'] = df_safety['Date'].dt.strftime('%m/%d/%Y')
        df_safety['Year'] = df_safety['Date'].str[-4:]
        df_grouped_recordable = df_safety[df_safety['Recordable'] == 'Y'].groupby('Year').size().reset_index(name='Recordables')
        df_grouped_total = df_safety.groupby('Year').size().reset_index(name='Total Incidents')
        df_combined = df_grouped_total.merge(df_grouped_recordable, how='left', on='Year').fillna(0)
        st.subheader("Safety")
        st.dataframe(df_combined.set_index('Year'), use_container_width=False)