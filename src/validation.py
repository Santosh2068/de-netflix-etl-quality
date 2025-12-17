import pandas as pd

REQUIRED_COLUMNS = [
    "show_id", "type", "title", "date_added", "release_year"
]

def validate_data(df: pd.DataFrame) -> dict:
    report = {}

    # Schema check
    report["missing_required_columns"] = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    # Basic row checks
    report["row_count"] = int(len(df))
    report["duplicate_show_id"] = int(df["show_id"].duplicated().sum()) if "show_id" in df.columns else None
    report["null_title"] = int(df["title"].isnull().sum()) if "title" in df.columns else None

    # Range check (release_year should look realistic)
    if "release_year" in df.columns:
        bad_years = df[(df["release_year"] < 1900) | (df["release_year"] > 2030)]
        report["invalid_release_year"] = int(len(bad_years))
    else:
        report["invalid_release_year"] = None

    # Overall status
    report["status"] = "PASS"
    if report["missing_required_columns"]:
        report["status"] = "FAIL (missing required columns)"
    elif report["row_count"] == 0:
        report["status"] = "FAIL (no rows)"
    elif report["null_title"] and report["null_title"] > 0:
        report["status"] = "FAIL (null titles)"
    elif report["duplicate_show_id"] and report["duplicate_show_id"] > 0:
        report["status"] = "FAIL (duplicate show_id)"
    elif report["invalid_release_year"] and report["invalid_release_year"] > 0:
        report["status"] = "FAIL (invalid release_year values)"

    return report


if __name__ == "__main__":
    df = pd.read_csv("data/raw/netflix_titles.csv")
    report = validate_data(df)
    for k, v in report.items():
        print(f"{k}: {v}")
