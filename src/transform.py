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


def build_final_table(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:

    transaction = tables["transaction"][
        [
            "transaction_id",
            "datetime",
            "transaction_type",
            "hospital_id",
            "hospital_ward_id",
            "medication_id",
            "transaction_quantity",
            "quantity_on_hand",
        ]
    ]
    # transaction_type column has issues that need fixing from notebook knowledge
    transaction["transaction_type"] = transaction["transaction_type"].str.strip()
    transaction["transaction_type"].unique()

    transaction_type = tables["transaction_type"][
        ["transaction_type", "transaction_type_action"]
    ]
    # transaction_type column has issues that need fixing from notebook knowledge that needs fixing
    transaction_type["transaction_type"] = transaction_type[
        "transaction_type"
    ].str.strip()
    transaction_type["transaction_type"].unique()

    medication = tables["medication"][["medication_id", "medication"]]

    # machine = tables["machine"]

    hospital = tables["hospital"][["hospital_id", "hospital_name"]]

    hospital_ward = tables["hospital_ward"][["hospital_ward_id", "hospital_ward_name"]]

    # Join transaction → transaction type
    df = transaction.merge(transaction_type, on="transaction_type", how="left")

    # Join medication
    df = df.merge(medication, on="medication_id", how="left")

    # # Join machine
    # df = df.merge(machine, on="machine_id", how="left")

    # Join hospital
    df = df.merge(hospital, on="hospital_id", how="left")

    # Join ward
    df = df.merge(hospital_ward, on="hospital_ward_id", how="left")

    # Create a list of desired columns from the identified relevant columns
    desired_columns = [
        "transaction_id",
        "datetime",
        "transaction_type",
        "transaction_type_action",
        "transaction_quantity",
        "quantity_on_hand",
        "medication_id",
        "medication",
        "hospital_id",
        "hospital_name",
        "hospital_ward_id",
        "hospital_ward_name",
        # "machine_id",
        # "machine_identifier",
        # "machine_name",
        # "machine_type",
        # "hospital_id",
    ]

    df = df[desired_columns]

    ##### Further transformation from notebook logic ####
    # 1) Change data type of datetime column to datetime
    df["datetime"] = pd.to_datetime(df["datetime"].astype("str").str[:14])

    # 2) drop rows with year value of 1970 from the datetime column
    df = df.drop(df.loc[df["datetime"].dt.year == 1970].index)

    # 3) Change 2025 to 2022. This was a data input error
    df["datetime"] = pd.to_datetime(df["datetime"].dt.strftime("2022-%m-%d %H:%M:%S"))

    return df
