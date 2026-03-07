import pandas as pd
import streamlit as st

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

col1, col2, col3 = st.columns(3)

col1.metric("Total Stockout Events", metrics["total_stockout_events"])
col2.metric("Affected Wards", metrics["affected_wards"])
col3.metric("Affected Medications", metrics["affected_medications"])

# Preview data
st.markdown("### Stockout Events Preview")
st.dataframe(stockout_df.head(20), use_container_width=True)
