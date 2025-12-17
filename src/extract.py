import pandas as pd

def extract_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

if __name__ == "__main__":
    df = extract_data("data/raw/netflix_titles.csv")
    print("Loaded rows, cols:", df.shape)
    print(df.head(3))
