import os
import glob
import pandas as pd

# Input and output directories
raw_dir = "/Users/rashidkarimov/Desktop/agro/data/raw/statistics_committee"
processed_dir = "/Users/rashidkarimov/Desktop/agro/data/processed/statistics_committee"

# Create folder structure if it doesn't exist
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)

# Convert each Excel file in raw_dir to CSV in processed_dir
for excel_path in glob.glob(os.path.join(raw_dir, "*.xls*")):
    try:
        df = pd.read_excel(excel_path)
        filename = os.path.splitext(os.path.basename(excel_path))[0] + ".csv"
        csv_path = os.path.join(processed_dir, filename)
        df.to_csv(csv_path, index=False)
        print(f"✅ {excel_path} → {csv_path}")
    except Exception as e:
        print(f"❌ Failed converting {excel_path}: {e}")
