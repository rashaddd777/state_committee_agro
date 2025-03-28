import os, glob
import pandas as pd

raw_dir   = "/Users/rashidkarimov/Desktop/agro/data/processed/dirty/statistics_committee"
clean_dir = "/Users/rashidkarimov/Desktop/agro/data/processed/cleaned/statistics_committee"
os.makedirs(clean_dir, exist_ok=True)

for path in glob.glob(os.path.join(raw_dir, "*.csv")):
    df = pd.read_csv(path, header=0)
    # Drop first unnamed column
    if df.columns[0].startswith("Unnamed"):
        df = df.drop(df.columns[0], axis=1)

    # Strip whitespace in Setting
    df.iloc[:,0] = df.iloc[:,0].astype(str).str.strip()
    df = df[df.iloc[:,0] != ""]

    # Convert all year columns to numeric
    year_cols = [col for col in df.columns if col not in [df.columns[0]]]
    df[year_cols] = df[year_cols].apply(pd.to_numeric, errors="coerce")

    out = os.path.join(clean_dir, os.path.basename(path))
    df.to_csv(out, index=False)
    print(f"✅ Cleaned → {out}")
