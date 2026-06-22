import pandas as pd
import os

target_occupations = [
    "Information Technology Project Managers",
    "Computer and Information Systems Managers",
    "Computer and Information Research Scientists",
    "Computer Systems Analysts",
    "Computer Systems Engineers/Architects"
]

data_dir = r"C:\Users\NguyenNgocKhanh\Desktop\k\sandbox\ai_agent_research_project\data"
out_dir = os.path.join(data_dir, "CSC")

os.makedirs(out_dir, exist_ok=True)

files = [
    "domain_worker_desires.csv",
    "domain_worker_metadata.csv",
    "expert_rated_technological_capability.csv",
    "task_statement_with_metadata.csv"
]

print("Starting data filtering...")
for file in files:
    file_path = os.path.join(data_dir, file)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        filtered_df = df[df["Occupation (O*NET-SOC Title)"].isin(target_occupations)]
        
        out_file = os.path.join(out_dir, file)
        filtered_df.to_csv(out_file, index=False)
        print(f"Filtered {file}: {len(filtered_df)} rows left (from {len(df)} original rows).")
    else:
        print(f"File not found: {file}")

print(f"\nSuccessfully saved all filtered data to: {out_dir}")
