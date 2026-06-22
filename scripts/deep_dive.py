import pandas as pd
import os

d = r'C:\Users\NguyenNgocKhanh\Desktop\k\sandbox\ai_agent_research_project\data\CSC'
desires = pd.read_csv(os.path.join(d, 'domain_worker_desires.csv'))
metadata = pd.read_csv(os.path.join(d, 'domain_worker_metadata.csv'))

merged = pd.merge(desires, metadata, on='User ID')

print("--- Income vs Desire ---")
print(merged.groupby('Income')['Automation Desire Rating'].mean().sort_values())

print("\n--- Attitudes correlation with Desire ---")
atts = ['AI Tedious Work Attitude', 'AI Job Importance Attitude', 'AI Daily Interest Attitude', 'AI Suffering Attitude']
map_dict = {'Strongly disagree': 1, 'Somewhat disagree': 2, 'Neither agree nor disagree': 3, 'Somewhat agree': 4, 'Strongly agree': 5}
for att in atts:
    merged[att] = merged[att].map(map_dict)
    print(f"{att}: {merged[[att, 'Automation Desire Rating']].corr().iloc[0,1]:.3f}")

print("\n--- LLM Usage Types vs Desire ---")
llm_cols = [c for c in merged.columns if 'LLM Usage by Type' in c]
for col in llm_cols:
    t_avg = merged[merged[col]==True]['Automation Desire Rating'].mean()
    f_avg = merged[merged[col]==False]['Automation Desire Rating'].mean()
    print(f"{col}: Using={t_avg:.2f}, Not Using={f_avg:.2f}, Diff={t_avg-f_avg:.2f}")

print("\n--- Human Agency Scale by Occupation ---")
print(desires.groupby('Occupation (O*NET-SOC Title)')['Human Agency Scale Rating'].mean().sort_values())

print("\n--- Task Frequency vs Desire ---")
tasks = pd.read_csv(os.path.join(d, 'task_statement_with_metadata.csv'))
merged_task = pd.merge(desires, tasks, on='Task ID')
print(merged_task.groupby('Frequency')['Automation Desire Rating'].mean().sort_values())
