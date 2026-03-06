from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path("data/raw")


def load_csv(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)


def load_all_tables() -> dict[str, pd.DataFrame]:
    tables = {}
    for file_path in RAW_DATA_DIR.glob("*.csv"):
        tables[file_path.stem] = load_csv(file_path)
    return tables
