from pathlib import Path

from src.load_data import load_all_tables
from src.transform import standardize_tables, build_final_table
from src.stockout_logic import (
    filter_stockout_events,
    get_stockout_table_by_ward,
    get_top_medications,
    get_top_wards,
)

PROCESSED_DATA_DIR = Path("data/processed")
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    tables = load_all_tables()
    tables = standardize_tables(tables)

    final_table = build_final_table(tables)
    final_table.to_csv(PROCESSED_DATA_DIR / "final_table.csv", index=False)

    stockout_df = filter_stockout_events(final_table)
    stockout_df.to_csv(PROCESSED_DATA_DIR / "stockout_events.csv", index=False)

    ward_summary_df = get_stockout_table_by_ward(stockout_df)
    ward_summary_df.to_csv(PROCESSED_DATA_DIR / "stockout_by_ward.csv", index=False)

    top_medications_df = get_top_medications(stockout_df)
    top_medications_df.to_csv(PROCESSED_DATA_DIR / "top_medications.csv", index=False)

    top_wards_df = get_top_wards(stockout_df)
    top_wards_df.to_csv(PROCESSED_DATA_DIR / "top_wards.csv", index=False)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
