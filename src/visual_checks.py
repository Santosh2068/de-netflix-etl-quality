import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PLOTS_DIR = Path("outputs/plots")

def save_plots(df: pd.DataFrame) -> None:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    # Ensure date_added is datetime for time plots
    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

    # 1) Movies vs TV Shows (bar)
    if "type" in df.columns:
        plt.figure()
        df["type"].value_counts().plot(kind="bar", title="Movies vs TV Shows")
        plt.savefig(PLOTS_DIR / "type_counts.png", dpi=150, bbox_inches="tight")
        plt.close()

    # 2) Release year distribution (hist)
    if "release_year" in df.columns:
        plt.figure()
        df["release_year"].plot(kind="hist", bins=30, title="Release Year Distribution")
        plt.savefig(PLOTS_DIR / "release_year_hist.png", dpi=150, bbox_inches="tight")
        plt.close()

    # 3) Titles added per year (line)
    if "date_added" in df.columns and "show_id" in df.columns:
        tmp = df.dropna(subset=["date_added"]).copy()
        if not tmp.empty:
            by_year = tmp.groupby(tmp["date_added"].dt.year)["show_id"].count()
            plt.figure()
            by_year.plot(kind="line", title="Titles Added by Year (date_added)")
            plt.savefig(PLOTS_DIR / "titles_added_by_year.png", dpi=150, bbox_inches="tight")
            plt.close()

if __name__ == "__main__":
    df = pd.read_csv("data/cleaned/netflix_cleaned.csv")
    save_plots(df)
    print("✅ Saved plots to outputs/plots/")
