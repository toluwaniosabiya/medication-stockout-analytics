import pandas as pd
import streamlit as st
import plotly.express as px
from src.stockout_logic import (
    get_overview_metrics,
    get_top_medications,
    get_top_wards,
    get_stockout_table_by_ward,
)
from src.stockout_logic import get_overview_metrics

st.set_page_config(page_title="Medication Stockout Analytics", layout="wide")

st.title("Dynamic Medication Stockout Analytics and Visualisation")
st.subheader(
    "Identify medications that stock out the most and the wards where they occur most often"
)

# Load processed data
final_table = pd.read_csv("data/processed/final_table.csv")
stockout_df = pd.read_csv("data/processed/stockout_events.csv")

# Overview metrics
metrics = get_overview_metrics(stockout_df)

col1, col2, col3 = st.columns(
    3,
)

col1.metric("Total Stockout Events", metrics["total_stockout_events"])
col2.metric("Affected Wards", metrics["affected_wards"])
col3.metric("Affected Medications", metrics["affected_medications"])

top_medications = get_top_medications(stockout_df)
top_wards = get_top_wards(stockout_df)

col4, col5 = st.columns(2)

with col4:
    fig_medications = px.bar(
        top_medications.sort_values("count", ascending=True),
        x="count",
        y="medication",
        orientation="h",
        title="Top Medications Stocking Out",
        template="plotly_white",
    )

    fig_medications.update_xaxes(showline=True, linewidth=2, linecolor="black")

    # fig_medications.update_yaxes(
    #     showline=True,
    #     linewidth=2,
    #     linecolor="black"
    # )

    fig_medications.update_layout(
        xaxis_title="Stockout Frequency", yaxis_title="Medication"
    )

    st.plotly_chart(fig_medications, use_container_width=True)

with col5:
    fig_wards = px.bar(
        top_wards.sort_values("count", ascending=True),
        x="count",
        y="hospital_ward_name",
        orientation="h",
        title="Hospital Wards With Most Stockout Occurrences",
        template="plotly_white",
    )

    fig_wards.update_xaxes(showline=True, linewidth=2, linecolor="black")

    # fig_wards.update_yaxes(
    #     showline=True,
    #     linewidth=2,
    #     linecolor="black"
    # )

    fig_wards.update_layout(xaxis_title="Stockout Frequency", yaxis_title="Ward")

    st.plotly_chart(fig_wards, use_container_width=True)

st.markdown("## Stockout by Ward")

ward_summary_df = get_stockout_table_by_ward(stockout_df)

selected_ward = st.selectbox(
    "Select a ward", options=sorted(ward_summary_df["hospital_ward_name"].unique())
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
        fig_selected_ward = px.bar(
            filtered_ward_df.sort_values("Stockout Count", ascending=True),
            x="Stockout Count",
            y="Medication",
            orientation="h",
            title=f"Medications Stocking Out in {selected_ward}",
            template="plotly_white",
        )

        fig_selected_ward.update_xaxes(showline=True, linewidth=2, linecolor="black")

        # fig_selected_ward.update_yaxes(
        #     showline=True,
        #     linewidth=2,
        #     linecolor="black"
        # )

        fig_selected_ward.update_layout(
            xaxis_title="Stockout Frequency", yaxis_title="Medication"
        )

        st.plotly_chart(fig_selected_ward, use_container_width=True)
else:
    st.dataframe(filtered_ward_df, use_container_width=True, hide_index=True)
