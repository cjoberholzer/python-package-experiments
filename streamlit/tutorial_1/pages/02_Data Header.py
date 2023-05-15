import streamlit as st
import pandas as pd


def data_header(dataframe: pd.DataFrame) -> None:
    """
    Display the dataframe header
    :param dataframe: Pandas dataframe
    :return: None
    """
    st.header("Dataframe header")
    st.write(dataframe.head())


try:
    df = st.session_state["dataframe"]
    data_header(dataframe=df)
except KeyError:
    st.error("Please upload a file first")

