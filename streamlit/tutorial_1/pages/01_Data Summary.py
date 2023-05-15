import streamlit as st
import pandas as pd


def data_statistics(dataframe: pd.DataFrame) -> None:
    """
    Display statistics of the dataframe
    :param dataframe: Pandas dataframe
    :return: None
    """
    st.header("Dataframe statistics")
    st.write(dataframe.describe())


try:
    df = st.session_state["dataframe"]
    data_statistics(dataframe=df)
except KeyError:
    st.error("Please upload a file first")
