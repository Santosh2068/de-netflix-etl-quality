import sys
from extract import extract_data
from validation import validate_raw, validate_clean
from transform import transform_data
from load import load_data
from visual_checks import save_plots

DEFAULT_RAW = "data/raw/netflix_titles.csv"
CLEAN_PATH = "data/cleaned/netflix_cleaned.csv"

def main():
    raw_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RAW

    print("1) Extract")
    df_raw = extract_data(raw_path)
    print("   raw_path:", raw_path)
    print("   shape:", df_raw.shape)

    print("2) Validate RAW (schema/sanity)")
    raw_report = validate_raw(df_raw)
    for k, v in raw_report.items():
        print(f"   {k}: {v}")

    if not str(raw_report.get("status", "")).startswith("PASS"):
        raise SystemExit(f"❌ RAW validation failed: {raw_report['status']}")

    print("3) Transform (clean)")
    df_clean = transform_data(df_raw)
    print("   shape:", df_clean.shape)

    print("4) Validate CLEAN (strict rules)")
    clean_report = validate_clean(df_clean)
    for k, v in clean_report.items():
        print(f"   {k}: {v}")

    if not str(clean_report.get("status", "")).startswith("PASS"):
        raise SystemExit(f"❌ CLEAN validation failed: {clean_report['status']}")

    print("5) Load cleaned output")
    load_data(df_clean, CLEAN_PATH)
    print(f"   saved: {CLEAN_PATH}")

    print("6) Save plots")
    save_plots(df_clean)
    print("   saved plots: outputs/plots/")

    print("✅ Day 2 ETL completed")

if __name__ == "__main__":
    main()
