import streamlit as st
import pandas as pd
import plotly.express as px


def interactive_plot(dataframe: pd.DataFrame) -> None:
    """
    Display an interactive plot of the dataframe
    :param dataframe: Pandas dataframe
    :return: None
    """
    col_1, col_2 = st.columns(2)

    x_axis_val = col_1.selectbox("Select X-Axis Value", options=list(dataframe.columns), index=5)
    y_axis_val = col_2.selectbox("Select Y-Axis Value", options=list(dataframe.columns), index=8)
    color = st.color_picker("Select a Plot Color", value="#4577C3")

    plot = px.scatter(dataframe, x=x_axis_val, y=y_axis_val)
    plot.update_traces(marker=dict(color=color))
    st.plotly_chart(plot, use_container_width=True)


try:
    df = st.session_state["dataframe"]
    interactive_plot(dataframe=df)
except KeyError:
    st.error("Please upload a file first")
