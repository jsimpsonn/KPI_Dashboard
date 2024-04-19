import os
import streamlit as st
import toml

def read_secrets():
    if os.getenv("STREAMLIT_PRODUCTION") == "true":
        # Running on Streamlit Sharing
        return st.secrets["sharepoint"]
    else:
        # Running locally
        try:
            return toml.load("secrets.toml")["sharepoint"]
        except FileNotFoundError:
            st.error("Secrets file not found. Please make sure you have a 'secrets.toml' file in your project directory.")
            return {}