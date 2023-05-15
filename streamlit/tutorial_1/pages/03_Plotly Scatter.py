import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def data_plot(dataframe: pd.DataFrame) -> None:
    """
    Display a plot of the dataframe
    :param dataframe: Pandas dataframe
    :return: None
    """
    fig, ax = plt.subplots(1, 1)

    ax.scatter(x=dataframe['Depth'], y=dataframe['Magnitude'])
    ax.set_xlabel('Depth')
    ax.set_ylabel('Magnitude')

    st.header("Plot of Data")
    st.pyplot(fig)

try:
    df = st.session_state["dataframe"]
    data_plot(dataframe=df)
except KeyError:
    st.error("Please upload a file first")
