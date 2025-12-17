import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/netflix_titles_BAD.csv")
BAD_PATH = Path("data/raw/netflix_titles_BAD.csv")

def make_bad_dataset():
    df = pd.read_csv(RAW_PATH)

    # 1) Introduce null titles (should FAIL)
    df.loc[df.index[:5], "title"] = None

    # 2) Introduce unrealistic release years (should FAIL)
    if "release_year" in df.columns:
        df.loc[df.index[5:10], "release_year"] = 1800

    # 3) Duplicate show_id (should FAIL schema/uniqueness)
    if "show_id" in df.columns and len(df) > 2:
        df.loc[df.index[10], "show_id"] = df.loc[df.index[11], "show_id"]

    df.to_csv(BAD_PATH, index=False)
    print(f"Created bad dataset: {BAD_PATH}")

if __name__ == "__main__":
    make_bad_dataset()
