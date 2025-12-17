import pandas as pd

REQUIRED_COLUMNS = ["show_id", "type", "title", "date_added", "release_year"]

def validate_raw(df: pd.DataFrame) -> dict:
    """
    Raw-data validation: schema + basic sanity checks.
    Do NOT fail on messy-but-fixable issues like null title yet.
    """
    report = {}
    report["row_count"] = int(len(df))
    report["missing_required_columns"] = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    # Only report these issues in raw, do not fail yet
    report["duplicate_show_id"] = int(df["show_id"].duplicated().sum()) if "show_id" in df.columns else 0
    report["null_title"] = int(df["title"].isnull().sum()) if "title" in df.columns else 0

    if "release_year" in df.columns:
        bad_years = df[(df["release_year"] < 1900) | (df["release_year"] > 2030)]
        report["invalid_release_year"] = int(len(bad_years))
    else:
        report["invalid_release_year"] = 0

    report["status"] = "PASS"
    if report["row_count"] == 0:
        report["status"] = "FAIL (no rows)"
    if report["missing_required_columns"]:
        report["status"] = "FAIL (missing required columns)"
        
        # Threshold rule: if too many null titles, stop early (example threshold)
    null_title_rate = report["null_title"] / report["row_count"] if report["row_count"] else 0
    report["null_title_rate"] = round(null_title_rate, 6)

    if null_title_rate > 0.0005:  # ~0.05% (tweak as you like)
        report["status"] = "FAIL (raw title null rate too high)"


    return report


def validate_clean(df: pd.DataFrame) -> dict:
    """
    Clean-data validation: now we enforce strict rules.
    """
    report = {}
    report["row_count"] = int(len(df))

    report["duplicate_show_id"] = int(df["show_id"].duplicated().sum())
    report["null_title"] = int(df["title"].isnull().sum())
    report["invalid_release_year"] = int(((df["release_year"] < 1900) | (df["release_year"] > 2030)).sum())

    report["status"] = "PASS"
    if report["row_count"] == 0:
        report["status"] = "FAIL (no rows after cleaning)"
    elif report["null_title"] > 0:
        report["status"] = "FAIL (null titles after cleaning)"
    elif report["duplicate_show_id"] > 0:
        report["status"] = "FAIL (duplicate show_id after cleaning)"
    elif report["invalid_release_year"] > 0:
        report["status"] = "FAIL (invalid release_year after cleaning)"

    return report


if __name__ == "__main__":
    df = pd.read_csv("data/raw/netflix_titles.csv")
    print("RAW REPORT:", validate_raw(df))
