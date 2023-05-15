import streamlit as st
import pandas as pd


# Add a title and intro text
st.title("Earthquake Data Explorer")
st.text("This is a web app to allow exploration of Earthquake Data")

# Add a sidebar
st.sidebar.title("Navigation")
# Add a section to the sidebar that allows for file upload
upload_file = st.sidebar.file_uploader("Upload a CSV file containing earthquake data", type="csv")

if upload_file is not None and st.session_state["file_uploaded"] is True:
    # Read file
    df = pd.read_csv(filepath_or_buffer=upload_file)
    st.session_state["dataframe"] = df
    st.header("Begin exploring the data using the menu on the left.")
else:
    st.header("To begin, upload a CSV file containing earthquake data.")
