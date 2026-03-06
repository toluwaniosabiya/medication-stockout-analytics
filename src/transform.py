import pandas as pd


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w]", "", regex=True)
    )

    return df


def standardize_tables(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    standardized_tables = {}

    for name, df in tables.items():
        standardized_tables[name] = standardize_column_names(df)

    return standardized_tables
