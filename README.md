<h2>Streamlit Project Summary</h2>
<h3>Description</h3>
<p>This Streamlit project is a dashboard designed to visualize data related to Mississippi Steel Processing's quality management system. It offers insights into various aspects of steel production, including lead times, shipping, on-time delivery, production metrics, downtime analysis, and customer surveys.</p>
<h3>Features</h3>
<ul>
    <li><strong>Data Visualization:</strong> Interactive charts and graphs display key performance indicators (KPIs) and metrics.</li>
    <li><strong>Data Analysis:</strong> Users can explore and analyze steel production data, including quality metrics, lead times, and customer feedback.</li>
    <li><strong>Dashboard Components:</strong> Separate sections for different data categories such as production, shipping, work orders, and customer surveys.</li>
    <li><strong>Downloadable Data:</strong> Options for users to download raw data files for further analysis.</li>
</ul>
<h3>Data Sources</h3>
<p>The project utilizes data from various sources, including:</p>
<ul>
    <li><strong>Office 365 SharePoint REST API:</strong> Integrates with SharePoint to access live data on lead times, shipping, work order on-time delivery, and customer survey responses.</li>
    <li><strong>CSV Files:</strong> Additional data sources include CSV files containing production metrics, downtime, and safety incidents.</li>
</ul>
<h3>Dependencies</h3>
<ul>
    <li>Streamlit: Main framework for building the web application.</li>
    <li>Pandas: Used for data manipulation and analysis.</li>
    <li>Plotly: Utilized for creating interactive visualizations.</li>
    <li>Other standard Python libraries for data processing and visualization.</li>
</ul>
<h3>Usage</h3>
<p>To run the Streamlit application locally, follow these steps:</p>
<ol>
    <li>Clone the repository to your local machine.</li>
    <li>Install the required dependencies using <code>pip install -r requirements.txt</code>.</li>
    <li>Navigate to the project directory and run <code>streamlit run Home.py</code> in your terminal.</li>
    <li>Access the Streamlit dashboard in your web browser at <a href="http://localhost:8501">http://localhost:8501</a>.</li>
</ol>
<h3>Recent Updates (April 19, 2024)</h3>
<ul>
    <li>Added modules for SharePoint integration: <code>sharepoint_manager.py</code>.</li>
    <li>Introduced functions for retrieving SharePoint list items and managing SharePoint secrets.</li>
    <li>Utilized the <code>AuthenticationContext</code> and <code>ClientContext</code> modules for authentication.</li>
    <li>Imported functions <code>get_sharepoint_list_items</code>, <code>sharepoint_urls</code>, <code>sharepoint_lists</code>, and <code>read_secrets</code> from <code>sharepoint_manager.py</code>.</li>
</ul>