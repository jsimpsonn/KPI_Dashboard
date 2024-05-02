import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", initial_sidebar_state="auto", menu_items=None)

def load_data():
    # Load maintenance and non-maintenance data from separate CSV files
    maintenance_data = pd.read_csv('data/downtime/rb_mr.csv')
    non_maintenance_data = pd.read_csv('data/downtime/rb_nmr.csv')

    # Exclude rows where the category is 'TOTALS'
    category_data_mr = maintenance_data[maintenance_data['MAINTENANCE RELATED'] != 'TOTALS']
    category_data_nmr = non_maintenance_data[non_maintenance_data['NON MAINTENANCE RELATED'] != 'TOTALS']

    return category_data_mr, category_data_nmr

def main():
    st.header("Stamco Downtime")
    category_data_mr, category_data_nmr = load_data()

    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC']
    selected_months = st.multiselect('Select months for the treemap:', months, default=['JAN', 'FEB', 'MAR', 'APR'])

    color_scale = px.colors.sequential.RdBu_r

    for month in selected_months:
        # Prepare data for maintenance related downtime
        treemap_data_mr = category_data_mr.melt(id_vars=['MAINTENANCE RELATED'], value_vars=[month], 
                                                var_name='Month', value_name='Downtime')
        treemap_data_mr = treemap_data_mr.rename(columns={'MAINTENANCE RELATED': 'Category'})
        treemap_data_mr['Maintenance Status'] = 'Maintenance Related'

        # Prepare data for non-maintenance related downtime
        treemap_data_nmr = category_data_nmr.melt(id_vars=['NON MAINTENANCE RELATED'], value_vars=[month], 
                                                  var_name='Month', value_name='Downtime')
        treemap_data_nmr = treemap_data_nmr.rename(columns={'NON MAINTENANCE RELATED': 'Category'})
        treemap_data_nmr['Maintenance Status'] = 'Non-Maintenance Related'

        # Combine both datasets
        treemap_data = pd.concat([treemap_data_mr, treemap_data_nmr])
        treemap_data = treemap_data[treemap_data['Downtime'] != 0]  # Filter out zero downtime entries

        # Generate the treemap
        fig_treemap = px.treemap(treemap_data, path=['Maintenance Status', 'Category'], values='Downtime',
                                 title=month, color='Downtime', color_continuous_scale=color_scale)
        fig_treemap.update_layout(uniformtext=dict(minsize=10, mode='show'), margin=dict(t=50, l=25, r=25, b=25),
                                  plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_treemap, use_container_width=True)

if __name__ == "__main__":
    main()
