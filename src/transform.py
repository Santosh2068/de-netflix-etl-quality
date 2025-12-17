import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    # 1) Drop rows with missing title (title is essential)
    df = df.dropna(subset=["title"])

    # 2) Convert date_added to datetime (invalid becomes NaT)
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

    # 3) Fix unrealistic release_year: set invalid to NA then drop
    df.loc[(df["release_year"] < 1900) | (df["release_year"] > 2030), "release_year"] = pd.NA
    df = df.dropna(subset=["release_year"])
    df["release_year"] = df["release_year"].astype(int)

    # 4) Remove duplicate show_id (keep first)
    df = df.drop_duplicates(subset=["show_id"], keep="first")

    # 5) Fill optional text columns
    for col in ["director", "cast", "country", "rating", "duration", "listed_in", "description"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df
