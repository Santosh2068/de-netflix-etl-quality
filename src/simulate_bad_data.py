import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/netflix_titles.csv")
BAD_PATH = Path("data/raw/netflix_titles_BAD.csv")

def make_bad_dataset():
    df = pd.read_csv(RAW_PATH)

    # 1) Introduce null titles (should fail CLEAN validation if not removed)
    df.loc[df.index[:5], "title"] = None

    # 2) Introduce unrealistic release years
    if "release_year" in df.columns and len(df) > 10:
        df.loc[df.index[5:10], "release_year"] = 1800

    # 3) Duplicate a show_id
    if "show_id" in df.columns and len(df) > 12:
        df.loc[df.index[10], "show_id"] = df.loc[df.index[11], "show_id"]

    df.to_csv(BAD_PATH, index=False)
    print(f"✅ Created bad dataset: {BAD_PATH}")

if __name__ == "__main__":
    make_bad_dataset()
