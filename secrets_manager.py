import os
import toml
import streamlit as st

def read_secrets():
    if "STREAMLIT_SERVER_ADDRESS" in os.environ:
        # Running on Streamlit Sharing
        return st.secrets["sharepoint"]
    else:
        # Running locally
        streamlit_home = os.environ.get("STREAMLIT_HOME", "")
        secrets_path = os.path.join(streamlit_home, ".streamlit", "secrets.toml")
        return toml.load(secrets_path)["sharepoint"]
