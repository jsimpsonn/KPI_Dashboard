import os
import toml

def read_secrets():
    if "streamlit" in os.environ.get("SERVER_SOFTWARE", ""):
        # Running on Streamlit Sharing
        return toml.load("secrets.toml")["sharepoint"]
    else:
        # Running locally
        return toml.load("secrets.toml")["sharepoint"]