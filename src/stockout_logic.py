import pandas as pd

# Per notebook logic, some transactions are excluded from counting towards stockout
# because they do not truly represent a stockout situation
EXCLUDED_TRANSACTION_TYPES = {
    "Return",
    "Waste",
    "Null",
    "Destock",
    "Expired",
    "Receive",
}


def filter_stockout_events(df: pd.DataFrame) -> pd.DataFrame:
    stockout_df = df.copy()

    stockout_df = stockout_df[stockout_df["quantity_on_hand"] == 0]

    stockout_df = stockout_df[
        ~stockout_df["transaction_type_action"].isin(EXCLUDED_TRANSACTION_TYPES)
    ]

    return stockout_df


def get_stockout_table_by_ward(stockout_df: pd.DataFrame) -> pd.DataFrame:
    summary_df = (
        stockout_df.groupby(["hospital_ward_name", "medication"])["transaction_id"]
        .count()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
    )

    return summary_df
