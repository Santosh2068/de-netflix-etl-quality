import pandas as pd

def load_data(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)

if __name__ == "__main__":
    df = pd.read_csv("data/raw/netflix_titles.csv")
    load_data(df, "data/cleaned/netflix_cleaned.csv")
    print("Saved to data/cleaned/netflix_cleaned.csv")
