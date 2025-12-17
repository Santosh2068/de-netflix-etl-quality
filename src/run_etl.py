from extract import extract_data
from validation import validate_data
from transform import transform_data
from load import load_data

RAW_PATH = "data/raw/netflix_titles.csv"
CLEAN_PATH = "data/cleaned/netflix_cleaned.csv"

def main():
    print("1) Extract")
    df_raw = extract_data(RAW_PATH)
    print("   shape:", df_raw.shape)

    print("2) Validate")
    report = validate_data(df_raw)
    for k, v in report.items():
        print(f"   {k}: {v}")

    if not str(report.get("status", "")).startswith("PASS"):
        raise SystemExit(f"❌ Pipeline stopped: {report['status']}")

    print("3) Transform")
    df_clean = transform_data(df_raw)
    print("   shape:", df_clean.shape)

    print("4) Load")
    load_data(df_clean, CLEAN_PATH)
    print(f"   saved: {CLEAN_PATH}")

    print("✅ Day 2 ETL completed")

if __name__ == "__main__":
    main()
