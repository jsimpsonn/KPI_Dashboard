import os
import toml
import streamlit as st

def read_secrets():
    if "streamlit" in os.environ.get("SERVER_SOFTWARE", ""):
        # Running on Streamlit Sharing
        return st.secrets["sharepoint"]
    else:
        # Running locally
        return toml.load("secrets.toml")["sharepoint"]