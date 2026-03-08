import pandas as pd
import streamlit as st
import plotly.express as px

from src.stockout_logic import (
    get_overview_metrics,
    get_top_medications,
    get_top_wards,
    get_stockout_table_by_ward,
)
from src.plots import plot_top_medications, plot_top_wards, plot_selected_ward

st.set_page_config(page_title="Medication Stockout Analytics", layout="wide")

st.title("Medication Stockout Analytics Dashboard")
st.caption(
    "Interactive analytics for identifying medications that stock out most frequently and the hospital wards where stockout events are concentrated."
)
st.info(
    "User Story: Provide a dynamic overview of medications experiencing stockouts across hospitals and identify the specific wards where these stockouts occur."
)

st.divider()
# Load processed data
final_table = pd.read_csv("data/processed/final_table.csv")
stockout_df = pd.read_csv("data/processed/stockout_events.csv")

# Overview metrics
metrics = get_overview_metrics(stockout_df)

st.write("")
kpi_container = st.container(border=True)
with kpi_container:
    st.markdown("### Overview")
    col1, col2, col3 = st.columns(
        3,
    )

    col1.metric("Total Stockout Events", metrics["total_stockout_events"], border=True)
    col2.metric("Affected Wards", metrics["affected_wards"], border=True)
    col3.metric("Affected Medications", metrics["affected_medications"], border=True)

st.divider()
st.write("")
st.write("")
med_ward_container = st.container(border=True)
with med_ward_container:
    st.markdown("### Stockout Trends")
    top_medications = get_top_medications(stockout_df)
    top_wards = get_top_wards(stockout_df)

    col4, col5 = st.columns(2)

    with col4:
        st.plotly_chart(plot_top_medications(top_medications), use_container_width=True)

    with col5:
        st.plotly_chart(plot_top_wards(top_wards), use_container_width=True)

st.divider()
st.write("")
st.write("")
stockout_by_ward_container = st.container(border=True)
with stockout_by_ward_container:
    st.markdown("## Stockout by Ward")

    ward_summary_df = get_stockout_table_by_ward(stockout_df)

    selected_ward = st.selectbox(
        "Select a ward", options=sorted(final_table["hospital_ward_name"].unique())
    )

    filtered_ward_df = ward_summary_df[
        ward_summary_df["hospital_ward_name"] == selected_ward
    ].sort_values(by="count", ascending=False)
    filtered_ward_df = filtered_ward_df.drop(columns="hospital_ward_name").rename(
        columns={"count": "Stockout Count", "medication": "Medication"}
    )
    col6, col7 = st.columns(2)

    if len(filtered_ward_df) > 1:
        with col6:
            st.dataframe(filtered_ward_df, use_container_width=True, hide_index=True)

        with col7:
            st.plotly_chart(
                plot_selected_ward(filtered_ward_df, selected_ward),
                use_container_width=True,
            )
    elif len(filtered_ward_df) == 1:
        st.dataframe(filtered_ward_df, use_container_width=True, hide_index=True)

    else:
        st.markdown("##### No stockouts recorded for this ward!")
