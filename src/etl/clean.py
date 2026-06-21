"""
Project Meridian - Data Cleaning Script
Reads raw Online Retail II data, applies cleaning rules,
and saves two analysis-ready datasets to data/processed/.
"""

import pandas as pd

RAW_PATH = "data/raw/online_retail_II.xlsx"
FULL_OUTPUT_PATH = "data/processed/sales_clean_full.csv"
CUSTOMER_OUTPUT_PATH = "data/processed/sales_clean_customer_level.csv"


def load_raw_data(path: str) -> pd.DataFrame:
    sheet1 = pd.read_excel(path, sheet_name="Year 2009-2010")
    sheet2 = pd.read_excel(path, sheet_name="Year 2010-2011")
    return pd.concat([sheet1, sheet2], ignore_index=True)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    df_clean = df_clean.drop_duplicates()

    df_clean["is_cancelled"] = df_clean["Invoice"].astype(str).str.startswith("C")

    df_clean = df_clean[df_clean["Price"] > 0]

    df_clean = df_clean[
        ~((df_clean["Quantity"] <= 0) & (~df_clean["is_cancelled"]))
    ]

    df_clean["Description"] = df_clean["Description"].fillna("Unknown")
    df_clean["TotalPrice"] = df_clean["Quantity"] * df_clean["Price"]

    return df_clean


def split_customer_level(df_clean: pd.DataFrame) -> pd.DataFrame:
    return df_clean[df_clean["Customer ID"].notnull()].copy()


def main():
    print("Loading raw data...")
    df = load_raw_data(RAW_PATH)
    print(f"Raw rows loaded: {len(df)}")

    print("Cleaning data...")
    df_clean = clean_data(df)
    print(f"Rows after cleaning: {len(df_clean)}")

    df_customer_level = split_customer_level(df_clean)
    print(f"Customer-level rows: {len(df_customer_level)}")

    df_clean.to_csv(FULL_OUTPUT_PATH, index=False)
    df_customer_level.to_csv(CUSTOMER_OUTPUT_PATH, index=False)
    print("Saved cleaned datasets to data/processed/")


if __name__ == "__main__":
    main()