import pandas as pd
import glob
import os

# ── Configuration ──────────────────────────────────────────
INPUT_FOLDER = "D:\\elonmusk\\outputs"
OUTPUT_FILE  = "D:\\elonmusk\\merged_tweets_may.csv"
# ───────────────────────────────────────────────────────────

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(INPUT_FOLDER, "*.csv"))

if len(csv_files) == 0:
    print("⚠️  No CSV files found in the folder.")
    exit()

# Display available files with index
print("📂 Available CSV files:\n")
for i, f in enumerate(csv_files):
    row_count = len(pd.read_csv(f, encoding="utf-8-sig"))
    print(f"   [{i}] {os.path.basename(f)}  ({row_count} rows)")

# Let user select files
print("\nEnter the numbers of the files to merge (e.g. 0 2 3), or press Enter to select ALL:")
user_input = input("Your selection: ").strip()

if user_input == "":
    selected_files = csv_files
    print("→ All files selected.")
else:
    try:
        indices = [int(x) for x in user_input.split()]
        selected_files = [csv_files[i] for i in indices]
    except (ValueError, IndexError):
        print("❌ Invalid selection. Please enter valid numbers.")
        exit()

# Confirm selection
print(f"\n✅ Merging {len(selected_files)} file(s):")
for f in selected_files:
    print(f"   → {os.path.basename(f)}")

# Merge selected CSVs
dfs = []
for f in selected_files:
    try:
        df = pd.read_csv(f, encoding="utf-8-sig")
        dfs.append(df)
        print(f"   ✅ Loaded {len(df)} rows from {os.path.basename(f)}")
    except Exception as e:
        print(f"   ❌ Failed to load {os.path.basename(f)}: {e}")

merged = pd.concat(dfs, ignore_index=True)

# Remove duplicates
before = len(merged)
if "Tweet URL" in merged.columns:
    merged.drop_duplicates(subset=["Tweet URL"], inplace=True)
else:
    merged.drop_duplicates(inplace=True)
after = len(merged)

# Save
merged.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"\n📁 Merged file saved to: {OUTPUT_FILE}")
print(f"   Total rows:        {before}")
print(f"   Duplicates removed: {before - after}")
print(f"   Final rows:        {after}")