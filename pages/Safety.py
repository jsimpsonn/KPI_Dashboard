import streamlit as st
import pandas as pd

st.set_page_config(page_title="KPI | Safety",page_icon="assets/MSP_Favicon.png", layout="wide", initial_sidebar_state="auto", menu_items=None)

# Read the CSV file
df_safety = pd.read_csv("data/safety.csv")

st.title("Safety")
st.subheader("Summary")
st.caption(":blue[Recordable (OSHA Recordable) refers to workplace injuries, illnesses, or incidents that meet specific criteria set forth by the Occupational Safety and Health Administration (OSHA) for recording and reporting purposes. OSHA requires employers to maintain records of work-related injuries and illnesses through the OSHA Form 300 Log of Work-Related Injuries and Illnesses.]")

df_safety['Date'] = pd.to_datetime(df_safety['Date'])
df_safety['Year'] = df_safety['Date'].dt.year.astype(int)
df_safety["Year"] = df_safety["Year"].astype(int).astype(str)
df_safety["Year"] = df_safety["Year"].str.replace(",", "")
df_grouped_recordable = df_safety[df_safety['Recordable'] == 'Y'].groupby('Year').size().reset_index(name='Recordables')
df_grouped_total = df_safety.groupby('Year').size().reset_index(name='Total Incidents')
df_combined = df_grouped_total.merge(df_grouped_recordable, how='left', on='Year').fillna(0)
st.dataframe(df_combined.set_index('Year'), use_container_width=False)

st.subheader("Data")

tabAll, tab2019, tab2020, tab2021, tab2022, tab2023, tab2024 =st.tabs(["All", "2019", "2020", "2021", "2022", "2023", "2024"])
df_2019 = df_safety[df_safety["Date"].dt.year == 2019]
df_2020 = df_safety[df_safety["Date"].dt.year == 2020]
df_2021 = df_safety[df_safety["Date"].dt.year == 2021]
df_2022 = df_safety[df_safety["Date"].dt.year == 2022]
df_2023 = df_safety[df_safety["Date"].dt.year == 2023]
df_2024 = df_safety[df_safety["Date"].dt.year == 2024]

with tabAll:
    st.dataframe(df_safety,use_container_width=True)
with tab2019:
    st.dataframe(df_2019,use_container_width=True)
with tab2020:
    st.dataframe(df_2020,use_container_width=True)
with tab2021:
    st.dataframe(df_2021,use_container_width=True)
with tab2022:
    st.dataframe(df_2022,use_container_width=True)
with tab2023:
    st.dataframe(df_2023,use_container_width=True)
with tab2024:
    st.dataframe(df_2024,use_container_width=True)