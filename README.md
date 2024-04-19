
<h2>Streamlit Project Summary</h2>
<h3>Description</h3>
<p>This Streamlit project is a dashboard for visualizing data related to Mississippi Steel Processing's quality management system. It provides insights into various aspects of steel production, including lead times, shipping, on-time delivery, production metrics, downtime analysis, and customer surveys.</p>
<h3>Features</h3>
<ul>
    <li><strong>Data Visualization:</strong> Utilizes interactive charts and graphs to display key performance indicators (KPIs) and metrics.</li>
    <li><strong>Data Analysis:</strong> Allows users to explore and analyze steel production data, including quality metrics, lead times, and customer feedback.</li>
    <li><strong>Dashboard Components:</strong> Includes separate sections for different data categories such as production, shipping, work orders, and customer surveys.</li>
    <li><strong>Downloadable Data:</strong> Provides options for users to download raw data files for further analysis.</li>
</ul>
<h3>Data Sources</h3>
<p>The project utilizes data from various sources, including CSV files containing production metrics, shipping records, work order information, and customer survey responses. Additionally, it interacts with the Office 365 SharePoint REST API to access real-time data.</p>
<h3>Dependencies</h3>
<ul>
    <li>Streamlit: The main framework for building the web application.</li>
    <li>Pandas: Used for data manipulation and analysis.</li>
    <li>Plotly: Utilized for creating interactive visualizations.</li>
    <li>Other standard Python libraries for data processing and visualization.</li>
</ul>
<h3>Usage</h3>
<p>To run the Streamlit application locally, follow these steps:</p>
<ol>
    <li>Clone the repository to your local machine.</li>
    <li>Install the required dependencies using <code>pip install -r requirements.txt</code>.</li>
    <li>Create a <code>secrets.toml</code> file inside the <code>.streamlit</code> folder in the project root directory.</li>
    <li>In the <code>secrets.toml</code> file, replace the <code>client_id</code> and <code>client_secret</code> with your own SharePoint credentials. Also, create your own keys for the SharePoint site URLs and list names.</li>
    <pre><code>[sharepoint]
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
main_site_url = "YOUR_HOME_SITE_URL
plant_operations_subsite_url = "YOUR_SUBSITE_URL"
loading_times_list_name = "YOUR_LOADING_TIMES_LIST_NAME"
lead_times_list_name = "YOUR_LEAD_TIMES_LIST_NAME"
customer_surveys_list_name = "YOUR_CUSTOMER_SURVEYS_LIST_NAME"
otd_list_name = "YOUR_OTD_LIST_NAME"
</code></pre>
    <li>Navigate to the project directory and run <code>streamlit run Home.py</code> in your terminal.</li>
    <li>Access the Streamlit dashboard in your web browser at <a href="http://localhost:8501">http://localhost:8501</a>.</li>
</ol>