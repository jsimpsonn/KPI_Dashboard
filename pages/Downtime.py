import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", initial_sidebar_state="expanded", menu_items=None)

@st.cache_data(show_spinner=False)
def load_data():
    data_frames = []
    lines = ['stamco', 'redbud', 'braner']
    types = ['mr', 'nmr']
    for line in lines:
        for dtype in types:
            temp_df = pd.read_csv(f'data/downtime/{line}/{line}_{dtype}.csv')
            category_col = 'MAINTENANCE RELATED' if dtype == 'mr' else 'NON MAINTENANCE RELATED'
            temp_df = temp_df.rename(columns={category_col: 'Category'})
            temp_df = temp_df[temp_df['Category'] != 'TOTALS']
            temp_df['Line'] = line.capitalize()
            temp_df['Maintenance Status'] = 'Maintenance Related' if dtype == 'mr' else 'Non-Maintenance Related'
            data_frames.append(temp_df)
    combined_data = pd.concat(data_frames, ignore_index=True)
    return combined_data

def main():
    st.header("Downtime Analysis by Production Line")
    combined_data = load_data()

    line_options = ['All Lines', 'Stamco', 'Redbud', 'Braner']
    selected_line = st.selectbox("Select the production line to display:", line_options, key="line_select")

    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC']
    selected_months = st.multiselect('Select months for the treemap:', months, default=['JAN', 'FEB', 'MAR', 'APR'], key="month_select")

    color_scale = px.colors.sequential.RdBu_r

    # Filter data based on selections
    filtered_data = combined_data.copy()
    if selected_line != 'All Lines':
        filtered_data = filtered_data[filtered_data['Line'] == selected_line]

    for month in selected_months:
        if month not in filtered_data.columns:
            continue
        month_data = filtered_data.melt(id_vars=['Category', 'Line', 'Maintenance Status'], value_vars=[month],
                                        var_name='Month', value_name='Downtime')
        month_data = month_data[month_data['Downtime'] != 0]  # Filter out zero downtime entries

        if month_data.empty:
            st.write(f"No downtime data available for {month}.")
            continue

        fig_treemap = px.treemap(month_data, path=['Line', 'Maintenance Status', 'Category'] if selected_line == 'All Lines' else ['Maintenance Status', 'Category'],
                                 values='Downtime', title=f"{month} Downtime - {selected_line}",
                                 color='Downtime', color_continuous_scale=color_scale)
        fig_treemap.update_layout(margin=dict(t=50, l=25, r=25, b=25), plot_bgcolor='rgba(0,0,0,0)')
        fig_treemap.update_traces(marker=dict(cornerradius=5))

        st.plotly_chart(fig_treemap, use_container_width=True)

main()
