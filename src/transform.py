import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Standardize column names (optional but professional)
    df.columns = [c.strip() for c in df.columns]

    # Convert date_added (string -> datetime)
    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

    # Fill common nulls with "Unknown" (keeps rows usable)
    for col in ["director", "cast", "country", "rating", "duration"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Drop rows where title is missing (title is essential)
    if "title" in df.columns:
        df = df.dropna(subset=["title"])

    # Remove duplicate IDs (keep first)
    if "show_id" in df.columns:
        df = df.drop_duplicates(subset=["show_id"], keep="first")

    return df


if __name__ == "__main__":
    df = pd.read_csv("data/raw/netflix_titles.csv")
    out = transform_data(df)
    print("After transform:", out.shape)
    print(out.head(3))
