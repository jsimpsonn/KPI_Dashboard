import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client

st.set_page_config(layout="wide", initial_sidebar_state="expanded", menu_items=None)

@st.cache_resource
def init_supabase_connection():
    url = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
    key = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase_connection()

@st.cache_data(ttl=600, show_spinner=False)
def load_data():
    tables = {
        "Braner Maintenance Related Downtime": ("Braner", "Maintenance Related"),
        "Braner Non-Maintenance Related Downtime": ("Braner", "Non-Maintenance Related"),
        "Red Bud Maintenance Related Downtime": ("Red Bud", "Maintenance Related"),
        "Red Bud Non-Maintenance Related Downtime": ("Red Bud", "Non-Maintenance Related"),
        "Stamco Maintenance Related Downtime": ("Stamco", "Maintenance Related"),
        "Stamco Non-Maintenance Related Downtime": ("Stamco", "Non-Maintenance Related")
    }
    
    data_frames = []
    
    for table_name, (line, category) in tables.items():
        try:
            response = supabase.table(table_name).select("*").execute()
            if response.data:
                temp_df = pd.DataFrame(response.data)
                temp_df['Line'] = line
                temp_df['Category'] = category
                data_frames.append(temp_df)
            else:
                st.write(f"No data found for table: {table_name}")
        except Exception as e:
            st.error(f"An error occurred while fetching data from {table_name}: {e}")
    
    if data_frames:
        combined_data = pd.concat(data_frames, ignore_index=True)
        return combined_data
    else:
        return pd.DataFrame()

def main():
    st.header("Downtime Treemap")
    combined_data = load_data()

    if combined_data.empty:
        st.error("No data available.")
        return

    line_options = ['All Lines', 'Stamco', 'Red Bud', 'Braner']
    selected_line = st.selectbox("Select the production line to display:", line_options, key="line_select")

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    selected_months = st.multiselect('Select months for the treemap:', months, default=['January', 'February', 'March', 'April'], key="month_select")

    color_scale = px.colors.sequential.RdBu_r

    # Filter data based on selections
    filtered_data = combined_data.copy()
    if selected_line != 'All Lines':
        filtered_data = filtered_data[filtered_data['Line'] == selected_line]

    for month in selected_months:
        if month not in filtered_data.columns:
            continue
        month_data = filtered_data.melt(id_vars=['Reason', 'Category', 'Line'], value_vars=[month],
                                        var_name='Month', value_name='Downtime')
        month_data = month_data[month_data['Downtime'] != 0]  # Filter out zero downtime entries

        if month_data.empty:
            st.write(f"No downtime data available for {month}.")
            continue

        fig_treemap = px.treemap(month_data, path=['Line', 'Category', 'Reason'] if selected_line == 'All Lines' else ['Category', 'Reason'],
                                 values='Downtime', title=f"{month} Downtime - {selected_line}",
                                 color='Downtime', color_continuous_scale=color_scale)
        fig_treemap.update_layout(margin=dict(t=50, l=25, r=25, b=25), plot_bgcolor='rgba(0,0,0,0)')
        fig_treemap.update_traces(marker=dict(cornerradius=5))

        st.plotly_chart(fig_treemap, use_container_width=True)

main()
