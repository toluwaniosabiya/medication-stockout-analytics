import plotly.express as px
import pandas as pd


def plot_top_medications(top_medications: pd.DataFrame):
    fig = px.bar(
        top_medications.sort_values("count", ascending=True),
        x="count",
        y="medication",
        orientation="h",
        title="Top Medications Stocking Out",
        template="plotly_white",
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor="black")
    fig.update_layout(
        xaxis_title="Stockout Frequency",
        yaxis_title="Medication",
    )

    return fig


def plot_top_wards(top_wards: pd.DataFrame):
    fig = px.bar(
        top_wards.sort_values("count", ascending=True),
        x="count",
        y="hospital_ward_name",
        orientation="h",
        title="Hospital Wards With Most Stockout Occurrences",
        template="plotly_white",
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor="black")
    fig.update_layout(
        xaxis_title="Stockout Frequency",
        yaxis_title="Ward",
    )

    return fig


def plot_selected_ward(filtered_ward_df: pd.DataFrame, selected_ward: str):
    fig = px.bar(
        filtered_ward_df.sort_values("Stockout Count", ascending=True),
        x="Stockout Count",
        y="Medication",
        orientation="h",
        title=f"Medications Stocking Out in {selected_ward}",
        template="plotly_white",
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor="black")
    fig.update_layout(
        xaxis_title="Stockout Frequency",
        yaxis_title="Medication",
    )

    return fig
