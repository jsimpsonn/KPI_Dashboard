from streamlit_extras.switch_page_button import switch_page
import streamlit as st
from sharepoint_manager import authenticate_user
from annotated_text import annotated_text
from streamlit_extras.bottom_container import bottom 

st.set_page_config(page_title="MSP KPI Dashboard", page_icon="assets/MSP_Favicon.png")

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
    # App Layout

    st.subheader('KPI Dashboard 📈')
    st.header('Mississippi Steel Processing', divider='blue')
    with st.expander("Where does this data come from?",expanded=False):
        st.info("Values in this dashboard are managed through a combination of CSV files and SharePoint data. While some data is still sourced from CSV files, efforts are underway to migrate all data retrieval to SharePoint. Please note that the information provided here may not be real-time. However, any updates made to the SharePoint data will be reflected in the dashboard.")

    annotated_text(
        "The ",("Key Performance Indicator", "KPI", "#dbede6"), " Dashboard provides a comprehensive overview of critical performance metrics across different departments or areas of MSP. It serves as a centralized platform for monitoring key performance indicators, allowing employees and stakeholders to assess the health and progress of various operations."
    )

    st.markdown("""
        :blue[Customer Concessions]<br>
        :blue[Customer Surveys]<br>
        :blue[Downtime]<br>
        :blue[Lead Times]<br>
        :blue[On-time Delivery]<br>
        :blue[Production]<br>
        :blue[Safety]<br>
        :blue[Shipping]<br>
        """,unsafe_allow_html=True)
